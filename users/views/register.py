# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:24
# @Author  : Tony Skywalker
# @File    : register.py
#
import datetime

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from PaperFives.settings import ERROR_CODE
from msgs.models import EmailRecord
from shared.dtos.models.users import RegisterDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto, GeneralErrorDto
from shared.dtos.response.users import NoSuchUserDto, NotAuthorizedDto
from shared.exceptions.email import EmailException
from shared.exceptions.json import JsonException
from shared.response.base import BaseResponse
from shared.response.basic import BadRequestResponse, GoodResponse, NotAuthorizedResponse
from shared.utils.email_util import generate_code, send_code_email
from shared.utils.json_util import deserialize_dict
from shared.utils.parameter import parse_param
from shared.utils.token import generate_password
from shared.utils.users.roles import is_user_admin
from shared.utils.users.users import get_user_from_request
from shared.utils.validator import validate_email
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
        return BadRequestResponse(BadRequestDto("Missing 'email' field"))

    # registered user shouldn't get verification code
    users = User.objects.filter(email=email)
    if users.exists():
        return BaseResponse(GeneralErrorDto(ERROR_CODE['DUPLICATE_USER'], "User already registered"))

    if not validate_email(email):
        return BadRequestDto(BadRequestDto("Invalid email format!"))

    code = generate_code()
    try:
        send_code_email(email, code)
    except EmailException as e:
        return BaseResponse(GeneralErrorDto(ERROR_CODE['SEND_EMAIL'], "Failed to send email"))

    # add email into
    EmailRecord.objects.filter(email=email, usage="reg").delete()  # delete previous
    expire = timezone.now() + datetime.timedelta(minutes=10)
    email = EmailRecord.create(email, code, expire, "reg")
    email.save()

    return GoodResponse(GoodResponseDto("Verification code sent"))


def _register(request):
    """
    parameters needed:
    - email    --
    - username --
    - password -- consistency verified in frontend)
    - code     --
    """
    if request.method != 'POST':
        return None, BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    params = parse_param(request)
    dto: RegisterDto = RegisterDto()  # bad...
    try:
        dto = deserialize_dict(params, RegisterDto)
    except JsonException as e:
        return None, BadRequestResponse(BadRequestDto(e))
    if not dto.is_valid():
        return None, BadRequestResponse(BadRequestDto("invalid data value"))

    users = User.objects.filter(email=dto.email)
    if users.exists():
        return None, BaseResponse(GeneralErrorDto(ERROR_CODE['DUPLICATE_USER'], "User already registered"))

    # get email record
    error_code = ERROR_CODE['NOT_VERIFIED']
    emails = EmailRecord.objects.filter(email=dto.email, usage="reg", valid=True)
    if not emails.exists():
        error_hint = "Did you acquire verification code? Or has it expired?"
        return None, BaseResponse(GeneralErrorDto(error_code, error_hint))
    for email in emails:
        if timezone.now() > email.expire:
            email.valid = 0
            email.save()
    email = emails.last()
    if not email.valid:
        error_hint = "Oops! Verification code expired!"
        return None, BaseResponse(GeneralErrorDto(error_code, error_hint))
    if email.code != dto.code:
        error_hint = "Oops! Wrong verification code!"
        return None, BaseResponse(GeneralErrorDto(error_code, error_hint))
    email.valid = False
    email.save()

    # now, user is verified!
    user = User.create(dto.email, dto.username, generate_password(dto.password))
    user.save()

    return user, None


@csrf_exempt
def register_as_user(request):
    user, res = _register(request)
    if user is None:
        return res

    role = Role.create(Role.RoleName.USER, user)
    role.save()

    return GoodResponse(GoodResponseDto("Welcome to PaperFives!"))


@csrf_exempt
def register_as_admin(request):
    """
    The same as register, but will get admin privilege.
    """
    user, res = _register(request)
    if user is None:
        return res

    role = Role.create(Role.RoleName.USER, user)
    role.save()
    role = Role.create(Role.RoleName.ADMIN, user)
    role.save()

    return GoodResponse(GoodResponseDto("Welcome to PaperFives! We've been waiting for you."))


@csrf_exempt
def cancel_account(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)
    email = params.get('email')
    if email is None:
        return BadRequestResponse(BadRequestDto("Missing email"))
    users = User.objects.filter(email=email)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()

    profile = get_user_from_request(request)
    if profile is None:
        return NotAuthorizedResponse(NotAuthorizedDto("Login before you cancel the account"))
    if not is_user_admin(profile):
        if profile.email != user.email:
            return NotAuthorizedResponse(NotAuthorizedDto("You cannot cancel other people!"))
    user.attr.delete()
    user.stat.delete()
    user.delete()

    return GoodResponse(GoodResponseDto("Parting is such sweet sorrow."))
