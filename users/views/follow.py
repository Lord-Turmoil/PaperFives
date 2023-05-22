# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/20/2023 12:04
# @Author  : Tony Skywalker
# @File    : favorite.py
#
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.users import NotLoggedInDto, NoSuchUserDto, FollowSelfErrorDto, FollowNothingErrorDto, \
    UserListDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.parameter import parse_param
from shared.utils.users.users import get_user_from_request
from users.models import User, FavoriteUser


@csrf_exempt
def follow_user(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    uid = request.session.get('uid')
    if uid is None:
        return GoodResponse(NotLoggedInDto())
    users = User.objects.filter(uid=uid)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()

    params = parse_param(request)
    target = params.get('uid')
    if target is None:
        return BadRequestResponse(BadRequestDto("Whom are you going to follow?"))
    if target == uid:
        return GoodResponse(FollowSelfErrorDto())
    if not User.objects.filter(uid=target).exists():
        return BadRequestResponse(FollowNothingErrorDto())

    follows = FavoriteUser.objects.filter(src_uid=uid, dst_uid=target)
    if follows.exists():
        return GoodResponse(GoodResponseDto("User already followed"))
    follow = FavoriteUser.create(uid, target)
    follow.save()

    return GoodResponse(GoodResponseDto("User followed"))


@csrf_exempt
def unfollow_user(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    target = params.get('uid')
    if target is None:
        return BadRequestResponse(BadRequestDto("Whom are you going to unfollow?"))
    if target == user.uid:
        return GoodResponse(FollowSelfErrorDto())
    # No need to check this in unfollow?
    # if not User.objects.filter(uid=target).exists():
    #     return BadRequestResponse(FollowNothingErrorDto())

    follows = FavoriteUser.objects.filter(src_uid=user.uid, dst_uid=target)
    if not follows.exists():
        return GoodResponse(GoodResponseDto("User already unfollowed"))
    follows.delete()

    return GoodResponse(GoodResponseDto("User unfollowed"))


@csrf_exempt
def get_followers(request):
    """
    Get users that follows the given user.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    params = parse_param(request)
    uid = params.get('uid')
    if uid is None or not isinstance(uid, int):
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))

    users = User.objects.filter(uid=uid)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()

    # get all followers
    followers = FavoriteUser.objects.filter(dst_uid=user.uid)
    follower_list = [follower.src_uid for follower in followers]

    return GoodResponse(UserListDto(follower_list))


@csrf_exempt
def get_followees(request):
    """
    Get the users that the given user follows.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)
    uid = params.get('uid')
    if uid is None or not isinstance(uid, int):
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))

    users = User.objects.filter(uid=uid)
    if not users.exists():
        return GoodResponse(NoSuchUserDto())
    user = users.first()

    # get all followees
    followees = FavoriteUser.objects.filter(src_uid=user.uid)
    followee_list = [followee.dst_uid for followee in followees]

    return GoodResponse(UserListDto(followee_list))
