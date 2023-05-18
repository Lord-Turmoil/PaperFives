# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:24
# @Author  : Tony Skywalker
# @File    : register.py
#
from django.views.decorators.csrf import csrf_exempt

from PaperFives.settings import ERROR_CODE
from shared.dtos.base import GoodDto
from shared.dtos.error import RequestMethodErrorDto, BadRequestDto, GeneralErrorDto
from shared.dtos.user import RegisterDto
from shared.exceptions.email import EmailException
from shared.exceptions.json import JsonException
from shared.response.base import BaseResponse
from shared.response.basic import BadRequestResponse
from shared.utils.email_util import generate_code, send_code_email
from shared.utils.json_util import deserialize_dict
from users.models import User


@csrf_exempt
def get_verification_code(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    email = request.POST.get('email', None)
    if not email:
        return BadRequestResponse(BadRequestDto("missing 'email' field"))

    code = generate_code()
    try:
        send_code_email(email, code)
    except EmailException as e:
        return BaseResponse(GeneralErrorDto(ERROR_CODE['SEND_EMAIL'], "Failed to send email"))
    request.session['ver'] = { 'email': email, 'code': code }
    request.session.set_expiry(60 * 10) # expire after 10 minutes
    return BaseResponse(GoodDto("verification code sent"))

EMAIL_WHITE_LIST = [
    "111@111.com",
    "222@222.com",
    "333@333.com"
] # for debug purpose

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
    dto:RegisterDto = RegisterDto() # bad...
    try:
        dto = deserialize_dict(request.POST, RegisterDto)
    except JsonException as e:
        print(e)
        return BadRequestResponse(BadRequestDto())

    users = User.objects.filter(email=dto.email[0])
    if users.exists():
        return BaseResponse(GeneralErrorDto(ERROR_CODE['DUPLICATE_USER'], "User already registerd"))

    if dto.email[0] not in EMAIL_WHITE_LIST:
        ver = request.session['ver']
        error_hint = ""
        error_code = ERROR_CODE['NOT_VERIFIED']
        if ver is None:
            error_hint = "Did you acquired verification code? Or has it expired?"
            return BaseResponse(GeneralErrorDto(error_code, error_hint))
        if ver['email'] != dto.email[0]:
            error_hint = "Did you secretly change your email?"
            return BaseResponse(GeneralErrorDto(error_code, error_hint))
        if ver['code'] != dto.code[0]:
            error_hint = "Oops! Wrong verification code!"
            return BaseResponse(GeneralErrorDto(error_code, error_hint))
    request.session.clear() # clear verification code

    # now, user is verified!
    user = User.create(dto.email[0], dto.username[0])
    user.save()

    return BaseResponse(GoodDto("Welcome to PaperFives!"))
