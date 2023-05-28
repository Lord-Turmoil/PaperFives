# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 13:24
# @Author  : Tony Skywalker
# @File    : update.py
#
from django.views.decorators.csrf import csrf_exempt

from papers.tasks import update_area_statistics_task
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.dtos.response.users import NotLoggedInDto, PermissionDeniedDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.users.roles import is_user_admin
from shared.utils.users.users import get_user_from_request
from users.models import User


@csrf_exempt
def update_area_statistics(request):
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

    update_area_statistics_task.delay()

    return GoodResponse(GoodResponseDto("'update_area_statistics_task' started!"))
