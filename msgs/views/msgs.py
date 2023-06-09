# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 11:33
# @Author  : Tony Skywalker
# @File    : msgs.py
#
# Description:
#   Get messages.
#
from django.views.decorators.csrf import csrf_exempt

from msgs.models import Message, TextPayload, LinkPayload, ImagePayload, ContactRecord
from msgs.views.utils.contact import get_contacts_of_user
from msgs.views.utils.messages import get_and_read_messages_of_user
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.msgs import TextMessageResponseData, LinkMessageResponseData, ImageMessageResponseData
from shared.dtos.response.users import NotLoggedInDto, NoSuchUserDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.users.users import get_user_from_request, get_user_by_uid
from users.models import User


def _construct_msg(msg: Message):
    if msg.mtype == Message.MessageType.TEXT:
        model = TextPayload
        data = TextMessageResponseData
    elif msg.mtype == Message.MessageType.LINK:
        model = LinkPayload
        data = LinkMessageResponseData
    elif msg.mtype == Message.MessageType.IMAGE:
        model = ImagePayload
        data = ImageMessageResponseData
    else:
        return None, "Invalid message type"

    payloads = model.objects.filter(mid=msg.mid)
    if not payloads.exists():
        return None, "Message does not exist"
    payload = payloads.first()

    return data(msg.src_uid, msg.dst_uid, msg.timestamp, payload), None


@csrf_exempt
def get_contacts(request):
    """
    Get all users that has message with me.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    # Get all contacts
    contacts = get_contacts_of_user(user)

    data = {
        'total': len(contacts),
        'avatar': user.avatar,
        'contacts': contacts
    }

    return GoodResponse(GoodResponseDto(data=data))


@csrf_exempt
def delete_contact(request):
    """
    Delete user contact.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    uid = parse_value(params.get('uid'), int)
    if uid is None:
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))

    ContactRecord.objects.filter(src_uid=user.uid, dst_uid=uid).delete()

    return GoodResponse(GoodResponseDto(f"Contact from {user.uid} to {uid} deleted!"))


@csrf_exempt
def get_messages(request):
    """
    Get massages of the current user.
    Settings are:
      - ps   : page size, default is 20
      - p    : page number, default is 1
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    dst_uid = parse_value(params.get('uid'), int)
    if dst_uid is None:
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))
    dst: User = get_user_by_uid(dst_uid)
    if dst is None:
        return GoodResponse(NoSuchUserDto())

    messages = get_and_read_messages_of_user(user, dst)

    return GoodResponse(GoodResponseDto(data={'total': len(messages), 'msgs': messages}))


@csrf_exempt
def get_unread_msg(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    messages = Message.objects.filter(dst_uid=user.uid, checked=False).order_by('-timestamp')
    total = messages.count()
    # construct result
    data = {
        'total': total
    }

    user.stat.message_cnt -= total
    if user.stat.message_cnt < 0:
        user.stat.message_cnt = 0
    user.save()

    msg_list = []
    for msg in messages:
        msg.checked = True
        msg.save()
        msg_data, hint = _construct_msg(msg)
        if msg_data is None:
            continue
        msg_list.append(msg_data)
    data['msgs'] = msg_list

    return GoodResponse(GoodResponseDto(data=data))
