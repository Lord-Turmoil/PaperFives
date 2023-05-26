# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 18:03
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path

from .views import search, upload, cancel, publish, areas, download

urlpatterns = [
    path('search/', search.brief_search),

    path('upload/info', upload.upload_paper_info),
    path('upload/file', upload.upload_paper_file),

    path('download/info', download.download_info),
    path('download/file', download.download_paper),

    path('cancel/paper', cancel.cancel_paper),
    path('cancel/file', cancel.cancel_paper_file),

    path('publish', publish.publish_paper),

    path('areas/add', areas.add_areas),
    path('areas/del', areas.remove_areas),
    path('areas/get', areas.get_areas),
]
