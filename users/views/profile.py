# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 16:26
# @Author  : Tony Skywalker
# @File    : profile.py
#
# Description:
#   This file contains APIs to get user information.
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.errors import BadRequestDto, RequestMethodErrorDto, ServerErrorDto
from shared.dtos.response.users import NoSuchUserDto, UserProfileDto
from shared.response.basic import BadRequestResponse, GoodResponse, ServerErrorResponse
from shared.utils.users.roles import is_user_admin, get_roles
from shared.utils.users.users import get_user_from_request
from users.models import User
from users.serializer import UserSerializer, UserSimpleSerializer


@csrf_exempt
def get_user(request):
    """
    Get only primary information of user.
    profile/user?mode=all&id=uid
        mode=all -- all information
        mode=min -- only minimum information
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    mode = request.GET.get('mode', None)
    uid = request.GET.get('uid', None)
    if mode is None or uid is None:
        return BadRequestResponse(BadRequestDto("missing parameters"))

    # switch mode
    serializer = None
    if mode == 'all':
        serializer = UserSerializer
    elif mode == 'min':
        serializer = UserSimpleSerializer
    else:
        return BadRequestResponse(BadRequestDto("invalid mode"))

    # get original user
    users = User.objects.filter(uid=uid)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()
    data = None
    try:
        data = serializer(user).data
    except:
        return ServerErrorResponse(ServerErrorDto("Failed to get user data"))

    profile = get_user_from_request(request)
    if profile is not None:
        if user.uid == profile.uid:
            data['roles'] = get_roles(user)
        elif is_user_admin(profile):
            data['roles'] = get_roles(user)

    return GoodResponse(UserProfileDto(data))
