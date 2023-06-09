# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 18:03
# @Author  : Tony Skywalker
# @File    : urls.py
#
from django.urls import path

from .views import send, msgs

urlpatterns = [
    # path('login/', )
    path('send', send.send_msg),
    path('update', send.update_contact),
    path('get', msgs.get_messages),
    path('unread', msgs.get_unread_msg),
    path('contacts', msgs.get_contacts),
    path('delete', msgs.delete_contact),
]
