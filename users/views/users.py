# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/20/2023 13:15
# @Author  : Tony Skywalker
# @File    : users.py
#
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.models.users import GetUsersDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.json_util import deserialize
from shared.utils.parameter import parse_param
from shared.utils.str_util import is_no_content
from users.models import User
from users.serializer import UserSerializer, UserSimpleSerializer


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
    mode = params.get('mode', 'min')
    page_size = 20
    try:
        ps = params.get('ps')
        page_size = 20 if is_no_content(ps) else int(ps)
        p = params.get('p')
        page_num = 1 if is_no_content(p) else int(p)
    except:
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))

    # query parameters
    email = params.get('email', None)
    username = params.get('username', None)
    institute = params.get('institute', None)

    # get results
    users = User.objects.all()
    if email is not None:
        users = users.filter(email__icontains=email)
    if username is not None:
        users = users.filter(username__icontains=username)
    if institute is not None:
        users = users.filter(attr__institute__icontains=institute)

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
    serializer = None
    if mode == 'all':
        serializer = UserSerializer
    else:
        serializer = UserSimpleSerializer
    for user in page.object_list:
        data['users'].append(serializer(user).data)

    return GoodResponse(GoodResponseDto(data=data))


@csrf_exempt
def get_users(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = None
    try:
        params.pop('csrfmiddlewaretoken', None)
        params: GetUsersDto = deserialize(parse_param(request), GetUsersDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))

    if params.mode == 'all':
        serializer = UserSerializer
    else:
        serializer = UserSimpleSerializer
    uid_list = params.users

    data = {'users': []}
    for uid in uid_list:
        users = User.objects.filter(uid=uid)
        if not users.exists():
            continue
        data['users'].append(serializer(users.first()).data)
    data['total'] = len(data['users'])
    return GoodResponse(GoodResponseDto(data=data))
