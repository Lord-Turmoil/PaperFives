# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 18:03
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path

from .views import search, upload

urlpatterns = [
    path('search/', search.brief_search),
    path('upload/info', upload.upload_info),
    # path('upload/file', upload.upload_file),
    # path('publish', publish.publish),
    # path('download/info', download.get_info),
    # path('download/file', download.get_file),
]
