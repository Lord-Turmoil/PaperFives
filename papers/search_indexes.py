# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 21:02
# @Author  : Tony Skywalker
# @File    : search_indexes.py
#

from haystack import indexes

from papers.models import Paper


class PaperIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True)

    # fields to search
    pid = indexes.IntegerField(model_attr='pid')

    status = indexes.IntegerField(model_attr='status')
    title = indexes.CharField(model_attr='attr__title')
    keywords = indexes.CharField(model_attr='attr__keywords')
    abstract = indexes.CharField(model_attr='attr__abstract')

    # special fields
    authors = indexes.CharField()
    areas = indexes.CharField()

    def prepare_authors(self, obj):
        return ', '.join(author.name for author in obj.authors.all())

    def prepare_areas(self, obj: Paper):
        return ', '.join(area.name for area in obj.areas.all())

    def get_model(self):
        return Paper

    def index_queryset(self, using=None):
        """
        Default query set will only contain PASSED papers.
        """
        return self.get_model().objects.all().filter(status=Paper.Status.PASSED)