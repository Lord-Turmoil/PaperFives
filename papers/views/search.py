# ------- Litang Save The World! -------
#
# @Time    : 2023/5/21 15:44
# @Author  : Lynx
# @File    : search.py
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.errors import RequestMethodErrorDto
from shared.response.basic import BadRequestResponse
from shared.utils.parameter import parse_param


@csrf_exempt
def search(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

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
    return
