# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/25/2023 9:13
# @Author  : Tony Skywalker
# @File    : search_indexes.py
#
# Description:
#   For Haystack index models.
#

from haystack import indexes

from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    # fields to search
    email = indexes.EdgeNgramField(model_attr='email')
    username = indexes.EdgeNgramField(model_attr='username')
    institute = indexes.EdgeNgramField(model_attr='attr__institute')

    # accompany fields, it doesn't seem to work?
    # uid = indexes.IntegerField(model_attr='uid', index_fieldname=None)
    # avatar = indexes.CharField(model_attr='avatar', index_fieldname=None)
    # scholar = indexes.BooleanField(model_attr='scholar', index_fieldname=None)
    #
    # sex = indexes.IntegerField(model_attr='attr__sex', index_fieldname=None)
    # motto = indexes.CharField(model_attr='attr__motto', index_fieldname=None)
    #
    # publish_cnt = indexes.IntegerField(model_attr='attr__publish_cnt', index_fieldname=None)
    # message_cnt = indexes.IntegerField(model_attr='attr__message_cnt', index_fieldname=None)

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
