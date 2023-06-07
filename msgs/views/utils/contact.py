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

from django.utils import timezone

from msgs.models import Message, ContactRecord
from shared.dtos.models.msgs import ContactData
from shared.utils.users.users import get_user_by_uid
from users.models import User


def update_contact_of_user(src, dst, unread=0, update_time=True):
    """
    One way, in perspective of src, add unread for src.
    """
    contacts = ContactRecord.objects.filter(src_uid=src, dst_uid=dst)
    contact: ContactRecord
    if contacts.exists():
        contact = contacts.first()
        if update_time:
            contact.timestamp = timezone.now()
    else:
        contact = ContactRecord.create(src, dst)
    if unread < 0:  # reset unread
        contact.unread = 0
    else:
        contact.unread += unread
    contact.save()


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
    records = ContactRecord.objects.filter(src_uid=user.uid)
    contacts = []
    for record in records:
        dst: User = get_user_by_uid(record.dst_uid)
        if dst is None:
            continue
        contact = ContactData().init(dst, record.timestamp, record.unread)
        contacts.append(contact)

    return sorted(contacts, key=functools.cmp_to_key(__cmp_contact))
