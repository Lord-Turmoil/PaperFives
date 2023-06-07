# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 18:03
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path

from .views import search, upload, cancel, publish, areas, download, review, update, hot, interaction, papers

urlpatterns = [
    path('upload/info', upload.upload_paper_info),
    path('upload/file', upload.upload_paper_file),

    path('download/info', download.download_info),
    path('download/file', download.download_paper),

    path('cancel/paper', cancel.cancel_paper),
    path('cancel/file', cancel.cancel_paper_file),

    path('publish', publish.publish_paper),

    path('action/favorite', interaction.favorite_paper),
    path('action/unfavorite', interaction.unfavorite_paper),
    path('action/cite', interaction.cite_paper),
    path('action/isfavorite', interaction.is_favorite_paper),

    path('areas/add', areas.add_areas),
    path('areas/del', areas.remove_areas),
    path('areas/get', areas.get_areas),

    path('review/pending', review.get_pending_papers),
    path('review/get', review.get_review_paper),
    path('review/release', review.release_review_paper),
    path('review/review', review.review_paper),

    path('search/temp/all', search.temp_get_pid_list),
    path('search/query', search.query_paper),
    path('search/areas', search.query_area),

    path('hot/areas', hot.get_hot_areas),
    path('hot/papers', hot.get_hot_papers),

    path('get/papers', papers.get_papers_of_user),
    path('get/favorite', interaction.get_favorite_paper),

    path('task/update_stat', update.update_paper_statistics),
]
