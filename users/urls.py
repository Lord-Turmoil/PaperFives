# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:21
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path

from .views import register, login, profile, follow, users, tasks

urlpatterns = [
    # basic register and login
    path('verification', register.get_verification_code),
    path('register', register.register_as_user),
    path('register-admin', register.register_as_admin),
    path('cancel', register.cancel_account),
    path('login', login.login),
    path('logout', login.logout),

    # profile
    path('profile/user', profile.get_user),
    path('profile/profile', profile.edit_user_profile),
    path('profile/avatar', profile.edit_user_avatar),
    path('profile/password', profile.edit_user_password),

    # query user
    path('query/query', users.query_users),
    path('query/get', users.get_users),

    # follow
    path('favorite/follow', follow.follow_user),
    path('favorite/unfollow', follow.unfollow_user),
    path('favorite/followers', follow.get_followers),
    path('favorite/followees', follow.get_followees),
    path('favorite/isfollower', follow.is_follower),
    path('favorite/isfollowee', follow.is_followee),

    # tasks
    path('task/update_stat', tasks.update_user_statistics),
]
