# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:21
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path

from .views import register, login, profile

urlpatterns = [
    # basic register and login
    path('verification/', register.get_verification_code),
    path('register/', register.register),
    path('login/', login.login),
    path('logout/', login.logout),

    # profile
    path('profile/user', profile.get_user),
    path('profile/profile/', profile.edit_user_profile),
    path('profile/avatar/', profile.edit_user_avatar)
]
