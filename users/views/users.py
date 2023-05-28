# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/20/2023 13:15
# @Author  : Tony Skywalker
# @File    : users.py
#
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from shared.dtos.models.users import GetUsersDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.json_util import deserialize
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.users.users import get_user_by_email
from users.serializer import UserSerializer, UserSimpleSerializer, UserPrivateSerializer
from users.views.utils.users import get_users_from_uid_list


@csrf_exempt
def query_users(request):
    """
    Query users based on given fields. If no field given, all users will be listed.
    This response is paginated, and page size and page number can be customized.
    Query settings are:
      - mode : 'all' for all details, 'min' for essential only
      - ps   : page size, default is 20
      - p    : page number, default is 1
    Available query parameters are:
      - email
      - username
      - institute
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)

    # query settings
    mode = parse_value(params.get('mode', 'min'), str)
    page_size = parse_value(params.get('ps'), int, 20)
    page_num = parse_value(params.get('p'), int, 1)
    if (page_size < 1) or (page_num < 1):
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))

    # query parameters
    email = parse_value(params.get('email', None), str)
    username = parse_value(params.get('username', None), str)
    institute = parse_value(params.get('institute', None), str)

    users = SearchQuerySet().all()
    if (email is not None) and (not is_no_content(email)):
        users = users.filter_or(email__contains=email)
    if (username is not None) and (not is_no_content(username)):
        users = users.filter_or(username__fuzzy=username)
    if (institute is not None) and (not is_no_content(institute)):
        users = users.filter_or(institute__fuzzy=institute)

    # paginate
    paginator = Paginator(users, page_size)
    page = paginator.get_page(page_num)

    # construct result
    data = {
        'ps': page_size,
        'p': page.number,
        'total': users.count(),
        'next': paginator.num_pages > page.number,
        'users': []
    }
    if mode == 'all':
        serializer = UserSerializer
    else:
        serializer = UserSimpleSerializer

    # the result in search is not complete
    for user in page.object_list:
        data['users'].append(serializer(get_user_by_email(user.email)).data)

    return GoodResponse(GoodResponseDto(data=data))


@csrf_exempt
def get_users(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)
    try:
        params.pop('csrfmiddlewaretoken', None)
        data: GetUsersDto = deserialize(params, GetUsersDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))

    if data.mode == 'all':
        serializer = UserPrivateSerializer
    else:
        serializer = UserSimpleSerializer
    uid_list = data.users

    payload = {'users': get_users_from_uid_list(uid_list, serializer)}
    payload['total'] = len(payload['users'])

    return GoodResponse(GoodResponseDto(data=payload))
