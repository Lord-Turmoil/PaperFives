# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 13:34
# @Author  : Tony Skywalker
# @File    : token.py
#
# Description:
#   For JWT token and password generation & verification.
#

import hashlib
import time

from django.contrib.auth.hashers import make_password, check_password
from django.core import signing

from PaperFives import settings

HEADER = {'type': 'JWT', 'alg': 'default'}
KEY = settings.SECRETS['signing']['key']
SALT = settings.SECRETS['signing']['salt']


def _encrypt(src):
    value = signing.dumps(src, key=KEY, salt=SALT)
    value = signing.b64_encode(value.encode()).decode()
    return value


def _decrypt(src):
    src = signing.b64_decode(src.encode()).decode()
    raw = signing.loads(src, key=KEY, salt=SALT)
    return raw


def generate_token(identity: str) -> str:
    """
    Should pass an identity here, can be email or uid.
    :param identity: str that can determine a user
    :return:
    """

    header = _encrypt(HEADER)

    # valid in 14 days
    payload = {"id": identity, "iat": time.time(), "exp": time.time() + 1209600.0}
    payload = _encrypt(payload)

    # MD5 signature
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    signature = md5.hexdigest()

    token = "%s.%s.%s" % (header, payload, signature)

    return token


def _get_payload(token):
    payload = str(token).split('.')[1]
    return _decrypt(payload)


def _get_header(token):
    header = str(token).split('.')[0]
    return _decrypt(header)


def _verify_signature(token) -> bool:
    try:
        header = str(token).split('.')[0]
        payload = str(token).split('.')[1]
        signature = str(token).split('.')[2]
    except:
        return False
    md5 = hashlib.md5()
    md5.update(("%s.%s" % (header, payload)).encode())
    return signature == md5.hexdigest()


def get_identity_from_token(token):
    payload = _get_payload(token)
    return payload.get('id', None)


def get_expire_from_token(token):
    payload = _get_payload(token)
    return payload.get('exp', None)


def verify_token(token) -> bool:
    if (token is None) or (not _verify_signature(token)):
        return False
    try:
        if (_get_header(token) != HEADER) or (get_identity_from_token(token) is None):
            return False
        exp = get_expire_from_token(token)
    except Exception as e:
        print(e)
        return False
    if exp is None:
        return False
    return exp > time.time()


def generate_password(password) -> str:
    return make_password(password, SALT, 'pbkdf2_sha1')


def verify_password(password, token) -> bool:
    return check_password(password, token)
