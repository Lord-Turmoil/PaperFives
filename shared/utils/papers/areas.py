# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/30/2023 15:45
# @Author  : Tony Skywalker
# @File    : areas.py
#
from papers.models import Area


def get_area_by_aid(aid):
    areas = Area.objects.filter(aid=aid)
    if areas.exists():
        return areas.first()
    return None


def get_area_by_code(primary, secondary):
    areas = Area.objects.filter(primary=primary, secondary=secondary)
    if areas.exists():
        return areas.first()
    return None


def get_area_by_name(name: str):
    areas = Area.objects.filter(name=name)
    if not areas.exists():
        return None
    return areas.first()


def get_full_area_by_name(name: str):
    """
    Return itself and its parent subject.
    """
    sub = get_area_by_name(name)
    if sub is None:
        return None, None

    if sub.secondary == 0:  # also a primary
        return sub, sub

    sup = get_area_by_code(sub.primary, 0)
    # sup may be None
    return sub, sup
