# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 16:14
# @Author  : Tony Skywalker
# @File    : serializer.py
#

from rest_framework import serializers

from papers.models import Author, Reference, Paper, PaperAttribute, PaperStatistics


class PaperAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperAttribute
        fields = ('title', 'keywords', 'abstract', 'publish_date')


class PaperStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaperStatistics
        fields = ('cites', 'downloads', 'favorites')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('email', 'name', 'order')


class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ('ref', 'link')


class PaperSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        field = ('pid', 'path')


class PaperSerializer(serializers.ModelSerializer):
    attr = PaperAttributeSerializer()
    stat = PaperStatisticsSerializer()
    authors = AuthorSerializer(many=True)
    references = ReferenceSerializer(many=True)

    class Meta:
        model = Paper
        field = ('pid', 'path', 'attr', 'stat', 'authors', 'references')
