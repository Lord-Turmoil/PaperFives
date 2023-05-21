# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 16:26
# @Author  : Tony Skywalker
# @File    : profile.py
#
# Description:
#   This file contains APIs to get user information.
import os

from django.views.decorators.csrf import csrf_exempt

from PaperFives.settings import CONFIG
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import BadRequestDto, RequestMethodErrorDto, ServerErrorDto
from shared.dtos.response.users import NoSuchUserDto, UserProfileDto, NotLoggedInDto, WrongPasswordDto
from shared.response.basic import BadRequestResponse, GoodResponse, ServerErrorResponse
from shared.utils.parameter import parse_param
from shared.utils.str_util import is_no_content
from shared.utils.token import verify_password, generate_password
from shared.utils.users.roles import is_user_admin, get_roles
from shared.utils.users.users import get_user_from_request
from shared.utils.validator import validate_image_name, validate_password
from users.models import User, UserAttribute
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
    params = parse_param(request)
    mode = params.get('mode')
    uid = params.get('uid')
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
    if (profile is not None) and (user.uid == profile.uid or is_user_admin(profile)):
        data['roles'] = get_roles(user)
    else:
        data['roles'] = []

    return GoodResponse(UserProfileDto(data))


@csrf_exempt
def edit_user_profile(request):
    """
    Will only update given fields.
    - username
    - sex
    - institute
    - motto
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    uid = request.session.get('uid')
    if uid is None:
        return GoodResponse(NotLoggedInDto())
    users = User.objects.filter(uid=uid)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()

    params = parse_param(request)
    username = params.get('username')
    sex = int(params.get('sex', -1))
    institute = params.get('institute')
    motto = params.get('motto')

    if not is_no_content(username):
        user.username = username
    attr: UserAttribute = user.attr
    if sex in UserAttribute.Sex.values:
        attr.sex = sex
    if not is_no_content(institute):
        attr.institute = institute
    if not is_no_content(motto):
        attr.motto = motto
    attr.save()
    user.save()

    return GoodResponse(UserProfileDto(UserSerializer(user).data))


@csrf_exempt
def edit_user_avatar(request):
    """
    Change user avatar.
    This request must be multipart/form-data.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    uid = request.session.get('uid')
    if uid is None:
        return GoodResponse(NotLoggedInDto())
    users = User.objects.filter(uid=uid)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()

    # get avatar from request
    file = request.FILES.get('file')
    if file is None:
        return BadRequestResponse(BadRequestDto("Missing image file"))
    if not validate_image_name(file.name):
        return BadRequestResponse(BadRequestDto("Invalid image type!"))

    # save avatar to file.
    avatar = f"{CONFIG['AVATAR_PATH']}{user.uid}.{file.name.split('.')[-1]}"
    if user.avatar != CONFIG['DEFAULT_AVATAR']:  # has avatar before
        if user.avatar != avatar:  # different filename
            try:
                os.remove(f"{CONFIG['PROJECT_PATH']}{user.avatar}")  # remove old avatar
            except:
                pass

    try:
        f = open(f"{CONFIG['PROJECT_PATH']}{avatar}", "wb")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
    except Exception as e:
        print(e)
        return ServerErrorResponse(ServerErrorDto("Failed to save avatar!"))

    user.avatar = avatar
    user.save()

    return GoodResponse(UserProfileDto(UserSimpleSerializer(user).data))


@csrf_exempt
def edit_user_password(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    uid = request.session.get('uid')
    if uid is None:
        return GoodResponse(NotLoggedInDto())
    users = User.objects.filter(uid=uid)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()

    params = parse_param(request)

    old_pwd = params.get('old')
    new_pwd = params.get('new')
    if old_pwd is None or new_pwd is None:
        return BadRequestResponse(BadRequestDto("missing parameters"))
    if not verify_password(old_pwd, user.password):
        return GoodResponse(WrongPasswordDto())
    if not validate_password(new_pwd):
        return BadRequestResponse(BadRequestDto("Invalid password formt"))

    user.password = generate_password(new_pwd)
    user.save()

    return GoodResponse(GoodResponseDto("Password changed!"))
