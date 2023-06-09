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
from shared.utils.parser import parse_value
from shared.utils.users.users import get_user_from_request, get_user_by_uid
from users.models import User, FavoriteUser
from users.serializer import UserSimpleSerializer
from users.views.utils.users import get_users_from_uid_list, is_follower_by_id


@csrf_exempt
def follow_user(request):
    """
    Require login.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    target = params.get('uid')
    if target is None:
        return BadRequestResponse(BadRequestDto("Whom are you going to follow?"))
    if target == user.uid:
        return GoodResponse(FollowSelfErrorDto())
    if not User.objects.filter(uid=target).exists():
        return BadRequestResponse(FollowNothingErrorDto())

    follows = FavoriteUser.objects.filter(src_uid=user.uid, dst_uid=target)
    if follows.exists():
        return GoodResponse(GoodResponseDto("User already followed"))
    follow = FavoriteUser.create(user.uid, target)
    follow.save()

    return GoodResponse(GoodResponseDto("User followed"))


@csrf_exempt
def unfollow_user(request):
    """
    Require login.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))
    user = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    target = parse_value(params.get('uid'), int)
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
    uid = parse_value(params.get('uid'), int)
    if uid is None:
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))

    user = get_user_by_uid(uid)
    if user is None:
        return GoodResponse(NoSuchUserDto())

    # get all followers
    followers = FavoriteUser.objects.filter(dst_uid=user.uid)
    follower_list = get_users_from_uid_list(
        [follower.src_uid for follower in followers],
        UserSimpleSerializer)

    return GoodResponse(UserListDto(follower_list))


@csrf_exempt
def get_followees(request):
    """
    Get the users that the given user follows.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)
    uid = parse_value(params.get('uid'), int)
    if uid is None:
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))

    user = get_user_by_uid(uid)
    if user is None:
        return GoodResponse(NoSuchUserDto())

    # get all followees
    followees = FavoriteUser.objects.filter(src_uid=user.uid)
    followee_list = get_users_from_uid_list(
        [followee.dst_uid for followee in followees],
        UserSimpleSerializer)

    return GoodResponse(UserListDto(followee_list))


@csrf_exempt
def is_follower(request):
    """
    Require login. Is given user a follower of current user or not.
    'given user' follows 'current user'
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    uid = parse_value(params.get('uid'), int)
    if uid is None:
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))

    data = {'value': is_follower_by_id(uid, user.uid)}

    return GoodResponse(GoodResponseDto(data=data))


@csrf_exempt
def is_followee(request):
    """
    Require login. Is current user a follower of given user or not.
    'current user' follows 'given user'
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    user: User = get_user_from_request(request)
    if user is None:
        return GoodResponse(NotLoggedInDto())

    params = parse_param(request)
    uid = parse_value(params.get('uid'), int)
    if uid is None:
        return BadRequestResponse(BadRequestDto("Missing 'uid'"))

    data = {'value': is_follower_by_id(user.uid, uid)}

    return GoodResponse(GoodResponseDto(data=data))
