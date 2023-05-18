# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 16:29
# @Author  : Tony Skywalker
# @File    : test.py
#

from http import HTTPStatus

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from django import forms

from shared.dtos.error import RequestMethodErrorDto, BadRequestDto
from shared.dtos.user import CreateUserFailedDto, CreateUserSucceededDto, UserDto
from shared.exceptions.json import JsonException
from shared.utils.json_util import deserialize, serialize
from users.models import User, UserAttribute
from users.serializer import UserSerializer


@csrf_exempt
def get_user_all(request):
    if request.method != 'GET':
        return Response(RequestMethodErrorDto('GET', request.method), HTTPStatus.BAD_REQUEST)
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    data = {'model': serializer.data, 'raw': serialize(users)}
    return Response(data, HTTPStatus.OK)


@csrf_exempt
def get_user_by_id(request):
    if request.method != 'GET':
        return Response(RequestMethodErrorDto('GET', request.method), HTTPStatus.BAD_REQUEST)

    users = User.objects.filter(uid=request.POST.get('uid'))
    if not users.exists():
        return Response("No such user", HTTPStatus.OK)
    user = users.first()
    return Response(deserialize(user), HTTPStatus.OK)


@csrf_exempt
def put_user(request):
    request
    if request.method != 'POST':
        return HttpResponse(serialize(RequestMethodErrorDto('PUT', request.method)))

    try:
        user_dto = deserialize(request.body, UserDto)
    except JsonException as e:
        print(e)
        return HttpResponse(serialize(BadRequestDto("Bad")), HTTPStatus.BAD_REQUEST)

    print(user_dto)

    return HttpResponse(serialize(CreateUserSucceededDto()))
