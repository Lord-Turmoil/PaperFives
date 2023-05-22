# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 8:19
# @Author  : Tony Skywalker
# @File    : send.py
#
# Description:
#   Send message to target user.
#
from django.views.decorators.csrf import csrf_exempt

from PaperFives.settings import CONFIG
from msgs.models import Message
from msgs.views.deliver import deliver_msg
from shared.dtos.models.msgs import TextMessageDto, LinkMessageDto, ImageMessageDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto, ServerErrorDto
from shared.dtos.response.msgs import MessageResponseDto, TextMessageResponseData, LinkMessageResponseData, \
    ImageMessageResponseData, MessageSelfErrorDto
from shared.dtos.response.users import NotLoggedInDto, NoSuchUserDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import BadRequestResponse, GoodResponse, ServerErrorResponse
from shared.utils.json_util import deserialize
from shared.utils.parameter import parse_param
from shared.utils.users.users import get_user_from_request, get_user_by_uid
from shared.utils.validator import validate_image_name
from users.models import User

"""
Text message
    {
        "uid": 123,
        "type": 0,
        "msg": {
            "text": "for text message"
        }
    }
Link message
    {
        "uid": 123,
        "type": 1,
        "msg": {
            "text": "link message text",
            "link": "url"
        }
    }
Image message (multipart/form-data)
    {
        "uid": 123,
        "type": 2
    }
    ---
    'file': 'image file'
"""


def _send_text_msg(request, src, dst, data: TextMessageDto):
    msg = {'text': data.msg.text}
    message, payload, hint = deliver_msg(src, dst, Message.MessageType.TEXT, msg)
    if message is None:
        return None, hint
    return TextMessageResponseData(src, dst, message.timestamp, payload), None


def _send_link_msg(request, src, dst, data: LinkMessageDto):
    msg = {'text': data.msg.text, 'link': data.msg.link}
    message, payload, hint = deliver_msg(src, dst, Message.MessageType.LINK, msg)
    if message is None:
        return None, hint
    return LinkMessageResponseData(src, dst, message.timestamp, payload), None


def _send_image_msg(request, src, dst, data: ImageMessageDto):
    file = request.FILES.get('file')
    if file is None:
        return None, "Missing image file"
    if not validate_image_name(file.name):
        return None, "Invalid image type!"

    # save default image
    msg = {'url': f"{CONFIG['DEFAULT_IMG_MSG']}"}
    message, payload, hint = deliver_msg(src, dst, Message.MessageType.IMAGE, msg)
    if message is None:
        return None, hint

    # change image to user uploaded file
    img_path = f"{CONFIG['IMG_MSG_PATH']}{src}-{dst}-{payload.mid}.{file.name.split('.')[-1]}"
    try:
        f = open(f"{CONFIG['PROJECT_PATH']}{img_path}", "wb")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
    except Exception as e:
        print(e)
        return ServerErrorResponse(ServerErrorDto("Failed to save message image!"))
    payload.path = img_path
    payload.save()

    return ImageMessageResponseData(src, dst, message.timestamp, payload), None


@csrf_exempt
def send_msg(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    # current logged-in user
    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    # get message type
    params = parse_param(request)
    try:
        msg_type = int(params.pop('type', -1))  # remove as should not in dto
    except:
        return BadRequestResponse(BadRequestDto("Message type should be int"))
    if msg_type not in Message.MessageType.values:
        return BadRequestResponse(BadRequestDto("Invalid message type"))

    # get corresponding request dto class
    dto_cls = None
    sender = None
    if msg_type == Message.MessageType.TEXT:
        dto_cls = TextMessageDto
        sender = _send_text_msg
    elif msg_type == Message.MessageType.LINK:
        dto_cls = LinkMessageDto
        sender = _send_link_msg
    elif msg_type == Message.MessageType.IMAGE:
        dto_cls = ImageMessageDto
        sender = _send_image_msg
    else:
        return BadRequestResponse(BadRequestDto("Unsupported message type"))

    # parse request parameter
    data = None
    try:
        params.pop('csrfmiddlewaretoken', None)
        data = deserialize(params, dto_cls)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))

    # confirm target user
    target: User = get_user_by_uid(data.uid)
    if target is None:
        return GoodResponse(NoSuchUserDto())
    if target.uid == user.uid:
        return GoodResponse(MessageSelfErrorDto())

    response_data, hint = sender(request, user.uid, target.uid, data)
    if response_data is None:
        return BadRequestResponse(BadRequestDto(hint))

    # target user message count++
    target.stat.message_cnt += 1
    target.stat.save()

    return GoodResponse(MessageResponseDto(response_data))
