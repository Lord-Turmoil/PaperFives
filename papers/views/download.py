# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/25/2023 9:03
# @Author  : Tony Skywalker
# @File    : download.py
#
# Description:
#   Download actions.
#
from django.views.decorators.csrf import csrf_exempt

from papers.models import Paper
from papers.views.utils.serialize import get_paper_get_dto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto, PageNotFoundErrorDto
from shared.dtos.response.papers import NoSuchPaperErrorDto, PaperFileMissingErrorDto
from shared.dtos.response.users import NotLoggedInDto
from shared.response.basic import BadRequestResponse, GoodResponse, PageNotFoundResponse
from shared.response.papers import PdfFileResponse
from shared.utils.papers.papers import get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.users.users import get_user_from_request
from users.models import User


@csrf_exempt
def download_info(request):
    """
    No login require.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)
    pid = parse_value(params.get('id'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing 'pid'"))

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    dto = get_paper_get_dto(paper)

    return GoodResponse(GoodResponseDto(dto=dto))


@csrf_exempt
def download_paper(request):
    """
    Require login.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    pid = parse_value(params.get('id'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing 'pid'"))

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    # it shouldn't be, but in case
    if is_no_content(paper.path):
        return GoodResponse(PaperFileMissingErrorDto())

    try:
        file = open(paper.path, 'rb')
    except:
        return PageNotFoundResponse(PageNotFoundErrorDto("This is not the paper you're looking for"))

    return PdfFileResponse(file)
