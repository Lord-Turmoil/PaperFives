# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/23/2023 14:49
# @Author  : Tony Skywalker
# @File    : upload.py
#
#
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from papers.models import PaperAttribute, Paper, Author, Area, Reference, PublishRecord, PaperUpdateRecord
from papers.views.utils.serialize import get_paper_post_dto, get_paper_get_dto
from shared.dtos.models.papers import PaperPostDto, PaperGetDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.papers import NotYourPaperErrorDto, NotLeadAuthorErrorDto, NoSuchPaperErrorDto
from shared.dtos.response.users import NotLoggedInDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.json_util import deserialize
from shared.utils.papers.papers import get_publish_record, get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.str_util import is_no_content
from shared.utils.users.users import get_user_from_request, get_user_by_email
from users.models import User


def _get_new_paper(user, dto):
    # self.pid:
    # self.attr: PaperAttrData = PaperAttrData()
    # self.authors: List[PaperAuthorData] = [PaperAuthorData()]
    # self.areas: List[int] = [0]
    # self.refs: List[PaperRefData] = [PaperRefData()]

    # Create properties
    attr = PaperAttribute.create(dto.attr.title, ', '.join(dto.attr.keywords), dto.attr.abstract, dto.attr.publish_date)
    attr.save()
    paper = Paper.create(None, attr)
    paper.save()

    return paper, None


def _get_old_paper(user, dto):
    record: PublishRecord = get_publish_record(user.uid, dto.pid)
    if record is None:
        return None, GoodResponse(NotYourPaperErrorDto())
    if not record.lead:
        return None, GoodResponse(NotLeadAuthorErrorDto("Contact Lead-Author to modify the paper"))

    paper: Paper = get_paper_by_pid(record.pid)
    if paper is None:
        return None, GoodResponse(NoSuchPaperErrorDto())

    paper.attr.title = dto.attr.title
    paper.attr.keywords = ', '.join(dto.attr.keywords)
    paper.attr.abstract = dto.attr.abstract
    paper.attr.publish_date = dto.attr.publish_date
    paper.attr.save()

    return paper, None


def _update_paper(user: User, paper: Paper, dto: PaperPostDto):
    """
    For now, a clumsy way is used, that is... deleting all old records...
    """

    # update authors
    for author in paper.authors.all():
        u: User = get_user_by_email(author.email)
        if u is None:
            continue
        PublishRecord.objects.filter(uid=u.uid, pid=paper.pid).delete()
    paper.authors.all().delete()  # bad...
    for v in dto.authors:
        author = Author.create(paper, v.email, v.name, v.order)
        author.save()
        u = get_user_by_email(v.email)
        if u is not None:
            r = PublishRecord.create(_uid=u.uid, _pid=paper.pid, _lead=(u.uid == user.uid))
            r.save()

    # update references
    paper.references.all().delete()  # so bad...
    for v in dto.refs:
        ref = Reference.create(paper, v.text, v.link)
        ref.save()

    # update areas
    paper.areas.clear()  # won't delete areas
    areas = Area.objects.filter(aid__in=dto.areas)
    for v in areas:
        paper.areas.add(v)

    # update status
    if not get_paper_post_dto(paper).is_complete() or is_no_content(paper.path):
        paper.status = paper.Status.INCOMPLETE
    else:
        paper.status = paper.Status.DRAFT

    # save paper
    paper.save()

    # update paper update time
    papers = PaperUpdateRecord.objects.filter(pid=paper.pid)
    if papers.exists():
        p: PaperUpdateRecord = papers.first()
        p.update_time = timezone.now()
        p.save()
    else:
        p: PaperUpdateRecord = PaperUpdateRecord.create(paper.pid)
        p.save()


@csrf_exempt
def upload_info(request):
    """
    Login status should be checked by middleware.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)

    dto: PaperPostDto
    try:
        dto = deserialize(params, PaperPostDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))
    if not dto.is_valid():
        return BadRequestResponse(BadRequestDto("Invalid data value"))

    if dto.pid < 0:
        return BadRequestDto(BadRequestDto("Invalid paper pid"))

    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    # Get new paper, or old paper to modify
    if dto.pid == 0:
        paper, response = _get_new_paper(user, dto)
    else:
        paper, response = _get_old_paper(user, dto)
    if response is not None:
        return response

    # update paper
    _update_paper(user, paper, dto)

    return GoodResponse(GoodResponseDto(data=get_paper_get_dto(paper)))
