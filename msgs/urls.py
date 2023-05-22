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
    path('send/', send.send_msg),
    path('get/', msgs.get_messages)
]
