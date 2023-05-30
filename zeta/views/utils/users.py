# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/30/2023 0:03
# @Author  : Tony Skywalker
# @File    : users.py
#
from random import Random
from essential_generators import DocumentGenerator

from shared.utils.token import generate_password
from shared.utils.users.users import get_users_by_username, get_user_by_email
from users.models import User, Role, UserAttribute

EMAIL_CHARACTER_SET = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789_-'
DEFAULT_PASSWORD = '123456'

gen = DocumentGenerator()
engine = Random()

def _generate_random_email() -> str:
    email = ""
    max_idx = len(EMAIL_CHARACTER_SET) - 1
    engine = Random()
    length = engine.randint(6, 10)
    for i in range(length):
        email += EMAIL_CHARACTER_SET[engine.randint(0, max_idx)]
    email += '@no.such.email'
    return email


def import_user(username: str):
    """
    Create a pseudo user.
    """
    users = get_users_by_username(username)
    if users.exists():
        return users.first()

    # generate a new email for him
    while True:
        email = gen.email()
        if get_user_by_email(email) is not None:
            continue
        else:
            break

    attr = UserAttribute.create(
            engine.randint(UserAttribute.Sex.UNKNOWN, UserAttribute.Sex.FEMALE),
            gen.slug(),
            gen.sentence())
    attr.save()
    user = User.create(email, username, generate_password(DEFAULT_PASSWORD), "", attr)
    user.scholar = True
    user.save()

    role = Role.create(Role.RoleName.USER, user)
    role.save()

    return user


def increase_publish_cnt(username: str):
    """
    Increase publish cnt of the given user. Do nothing if the
    user does not exist.
    """
    users = get_users_by_username(username)
    if users.exists():
        user: User = users.first()
        user.stat.publish_cnt += 1
        user.stat.save()
