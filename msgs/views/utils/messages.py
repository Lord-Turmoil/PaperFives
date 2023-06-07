# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 6/5/2023 21:12
# @Author  : Tony Skywalker
# @File    : messages.py
#
# Description:
#   Get messages of user.
#
import functools

from msgs.models import Message
from msgs.views.utils.contact import update_contact_of_user
from shared.dtos.models.msgs import TextMessageListDto, TextMessageData
from users.models import User


def __cmp_message(x: TextMessageData, y: TextMessageData):
    if x.timestamp != y.timestamp:
        return -1 if y.timestamp > x.timestamp else 1
    if x.income == y.income:
        return x.text < y.text
    return 1 if x.income else -1


def get_and_read_messages_of_user(user, dst):
    """
    Get all messages of user and dst. From user's perspective.
    """
    messages = Message.objects.filter(src_uid=user.uid, dst_uid=dst.uid)
    messages = messages.union(Message.objects.filter(src_uid=dst.uid, dst_uid=user.uid))

    # read messages
    read = 0
    for message in messages:
        if message.checked:
            continue
        message.checked = True
        message.save()
        read += 1
    user: User
    user.stat.message_cnt -= read
    if user.stat.message_cnt < 0:
        user.stat.message_cnt = 0
    user.stat.save()

    message_list = TextMessageListDto().init(user.uid, messages).msgs

    # contact in user's perspective should update, and clear all unread
    # but not update timestamp
    update_contact_of_user(user.uid, dst.uid, -1, False)

    return sorted(message_list, key=functools.cmp_to_key(__cmp_message))


def get_messages_of_user(user, dst):
    """
    Get all messages of user and dst. From user's perspective.
    """
    messages = Message.objects.filter(src_uid=user.uid, dst_uid=dst)
    messages.union(Message.objects.filter(src_uid=dst.uid, dst_uid=user.uid))

    message_list = TextMessageListDto().init(user.uid, messages).msgs

    return sorted(message_list, key=functools.cmp_to_key(__cmp_message))


def read_message(mid):
    messages = Message.objects.filter(mid=mid)
    for message in messages:
        if message.checked:
            continue
        message.checked = True
        message.save()
