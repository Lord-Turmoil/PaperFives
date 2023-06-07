# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 22:09
# @Author  : Tony Skywalker
# @File    : query.py
#
# Description:
#   Query utility functions. All these functions will return two values,
# the first is result, the second is error hint. One and only one of them
# is None.
import datetime

from haystack.query import SearchQuerySet

from papers.models import Paper
from shared.dtos.models.query import OrdinaryCondList, AdvancedCondList, AdvancedCond, CondAttr
from shared.exceptions.json import JsonDeserializeException
from shared.exceptions.search import SearchErrorException
from shared.utils.json_util import deserialize
from shared.utils.parser import parse_value

SEARCH_MODE = ['and', 'or', 'not']
SEARCH_FIELD = ['all', 'title', 'keywords', 'abstract', 'areas', 'authors']
ORDER_FIELD = {
    'default': 'default',
    'cites': 'cites',
    '-cites': '-cites',
    'downloads': 'downloads',
    '-downloads': '-downloads',
    'clicks': 'clicks',
    '-clicks': '-clicks',
    'favorites': 'favorites',
    '-favorites': '-favorites',
    'date': 'publish_date',
    '-date': '-publish_date'
}

DEFAULT_FUZZY = "1"


def _construct_all(key) -> dict:
    ret = {}
    for field in SEARCH_FIELD:
        if field == 'all':
            continue
        ret[f"{field}__fuzzy"] = key
    return ret


def _construct_search_args(field, key, attr: CondAttr) -> dict:
    args = {}
    if attr is not None:
        if (attr.time_from is not None) and (attr.time_to is not None):
            args['publish_date__range'] = [attr.time_from, attr.time_to]

    if field != 'all':
        args[f"{field}__fuzzy"] = f"{key}"
    else:
        args['content'] = f"{key}~"

    return args


def _search_and(search_set: SearchQuerySet, field, key, attr: CondAttr):
    args = _construct_search_args(field, key, attr)
    results = search_set.filter_and(**args)

    if (attr is not None) and (attr.order != 'default'):
        results = results.order_by(ORDER_FIELD[attr.order])

    return results


def _search_or(search_set: SearchQuerySet, field, key, attr: CondAttr):
    args = _construct_search_args(field, key, attr)
    results = search_set.filter_or(**args)

    if (attr is not None) and (attr.order != 'default'):
        results = results.order_by(ORDER_FIELD[attr.order])

    return results


def _search_not(search_set: SearchQuerySet, field, key, attr: CondAttr):
    args = _construct_search_args(field, key, attr)
    results = search_set.exclude(**args)

    if (attr is not None) and (attr.order != 'default'):
        results = results.order_by(ORDER_FIELD[attr.order])

    return results


SEARCHER = {
    'and': _search_and,
    'or': _search_or,
    'not': _search_not
}


def _search(search_set: SearchQuerySet, mode, field, key, attr: CondAttr):
    if mode not in SEARCH_MODE:
        return None, f"'{mode}' is not a valid search mode"
    if field not in SEARCH_FIELD:
        return None, f"'{field}' is not a valid search field"
    if attr is not None:
        if attr.order not in ORDER_FIELD.keys():
            return None, f"'{attr.order}' is not a valid order option"

    searcher = SEARCHER.get(mode)
    if searcher is None:
        return None, f"Missing searcher for '{mode}'"

    return searcher(search_set, field, key, attr), None


def _get_attr(dto: dict):
    """
    This is not a strict parse, so we don't use json deserializer.
    """
    data: dict = dto.get('attr')
    if data is None:
        return None

    if not isinstance(data, dict):
        return None

    attr = CondAttr()
    attr.order = parse_value(data.get('order'), str, 'default')
    attr.time_from = parse_value(data.get('from'), datetime.date)
    attr.time_to = parse_value(data.get('to'), datetime.date)

    return attr


"""
Ordinary Search:
{
    "attr": {
        "order": "click",
        "time_from": "2022-01-01",
        "time_to": "2023-01-01"
    },
    "cond": {
        "field": "all",
        "key": "algo"
    }
}
"""


def _ordinary_search(search_set, field, key, attr: CondAttr):
    return _search(search_set, 'and', field, key, attr)


def ordinary_search(dto: dict):
    try:
        cond_list: OrdinaryCondList = deserialize({'cond': dto.get('cond')}, OrdinaryCondList)
    except JsonDeserializeException as e:
        raise e

    papers = SearchQuerySet().models(Paper).all()
    attr = _get_attr(dto)
    cond = cond_list.cond

    papers, hint = _ordinary_search(papers, cond.field, cond.key, attr)
    if hint is not None:
        raise SearchErrorException(hint)
    return papers


"""
Advanced Search:
{
    "attr": {
        "order": "click",
        "time_from": "2022-01-01",
        "time_to": "2023-01-01"
    },
    "cond": [
        {
            "mode": "and",
            "fields": "title",
            "key": "algo"
        },
        {
            "mode": "or",
            "fields": "title",
            "key": "algo"
        }
    ]
}
"""


def advanced_search(dto: dict):
    try:
        cond_list: AdvancedCondList = deserialize({'cond': dto.get('cond')}, AdvancedCondList)
    except JsonDeserializeException as e:
        raise e

    papers = SearchQuerySet().models(Paper).all()
    attr = _get_attr(dto)

    cond: AdvancedCond
    for cond in cond_list.cond:
        papers, hint = _search(papers, cond.mode, cond.field, cond.key, attr)
        if hint is not None:
            raise SearchErrorException(hint)

    return papers
