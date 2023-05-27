# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/25/2023 9:02
# @Author  : Tony Skywalker
# @File    : publish.py
#
# Description:
#   Publish paper action.
#

from django.views.decorators.csrf import csrf_exempt

from papers.models import PublishRecord, Paper
from papers.views.utils.papers import is_paper_complete
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.dtos.response.papers import NotYourPaperErrorDto, NotLeadAuthorErrorDto, PaperNotCompleteErrorDto, \
    NotPublishableErrorDto
from shared.dtos.response.users import NotLoggedInDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.papers.papers import get_publish_record, get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.users.users import get_user_from_request
from users.models import User

PUBLISHABLE_STATUS = [
    Paper.Status.DRAFT,
]


@csrf_exempt
def publish_paper(request):
    """
    Require login.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    pid = parse_value(params.get('pid'), int)

    record: PublishRecord = get_publish_record(user.uid, pid)
    if record is None:
        return GoodResponse(NotYourPaperErrorDto())
    if not record.lead:
        return GoodResponse(NotLeadAuthorErrorDto("Contact Lead-Author to publish the paper"))

    paper: Paper = get_paper_by_pid(pid)
    if not is_paper_complete(paper):
        return GoodResponse(PaperNotCompleteErrorDto())
    if paper.status not in PUBLISHABLE_STATUS:
        return GoodResponse(NotPublishableErrorDto())

    paper.status = Paper.Status.PENDING
    paper.save()

    return GoodResponse(GoodResponseDto("We have received your paper!"))
