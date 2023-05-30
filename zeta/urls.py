# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/29/2023 23:13
# @Author  : Tony Skywalker
# @File    : urls.py

from django.urls import path

from .views import areas

urlpatterns = [
    path('area', areas.init_areas),
]
