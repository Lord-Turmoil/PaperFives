# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/23/2023 14:21
# @Author  : Tony Skywalker
# @File    : users.py
#
from users.models import User, FavoriteUser


def get_users_from_uid_list(uid_list, serializer):
    user_list = []
    for uid in uid_list:
        users = User.objects.filter(uid=uid)
        if not users.exists():
            continue
        user_list.append(serializer(users.first()).data)
    return user_list


def get_users_from_user_list(user_list, serializer):
    users = []
    for user in user_list:
        users.append(serializer(user).data)
    return users


def is_follower_by_id(src, dst):
    favorites = FavoriteUser.objects.filter(src_uid=src, dst_uid=dst)
    if favorites.exists():
        return True
    return False
