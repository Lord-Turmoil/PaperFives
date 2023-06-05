# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 6/5/2023 18:31
# @Author  : Tony Skywalker
# @File    : contact.py
#
# Description:
#   Contact related functions.
#
import functools

from msgs.models import Message
from shared.dtos.models.msgs import ContactData
from shared.utils.users.users import get_user_by_uid
from users.models import User


def __get_message_stat(src, dst):
    outcomes = Message.objects.filter(src_uid=src, dst_uid=dst)
    incomes = Message.objects.filter(src_uid=dst, dst_uid=src)

    # Assume that there is always last time.
    last_time = None
    for msg in outcomes:
        if (last_time is None) or (last_time < msg.timestamp):
            last_time = msg.timestamp
    unread = 0
    for msg in incomes:
        if (last_time is None) or (last_time < msg.timestamp):
            last_time = msg.timestamp
        if not msg.checked:
            unread += 1

    return unread, last_time


def _get_contact_of_user(src, dst):
    """
    Get the contact from src to dst.
    """
    unread, timestamp = __get_message_stat(src.uid, dst.uid)
    if timestamp is None:
        return None
    contact = ContactData().init(dst, timestamp, unread)
    return contact


def __cmp_contact(x: ContactData, y: ContactData):
    if x.unread != y.unread:
        return y.unread - x.unread
    if x.timestamp != y.timestamp:
        return 1 if y.timestamp > x.timestamp else -1
    return x.uid - y.uid


def get_contacts_of_user(user):
    """
    Get contact of user with uid.
    """
    # Get all related users
    uid_list = []
    dsts = Message.objects.filter(src_uid=user.uid)
    dst: Message
    for dst in dsts:
        if dst.dst_uid not in uid_list:
            uid_list.append(dst.dst_uid)
    srcs = Message.objects.filter(dst_uid=user.uid)
    for src in srcs:
        if src.src_uid not in uid_list:
            uid_list.append(src.src_uid)

    contacts = []
    for uid in uid_list:
        if uid == user.uid:
            continue
        dst: User = get_user_by_uid(uid)
        if dst is None:
            continue
        contact = _get_contact_of_user(user, dst)
        print(contact.timestamp)
        if contact is not None:
            contacts.append(contact)

    return sorted(contacts, key=functools.cmp_to_key(__cmp_contact))
