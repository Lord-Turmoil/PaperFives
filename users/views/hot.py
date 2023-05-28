# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 18:34
# @Author  : Tony Skywalker
# @File    : hot.py
#
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.users.users import get_user_by_uid
from users.models import UserRank
from users.serializer import UserSimpleSerializer


@csrf_exempt
def get_hot_users(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)

    page_size = parse_value(params.get('ps'), int, 20)
    page_num = parse_value(params.get('p'), int, 1)
    if (page_size < 1) or (page_num < 1):
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))

    user_ranks = UserRank.objects.all().order_by('-rank')
    paginator = Paginator(user_ranks, page_size)
    page = paginator.get_page(page_num)

    data = {
        'ps': page_size,
        'p': page.number,
        'total': user_ranks.count(),
        'next': paginator.num_pages > page.number,
        'users': []
    }

    for user_rank in user_ranks:
        user = get_user_by_uid(user_rank.uid)
        if user is None:
            continue
        data['users'].append({'user': UserSimpleSerializer(user).data, 'rank': user_rank.rank})

    return GoodResponse(GoodResponseDto(data=data))
