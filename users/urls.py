# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:21
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path
from .views import test

urlpatterns = [
    # path('login/', )
    path('_get_all/', test.get_user_all),
    path('_get/', test.get_user_by_id),
    path('_put/', test.put_user)
]
