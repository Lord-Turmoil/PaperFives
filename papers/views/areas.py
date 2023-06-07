# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/26/2023 16:02
# @Author  : Tony Skywalker
# @File    : areas.py
#
from django.views.decorators.csrf import csrf_exempt

from papers.models import Area, AreaStatistics
from shared.dtos.models.areas import AreaPostDto, AreaPostListDto, AreaGetDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.users import PermissionDeniedDto, NotLoggedInDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.json_util import deserialize
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.users.roles import is_user_admin
from shared.utils.users.users import get_user_from_request
from users.models import AreaPublishStatistics


def _add_area(dto: AreaPostDto):
    if dto.primary < 0 or dto.secondary < 0:
        return "Invalid discipline code"
    dto.name = dto.name.strip()
    if is_no_content(dto.name):
        return "Invalid discipline name"

    areas = Area.objects.filter(primary=dto.primary, secondary=dto.secondary)
    if areas.exists():
        area = areas.first()
        area.name = dto.name
    else:
        area = Area.create(dto.primary, dto.secondary, dto.name)
    area.save()

    return None


def _remove_area(aid):
    aid = parse_value(aid, int)
    if aid is None:
        return "Invalid area id"
    areas = Area.objects.filter(aid=aid)
    if not areas.exists():
        return f"Area of id '{aid}' doesn't exist"

    for area in areas:
        AreaStatistics.objects.filter(aid=area.aid).delete()
        AreaPublishStatistics.objects.filter(aid=area.aid).delete()

    areas.delete()

    return None


@csrf_exempt
def add_areas(request):
    """
    Require administrative permission.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)

    try:
        dto: AreaPostListDto = deserialize(params, AreaPostListDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))

    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())
    if not is_user_admin(user):
        return GoodResponse(PermissionDeniedDto())

    # continue on error
    error_list = []
    i = 0
    for area in dto.areas:
        hint = _add_area(area)
        if hint is not None:
            error_list.append({'no': i, 'hint': hint, 'area': area})
        i += 1
    data = {'errors': error_list}

    return GoodResponse(GoodResponseDto("Areas imported", data=data))


@csrf_exempt
def remove_areas(request):
    """
    Require administrative permission.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)
    id_list: list = params.get('areas', list)
    if id_list is None:
        return BadRequestResponse(BadRequestDto("Missing area list"))

    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())
    if not is_user_admin(user):
        return GoodResponse(PermissionDeniedDto())

    error_list = []
    for aid in id_list:
        hint = _remove_area(aid)
        if hint is not None:
            error_list.append({'id': aid, 'hint': hint})
    data = {'errors': error_list}

    return GoodResponse(GoodResponseDto("Areas deleted", data=data))


@csrf_exempt
def get_areas(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    areas = Area.objects.exclude(secondary=0).order_by('primary', 'secondary')
    data = {'areas': [AreaGetDto().init(area) for area in areas]}

    return GoodResponse(GoodResponseDto(data=data))
