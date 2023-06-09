# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 14:13
# @Author  : Tony Skywalker
# @File    : middleware.py
#
from shared.dtos.response.users import NotAuthorizedDto
from shared.response.basic import NotAuthorizedResponse
from shared.utils.token import verify_token

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object

BASE_URL = "/api/v1/"
PSEUDO_BASE_URL = "/pseudo/"

API_WHITELIST = ["/api/v1/user/login/", "/api/v1/user/register/"]

API_BLACKLIST = [
    f"{BASE_URL}users/profile/profile",

    f"{BASE_URL}users/favorite/follow",
    f"{BASE_URL}users/favorite/unfollow",
    f"{BASE_URL}users/favorite/isfollower",
    f"{BASE_URL}users/favorite/isfollowee",

    f"{BASE_URL}papers/upload/info",
    f"{BASE_URL}papers/upload/file",

    f"{BASE_URL}papers/download/file",

    f"{BASE_URL}papers/cancel",
    f"{BASE_URL}papers/publish",

    f"{BASE_URL}papers/action/favorite",
    f"{BASE_URL}papers/action/unfavorite",

    f"{BASE_URL}papers/areas/add",
    f"{BASE_URL}papers/areas/del",
    f"{BASE_URL}papers/areas/get",

    f"{BASE_URL}papers/review/pending",
    f"{BASE_URL}papers/review/get",
    f"{BASE_URL}papers/review/release",
    f"{BASE_URL}papers/review/review",

    f"{BASE_URL}msgs/send",
    f"{BASE_URL}msgs/get",
    f"{BASE_URL}msgs/unread",
]

API_PSEUDO_BLACKLIST = [f"{PSEUDO_BASE_URL}cancel/"]


def _authorize_session(request):
    if request.session.get('uid', None) is None:
        return NotAuthorizedResponse(NotAuthorizedDto("No login information"))
    return None


def _authorize_jwt(request):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    if not verify_token(token):
        return NotAuthorizedResponse(NotAuthorizedDto("Not Authorized! Please Login first!"))
    return None


class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in API_BLACKLIST:
            return
        # if request.path not in API_PSEUDO_BLACKLIST:
        #     return
        ret = _authorize_jwt(request)
        if ret is not None:
            return ret
