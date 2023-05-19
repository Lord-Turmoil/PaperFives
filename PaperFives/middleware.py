# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 14:13
# @Author  : Tony Skywalker
# @File    : middleware.py
#
from shared.dtos.response.users import NotAuthorizedDto
from shared.response.basic import NotAuthorizedResponse

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object

BASE_URL = "/api/v1/"
PSEUDO_BASE_URL = "/pseudo/"
API_WHITELIST = ["/api/user/login", "/api/user/register"]
API_BLACKLIST = [f"{BASE_URL}profile/profile/", ]
API_PSEUDO_BLACKLIST = [f"{PSEUDO_BASE_URL}cancel/"]


class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in API_BLACKLIST:
            return
        if request.path not in API_PSEUDO_BLACKLIST:
            return
        if request.session.get('uid', None) is None:
            return NotAuthorizedResponse(NotAuthorizedDto("No login information"))
