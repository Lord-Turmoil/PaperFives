# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:24
# @Author  : Tony Skywalker
# @File    : login.py
#
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.models.users import LoginDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.users import NoSuchUserDto, WrongPasswordDto, LoginSuccessDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.base import BaseResponse
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.json_util import deserialize_dict
from shared.utils.token import verify_password, generate_token
from users.models import User
from users.serializer import UserSerializer


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    dto: LoginDto = LoginDto()
    try:
        dto = deserialize_dict(request.POST.dict(), LoginDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))
    if not dto.is_valid():
        return BadRequestResponse(BadRequestDto("invalid data value"))

    users = User.objects.filter(email=dto.email)
    if not users.exists():
        return BaseResponse(NoSuchUserDto())
    user = users.first()
    if not verify_password(dto.password, user.password):
        return BaseResponse(WrongPasswordDto())

    # add user session
    request.session['uid'] = user.uid
    request.session.set_expiry(14 * 24 * 60 * 60)  # expire after 14 days

    return GoodResponse(
        LoginSuccessDto(UserSerializer(user).data))


@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    if request.session.get('uid') is not None:
        request.session.clear()
    return GoodResponse(GoodResponseDto("See you later!"))
