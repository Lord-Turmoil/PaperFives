# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/30/2023 18:07
# @Author  : Tony Skywalker
# @File    : users.py
#
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from users.models import User
from users.views.register import _erase_user


@csrf_exempt
def cancel_users(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    params = parse_param(request)
    low = parse_value(params.get('left'), int, 0)
    high = parse_value(params.get('right'), int, 99999)

    users = User.objects.filter(uid__in=range(low, high, 1))
    for user in users:
        _erase_user(user.uid)
        user.attr.delete()
        user.stat.delete()
        user.delete()

    return GoodResponse(GoodResponseDto(f"Users {range(low, high, 1)} erased!"))
