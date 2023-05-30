# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/29/2023 23:14
# @Author  : Tony Skywalker
# @File    : areas.py
#
from django.views.decorators.csrf import csrf_exempt

from papers.models import Area
from shared.dtos.models.areas import AreaPostListDto, AreaPostDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.users import PermissionDeniedDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import GoodResponse, BadRequestResponse
from shared.utils.json_util import deserialize
from shared.utils.parameter import parse_param
from shared.utils.str_util import is_no_content
from shared.utils.users.users import get_admin_from_request


def _init_area(dto: AreaPostDto):
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


@csrf_exempt
def import_areas(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    params = parse_param(request)
    try:
        dto: AreaPostListDto = deserialize(params, AreaPostListDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))

    # continue on error
    error_list = []
    i = 0
    for area in dto.areas:
        hint = _init_area(area)
        if hint is not None:
            error_list.append({'no': i, 'hint': hint, 'area': area})
        i += 1
    data = {'errors': error_list}

    return GoodResponse(GoodResponseDto("Areas imported", data=data))


@csrf_exempt
def clear_areas(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    Area.objects.all().delete()

    return GoodResponse(GoodResponseDto("All areas removed!"))
