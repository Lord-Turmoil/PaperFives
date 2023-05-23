# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 18:03
# @Author  : Tony Skywalker
# @File    : urls.py
#

from django.urls import path

from .views import search

urlpatterns = [
    path('search/', search.brief_search),
    # path('edit/upload/info/', edit.upload.upload_info),
    # path('edit/upload/file/', edit.upload.upload_file),
    # path('edit/publish/', edit.publish.publish),
    # path('download/info', download.get_info),
    # path('download/file', download.get_file),
]
