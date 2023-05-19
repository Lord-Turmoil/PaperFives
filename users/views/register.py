# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:24
# @Author  : Tony Skywalker
# @File    : register.py
#
import datetime

from django.views.decorators.csrf import csrf_exempt

from PaperFives.settings import ERROR_CODE
from msgs.models import EmailRecord
from shared.dtos.models.users import RegisterDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto, GeneralErrorDto
from shared.exceptions.email import EmailException
from shared.exceptions.json import JsonException
from shared.response.base import BaseResponse
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.email_util import generate_code, send_code_email
from shared.utils.json_util import deserialize_dict
from shared.utils.parameter import parse_param
from shared.utils.token import generate_password
from users.models import User, Role

EMAIL_WHITE_LIST = [
    "111@111.com",
    "222@222.com",
    "333@333.com"
]  # for debug purpose


@csrf_exempt
def get_verification_code(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)
    email = params.get('email')
    if not email:
        return BadRequestResponse(BadRequestDto("missing 'email' field"))

    # registered user shouldn't get verification code
    users = User.objects.filter(email=email)
    if users.exists():
        return BaseResponse(GeneralErrorDto(ERROR_CODE['DUPLICATE_USER'], "User already registered"))

    code = generate_code()
    try:
        send_code_email(email, code)
    except EmailException as e:
        return BaseResponse(GeneralErrorDto(ERROR_CODE['SEND_EMAIL'], "Failed to send email"))

    # add email into
    EmailRecord.objects.filter(email=email, usage="reg").delete()  # delete previous
    expire = datetime.datetime.now() + datetime.timedelta(minutes=10)
    email = EmailRecord.create(email, code, expire, "reg")
    email.save()

    return GoodResponse(GoodResponseDto("Verification code sent"))


@csrf_exempt
def register(request):
    """
    parameters needed:
    - email    --
    - username --
    - password -- consistency verified in frontend)
    - code     --
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    params = parse_param(request)
    dto: RegisterDto = RegisterDto()  # bad...
    try:
        dto = deserialize_dict(params, RegisterDto)
    except JsonException as e:
        return BadRequestResponse(BadRequestDto(e))
    if not dto.is_valid():
        return BadRequestResponse(BadRequestDto("invalid data value"))

    users = User.objects.filter(email=dto.email)
    if users.exists():
        return BaseResponse(GeneralErrorDto(ERROR_CODE['DUPLICATE_USER'], "User already registered"))

    # get email record
    error_code = ERROR_CODE['NOT_VERIFIED']
    emails = EmailRecord.objects.filter(email=dto.email, usage="reg")
    if not emails.exists():
        error_hint = "Did you acquired verification code? Or has it expired?"
        return BaseResponse(GeneralErrorDto(error_code, error_hint))
    email: EmailRecord = emails.first()
    if datetime.datetime.now() > email.expire:
        error_hint = "Oops! Verification code expired!"
        return BaseResponse(GeneralErrorDto(error_code, error_hint))
    if email.code != dto.code:
        error_hint = "Oops! Wrong verification code!"
        return BaseResponse(GeneralErrorDto(error_code, error_hint))
    email.delete()

    # now, user is verified!
    user = User.create(dto.email, dto.username, generate_password(dto.password))
    user.save()

    role = Role.create(Role.RoleName.USER, user)
    role.save()

    return GoodResponse(GoodResponseDto("Welcome to PaperFives!"))


@csrf_exempt
def register_as_admin(request):
    """
    The same as register, but will get admin privilege.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    dto: RegisterDto = RegisterDto()  # bad...
    try:
        dto = deserialize_dict(request.POST.dict(), RegisterDto)
    except JsonException as e:
        return BadRequestResponse(BadRequestDto(e))
    if not dto.is_valid():
        return BadRequestResponse(BadRequestDto("invalid data value"))

    users = User.objects.filter(email=dto.email)
    if users.exists():
        return BaseResponse(GeneralErrorDto(ERROR_CODE['DUPLICATE_USER'], "User already registered"))

    if dto.email not in EMAIL_WHITE_LIST:
        ver = request.session.get('ver')
        error_hint = ""
        error_code = ERROR_CODE['NOT_VERIFIED']
        if ver is None:
            error_hint = "Did you acquired verification code? Or has it expired?"
            return BaseResponse(GeneralErrorDto(error_code, error_hint))
        if ver['email'] != dto.email:
            error_hint = "Did you secretly change your email?"
            return BaseResponse(GeneralErrorDto(error_code, error_hint))
        if ver['code'] != dto.code:
            error_hint = "Oops! Wrong verification code!"
            return BaseResponse(GeneralErrorDto(error_code, error_hint))
    request.session.clear()  # clear verification code

    # now, user is verified!
    user = User.create(dto.email, dto.username, generate_password(dto.password))
    user.save()

    role = Role.create(Role.RoleName.USER, user)
    role.save()
    role = Role.create(Role.RoleName.ADMIN, user)
    role.save()

    return GoodResponse(GoodResponseDto("Welcome to PaperFives! We've been waiting for you."))
