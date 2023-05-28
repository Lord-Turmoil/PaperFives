# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 10:46
# @Author  : Tony Skywalker
# @File    : review.py
#
# Description:
#   For paper review. All api here require administrative permission.
#
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from papers.models import Paper, PaperReviewRecord
from papers.views.utils.review import pass_paper, reject_paper
from papers.views.utils.serializer import get_paper_get_simple_dto, get_paper_get_dto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.papers import NoSuchPaperErrorDto, NotReviewableErrorDto, NotConfirmableErrorDto
from shared.dtos.response.users import NotLoggedInDto, PermissionDeniedDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.papers.papers import get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.users.roles import is_user_admin
from shared.utils.users.users import get_user_from_request
from users.models import User

REVIEWABLE_STATUS = [
    Paper.Status.PENDING,
    Paper.Status.PASSED,
]


@csrf_exempt
def get_pending_papers(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())
    if not is_user_admin(user):
        return GoodResponse(PermissionDeniedDto("Not a administrator, you are"))

    params = parse_param(request)
    page_size = parse_value(params.get('ps', 20), int)
    page_num = parse_value(params.get('p', 1), int)
    if (page_size is None) or (page_num is None) or (page_size < 1) or (page_num < 1):
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))

    papers = Paper.objects.filter(status=Paper.Status.PENDING)
    paginator = Paginator(papers, page_size)
    page = paginator.get_page(page_num)

    data = {
        'ps': page_size,
        'p': page.number,
        'total': papers.count(),
        'next': paginator.num_pages > page.number,
        'papers': []
    }

    for paper in page.object_list:
        data['papers'].append(get_paper_get_simple_dto(paper))

    return GoodResponse(GoodResponseDto(data=data))


@csrf_exempt
def get_review_paper(request):
    """
    Get one paper to review. This will set the paper status to REVIEWING, and with
    extra checks. Won't add paper clicks.
    If review action aborted, must call release review paper to set it back to PENDING.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())
    if not is_user_admin(user):
        return GoodResponse(PermissionDeniedDto("Not a administrator, you are"))

    params = parse_param(request)
    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing 'pid'"))

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    if paper.status == Paper.Status.REVIEWING:
        return GoodResponse(NotReviewableErrorDto("Already reviewed by another administrator"))
    if paper.status not in REVIEWABLE_STATUS:
        return GoodResponse(NotReviewableErrorDto())

    paper.status = Paper.Status.REVIEWING
    paper.save()

    return GoodResponse(GoodResponseDto(data=get_paper_get_dto(paper)))


@csrf_exempt
def release_review_paper(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())
    if not is_user_admin(user):
        return GoodResponse(PermissionDeniedDto("Not a administrator, you are"))

    params = parse_param(request)
    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing 'pid'"))

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    paper.status = Paper.Status.PENDING
    paper.save()

    return GoodResponse(GoodResponseDto("Paper status reset to PENDING"))


CONFIRMABLE_STATUS = [
    Paper.Status.REVIEWING,
]


@csrf_exempt
def review_paper(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())
    if not is_user_admin(user):
        return GoodResponse(PermissionDeniedDto("Not a administrator, you are"))

    params = parse_param(request)
    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing 'pid'"))
    passed = parse_value(params.get('status'), bool)
    comment: str = parse_value(params.get('comment'), str)
    if passed is None:
        return BadRequestResponse(BadRequestDto("Missing paper status"))

    if comment is not None:
        comment = comment.strip()

    if not passed:
        if comment is None or is_no_content(comment):
            return BadRequestResponse(BadRequestDto("Comment is required to reject paper"))

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    if paper.status not in CONFIRMABLE_STATUS:
        return GoodResponse(NotConfirmableErrorDto())

    if passed:
        pass_paper(paper, comment)
    else:
        reject_paper(paper, comment)

    record = PaperReviewRecord.create(paper.pid, user.uid, passed, comment)
    record.save()

    return GoodResponse(GoodResponseDto("Review complete"))
