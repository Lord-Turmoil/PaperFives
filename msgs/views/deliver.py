# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 9:24
# @Author  : Tony Skywalker
# @File    : deliver.py
#
# Description:
#   This will deliver message directly to user. Can be used as
# system message.
#
from msgs.models import Message, TextPayload, LinkPayload, ImagePayload
from shared.utils.str_util import is_no_content
from shared.utils.users.users import get_user_by_uid


def deliver_text_msg(src: int, dst: int, data: dict):
    text = data.get('text')
    if is_no_content(text):
        return None, None, "Text message data format error"

    try:
        payload = TextPayload.create(text)
        payload.save()
    except Exception as e:
        return None, None, str(e)

    try:
        message = Message.create(payload.mid, src, dst, Message.MessageType.TEXT)
        message.save()
    except Exception as e:
        payload.delete()
        return None, None, str(e)

    return message, payload, None


def deliver_link_msg(src: int, dst: int, data: dict):
    text = data.get('text')
    link = data.get('link')
    if is_no_content(text) or is_no_content(link):
        return None, None, "Link message data format error"

    try:
        payload = LinkPayload.create(text, link)
        payload.save()
    except Exception as e:
        return None, None, str(e)

    try:
        message = Message.create(payload.mid, src, dst, Message.MessageType.LINK)
        message.save()
    except Exception as e:
        payload.delete()
        return None, None, str(e)

    return message, payload, None


def deliver_image_msg(src: int, dst: int, data: dict):
    url = data.get('url')
    if is_no_content(url):
        return None, None, "Image message data format error"

    try:
        payload = ImagePayload.create(url)
        payload.save()
    except Exception as e:
        return None, None, str(e)

    try:
        message = Message.create(payload.mid, src, dst, Message.MessageType.IMAGE)
        message.save()
    except Exception as e:
        payload.delete()
        return None, None, str(e)

    return message, payload, None


def deliver_msg(src: int, dst: int, msg_type: Message.MessageType, data: dict):
    if get_user_by_uid(src) is None or get_user_by_uid(dst) is None:
        return None, None, "No such user"

    if msg_type == Message.MessageType.TEXT:
        return deliver_text_msg(src, dst, data)
    elif msg_type == Message.MessageType.LINK:
        return deliver_link_msg(src, dst, data)
    elif msg_type == Message.MessageType.IMAGE:
        return deliver_image_msg(src, dst, data)

    return None, None, "Message type not supported"
