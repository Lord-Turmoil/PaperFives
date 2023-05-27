# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/25/2023 9:13
# @Author  : Tony Skywalker
# @File    : index.py
#
# Description:
#   For Haystack index models.
#

from haystack import indexes

from .models import User


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    # fields to search
    email = indexes.CharField(model_attr='email')
    username = indexes.CharField(model_attr='username')
    institute = indexes.CharField(model_attr='attr__institute')

    def get_model(self):
        return User

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
