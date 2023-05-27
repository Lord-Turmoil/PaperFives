# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/24/2023 13:21
# @Author  : Tony Skywalker
# @File    : cancel.py
#
# Description:
#   Cancel paper. Remove all information about a paper.
#

from django.views.decorators.csrf import csrf_exempt

from papers.models import Paper, PublishRecord
from papers.views.utils.papers import delete_paper_file, update_paper_update_record, delete_whole_paper
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.papers import NoSuchPaperErrorDto, NotYourPaperErrorDto, NotLeadAuthorErrorDto
from shared.dtos.response.users import NotLoggedInDto
from shared.response.basic import BadRequestResponse, GoodResponse, NotAuthorizedResponse
from shared.utils.papers.papers import get_paper_by_pid, get_publish_record
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.users.roles import is_user_admin
from shared.utils.users.users import get_user_from_request
from users.models import User


@csrf_exempt
def cancel_paper(request):
    """
    Login required.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)

    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Invalid pid"))

    user: User = get_user_from_request(request)
    if user is None:
        return NotAuthorizedResponse(NotLoggedInDto())

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    if not is_user_admin(user):
        r: PublishRecord = get_publish_record(user.uid, paper.pid)
        if r is None:
            return GoodResponse(NotYourPaperErrorDto())
        if not r.lead:
            return GoodResponse(NotLeadAuthorErrorDto("Contact Lead-Author to delete the paper."))

    # now, the paper can be deleted
    delete_whole_paper(paper)

    return GoodResponse(GoodResponseDto("Gone too soon~"))


@csrf_exempt
def cancel_paper_file(request):
    """
    Login required. Only cancel paper file.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)

    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Invalid pid"))
    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    user: User = get_user_from_request(request)
    if user is None:
        return NotAuthorizedResponse(NotLoggedInDto())
    if not is_user_admin(user):
        r: PublishRecord = get_publish_record(user.uid, paper.pid)
        if r is None:
            return GoodResponse(NotYourPaperErrorDto())
        if not r.lead:
            return GoodResponse(NotLeadAuthorErrorDto("Contact Lead-Author to delete the paper."))

    # now, the paper can be deleted
    if not is_no_content(paper.path):
        delete_paper_file(paper)
        paper.path = ""
        paper.save()
    else:
        return GoodResponse(GoodResponseDto("Paper already deleted"))

    update_paper_update_record(paper)

    return GoodResponse(GoodResponseDto("Looking forward to your update."))
