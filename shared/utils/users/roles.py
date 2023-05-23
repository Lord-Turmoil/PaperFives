# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 17:49
# @Author  : Tony Skywalker
# @File    : roles.py
#
from users.models import User, Role


def get_roles(user: User):
    roles = user.roles.all()
    ret = []
    for role in roles:
        ret.append(role.name)
    return ret


def get_roles_by_id(uid: int):
    users = User.objects.filter(uid=uid)
    if not users.exists():
        return [Role.RoleName.VISITOR]
    return get_roles(users.first())


def get_roles_by_email(email: str):
    users = User.objects.filter(email=email)
    if not users.exists():
        return [Role.RoleName.VISITOR]
    return get_roles(users.first())


def get_role(user: User):
    roles = user.roles.all()
    if not roles.exists():
        return Role.RoleName.VISITOR
    if Role.RoleName.ADMIN in roles:
        return Role.RoleName.ADMIN
    if Role.RoleName.SCHOLAR in roles:
        return Role.RoleName.SCHOLAR
    return Role.RoleName.USER


def get_role_by_id(uid):
    users = User.objects.filter(uid=uid)
    if not users.exists():
        return Role.RoleName.VISITOR
    return get_role(users.first())


def is_user_visitor_by_id(uid: int) -> bool:
    return Role.RoleName.VISITOR in get_roles_by_id(uid)


def is_user_admin_by_id(uid: int) -> bool:
    return Role.RoleName.ADMIN in get_roles_by_id(uid)


def is_user_admin(user) -> bool:
    if user is None:
        return False
    return Role.RoleName.ADMIN in get_roles(user)
