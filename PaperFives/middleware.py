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

API_WHITELIST = ["/api/user/login", "/api/user/register"]
API_BLACKLIST = []

class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path not in API_BLACKLIST:
            return
        identity = request.META.get('HTTP_IDENTITY')
        token = request.META.get('HTTP_AUTHORIZATION')
        if identity is None or token is None:
            return NotAuthorizedResponse(NotAuthorizedDto("No login information"))
        if not verify_token(identity, token):
            return NotAuthorizedResponse(NotAuthorizedDto("Invalid token"))
        pass
