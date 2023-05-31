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

    # 2023/05/30
    # Field that wants to support fuzzy search must be EdgeNgramField!!!
    title = indexes.EdgeNgramField(model_attr='attr__title')
    keywords = indexes.EdgeNgramField(model_attr='attr__keywords')
    abstract = indexes.EdgeNgramField(model_attr='attr__abstract')

    # order fields
    publish_date = indexes.DateField(model_attr='attr__publish_date')
    cites = indexes.IntegerField(model_attr='stat__cites', indexed=True)
    downloads = indexes.IntegerField(model_attr='stat__downloads', indexed=True)
    favorites = indexes.IntegerField(model_attr='stat__favorites', indexed=True)
    clicks = indexes.IntegerField(model_attr='stat__clicks', indexed=True)

    # special fields
    authors = indexes.EdgeNgramField()
    areas = indexes.EdgeNgramField()

    def prepare_authors(self, obj):
        return ' '.join(author.name for author in obj.authors.all())

    def prepare_areas(self, obj):
        return ' '.join(area.name for area in obj.areas.all())

    def get_model(self):
        return Paper

    def index_queryset(self, using=None):
        """
        Default query set will only contain PASSED papers.
        """
        return self.get_model().objects.all().filter(status=Paper.Status.PASSED)
