# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/29/2023 23:13
# @Author  : Tony Skywalker
# @File    : urls.py

from django.urls import path

from .views import areas, papers, users

urlpatterns = [
    path('area/upload', areas.import_areas),
    path('area/clear', areas.clear_areas),
    path('paper/upload', papers.import_paper),
    path('paper/clear', papers.clear_papers),
    path('user/cancel', users.cancel_users),
]
