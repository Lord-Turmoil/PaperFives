# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 18:34
# @Author  : Tony Skywalker
# @File    : hot.py
#
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.users.users import get_user_by_uid
from users.models import Top20User
from users.serializer import UserSimpleSerializer


@csrf_exempt
def get_hot_users(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    data = {'users': []}
    for user_rank in Top20User.objects.all().order_by('-rank'):
        user = get_user_by_uid(user_rank.uid)
        if user is None:
            continue
        data['users'].append({'user': UserSimpleSerializer(user).data, 'rank': user_rank.rank})

    return GoodResponse(GoodResponseDto(data=data))
