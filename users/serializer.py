# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 15:08
# @Author  : Tony Skywalker
# @File    : serializer.py
#
# Description:
#   For serialization of user related models.
#

from rest_framework import serializers
from users.models import UserAttribute, UserStatistics, User


class UserAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAttribute
        fields = ('sex', 'institute', 'avatar')


class UserStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistics
        fields = ('publish_cnt', 'message_cnt')


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uid', 'email', 'username')


class UserSerializer(serializers.Serializer):
    attr = UserAttributeSerializer()
    stat = UserStatisticsSerializer()

    class Meta:
        model = User
        fields = ('uid', 'email', 'username', 'attr', 'stat')


