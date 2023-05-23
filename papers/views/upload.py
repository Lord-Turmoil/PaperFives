# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/23/2023 14:49
# @Author  : Tony Skywalker
# @File    : upload.py
#
#
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.models.papers import PaperPostDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.json_util import deserialize
from shared.utils.parameter import parse_param


@csrf_exempt
def upload_info(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)

    dto: PaperPostDto
    try:
        dto = deserialize(params, PaperPostDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))
    if not dto.is_valid():
        return BadRequestResponse(BadRequestDto("invalid data value"))

    return GoodResponse(GoodResponseDto())
