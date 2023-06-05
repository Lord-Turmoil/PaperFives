# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 16:33
# @Author  : Tony Skywalker
# @File    : papers.py
#
# Description:
#   Get papers of a user.
#
import functools

from django.views.decorators.csrf import csrf_exempt

from papers.models import PublishRecord, Paper, PaperRank
from papers.views.utils.serializer import get_paper_get_user_dto
from shared.dtos.models.papers import PaperGetUserDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.users import NoSuchUserDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.papers.papers import get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.users.users import get_user_by_uid, get_user_from_request
from users.models import User


def __cmp_paper_get_user_dto(x: PaperGetUserDto, y: PaperGetUserDto):
    x_date = x.attr.publish_date
    y_date = y.attr.publish_date

    if x_date < y_date:
        return 1
    else:
        return -1


def _get_self_paper_list(uid):
    paper_list = []

    records = PublishRecord.objects.filter(uid=uid)
    for record in records:
        paper = get_paper_by_pid(record.pid)
        if paper is None:
            continue
        dto = get_paper_get_user_dto(paper, record.lead)
        paper_list.append(dto)

    return sorted(paper_list, key=functools.cmp_to_key(__cmp_paper_get_user_dto))


def _get_others_paper_list(uid):
    paper_list = []

    records = PublishRecord.objects.filter(uid=uid)
    for record in records:
        paper: Paper = get_paper_by_pid(record.pid)
        if paper is None:
            continue
        if paper.status != Paper.Status.PASSED:
            continue
        dto = get_paper_get_user_dto(paper, record.lead)
        paper_list.append(dto)

    return sorted(paper_list, key=functools.cmp_to_key(__cmp_paper_get_user_dto))


@csrf_exempt
def get_papers_of_user(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)

    uid = parse_value(params.get('uid'), int)
    if uid is None:
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))
    mode = parse_value(params.get('mode'), str, "min")

    user: User = get_user_by_uid(uid)
    if user is None:
        return GoodResponse(NoSuchUserDto())

    profile: User = get_user_from_request(request)
    if (profile is not None) and (profile.uid == uid):
        paper_list = _get_self_paper_list(uid)
    else:
        paper_list = _get_others_paper_list(uid)
    hot_pid = 0
    max_rank = 0
    for paper in paper_list:
        ranks = PaperRank.objects.filter(pid=paper.pid)
        if not ranks.exists():
            continue
        rank: PaperRank = ranks.first()
        if rank.rank > max_rank:
            max_rank = rank.rank
            hot_pid = paper.pid

    data = {
        'total': len(paper_list),
        'hot': hot_pid,
        'papers': paper_list
    }

    return GoodResponse(GoodResponseDto(data=data))
