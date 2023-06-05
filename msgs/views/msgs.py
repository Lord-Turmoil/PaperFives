# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 11:33
# @Author  : Tony Skywalker
# @File    : msgs.py
#
# Description:
#   Get messages.
#
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from msgs.models import Message, TextPayload, LinkPayload, ImagePayload
from msgs.views.utils.contact import get_contacts_of_user
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.msgs import TextMessageResponseData, LinkMessageResponseData, ImageMessageResponseData
from shared.dtos.response.users import NotLoggedInDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.users.users import get_user_from_request
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

    return GoodResponse(GoodResponseDto(data={'total': len(contacts), 'contacts': contacts}))


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
    params = parse_param(request)

    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    # query settings
    page_size = parse_value(params.get('ps'), int, 20)
    page_num = parse_value(params.get('p'), int, 1)
    if (page_size < 1) or (page_num < 1):
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))

    messages = Message.objects.filter(dst_uid=user.uid).order_by('-timestamp')
    paginator = Paginator(messages, page_size)
    page = paginator.get_page(page_num)

    # construct result
    data = {
        'ps': page_size,
        'p': page.number,
        'total': messages.count(),
        'next': paginator.num_pages > page.number,
    }

    msg: Message
    msg_list = []
    for msg in page.object_list:
        if not msg.checked:
            msg.checked = True
            msg.save()
            user.stat.message_cnt -= 1
        msg_data, hint = _construct_msg(msg)
        if msg_data is None:
            continue
        msg_list.append(msg_data)
    data['msgs'] = msg_list

    user.stat.save()

    return GoodResponse(GoodResponseDto(data=data))


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
