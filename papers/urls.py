# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 18:03
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path

from .views import search, upload, cancel, publish

urlpatterns = [
    path('search/', search.brief_search),
    path('upload/info', upload.upload_paper_info),
    path('upload/file', upload.upload_paper_file),
    path('cancel/paper', cancel.cancel_paper),
    path('cancel/file', cancel.cancel_paper_file),
    path('publish', publish.publish_paper),
    # path('download/info', download.get_info),
    # path('download/file', download.get_file),
]
