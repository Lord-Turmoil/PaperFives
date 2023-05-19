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
API_WHITELIST = ["/api/user/login", "/api/user/register"]
API_BLACKLIST = [f"{BASE_URL}profile/profile",]

class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in API_BLACKLIST:
            return
        if request.get('uid', None) is None:
            return NotAuthorizedResponse(NotAuthorizedDto("No login information"))
