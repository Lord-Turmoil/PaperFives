# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 23:36
# @Author  : Tony Skywalker
# @File    : tasks.py
#
# Description:
#   For user update tasks.
#
from celery import shared_task
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.dtos.response.users import NotLoggedInDto, PermissionDeniedDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.users.roles import is_user_admin
from shared.utils.users.users import get_user_from_request
from users.models import User
from users.views.utils.stat import update_all_user_statistics


@shared_task
def update_user_statistics_task():
    update_all_user_statistics()


@csrf_exempt
def update_user_statistics(request):
    """
    This is for debug purpose.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())
    if not is_user_admin(user):
        return GoodResponse(PermissionDeniedDto("Not a administrator, you are"))

    update_user_statistics_task.delay()

    return GoodResponse(GoodResponseDto("Update task started!"))
