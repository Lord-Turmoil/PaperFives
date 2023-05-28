# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 15:02
# @Author  : Tony Skywalker
# @File    : hot.py
#
# Descriptions:
#   Hot area, paper, author...
#
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from papers.views.utils.hot_util import get_hot_areas_aux
from shared.dtos.models.areas import AreaGetDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.papers.papers import get_area_by_aid, get_are_cnt_by_aid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value


@csrf_exempt
def get_hot_areas(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)
    year = parse_value(params.get('year'), int, timezone.now().year)
    month = parse_value(params.get('month'), int, timezone.now().month)

    page_size = parse_value(params.get('ps'), int, 20)
    page_num = parse_value(params.get('p'), int, 1)

    areas = get_hot_areas_aux(year, month)

    paginator = Paginator(areas, page_size)
    page = paginator.get_page(page_num)

    data = {
        'ps': page_size,
        'p': page.number,
        'total': areas.count(),
        'next': paginator.num_pages > page.number,
        'areas': []
    }

    for area in areas:
        db_area = get_area_by_aid(area.aid)
        if db_area is None:
            continue
        cnt = get_are_cnt_by_aid(area.aid)
        data['areas'].append({'area': AreaGetDto().init(db_area), 'cnt': cnt})

    return GoodResponse(GoodResponseDto(data=data))