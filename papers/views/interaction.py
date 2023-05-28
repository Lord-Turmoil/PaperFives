# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/25/2023 9:04
# @Author  : Tony Skywalker
# @File    : interaction.py
#
# Description:
#   User interaction with paper. Such as favorite, cite.
#
from django.views.decorators.csrf import csrf_exempt

from papers.models import Paper, FavoritePaper
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.papers import NoSuchPaperErrorDto
from shared.dtos.response.users import NotLoggedInDto
from shared.response.basic import BadRequestResponse, GoodResponse, NotAuthorizedResponse
from shared.utils.papers.papers import get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.users.users import get_user_from_request
from users.models import User


@csrf_exempt
def favorite_paper(request):
    """
    Login should be checked in middleware.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)

    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing pid"))

    user: User = get_user_from_request(request)
    if user is None:
        return NotAuthorizedResponse(NotLoggedInDto())

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    favorites = FavoritePaper.objects.filter(uid=user.uid, pid=paper.pid)
    if favorites.exists():
        return GoodResponse(GoodResponseDto("Already in your favorites"))
    favorite = FavoritePaper.create(user.uid, paper.pid)
    favorite.save()

    paper.stat.favorites += 1
    paper.stat.save()

    return GoodResponse(GoodResponseDto("Paper in your pocket!"))


@csrf_exempt
def unfavorite_paper(request):
    """
    Login should be checked in middleware.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)

    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing pid"))

    user: User = get_user_from_request(request)
    if user is None:
        return NotAuthorizedResponse(NotLoggedInDto())

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    favorites = FavoritePaper.objects.filter(uid=user.uid, pid=paper.pid)
    if not favorites.exists():
        return GoodResponse(GoodResponseDto("Already out of your favorites"))
    favorites.delete()

    paper.stat.favorites -= 1
    if paper.stat.favorites < 0:
        paper.stat.favorites = 0
    paper.stat.save()

    return GoodResponse(GoodResponseDto("Paper out of your pocket!"))


@csrf_exempt
def cite_paper(request):
    """
    No need to login.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)

    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing pid"))

    # anyone can cite
    # user: User = get_user_from_request(request)
    # if user is None:
    #     return NotAuthorizedResponse(NotLoggedInDto())

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    names = ', '.join(author.name for author in paper.authors.all())
    title = paper.attr.title
    publish_date = paper.attr.publish_date.strftime("%Y")

    cite = '[1] ' + '. '.join([names, title, publish_date])
    data = {'cite': cite}

    paper.stat.cites += 1
    paper.stat.save()

    return GoodResponse(GoodResponseDto(data=data))
