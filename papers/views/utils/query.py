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
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet

from papers.models import Paper
from shared.dtos.models.query import OrdinaryCondList, AdvancedCondList, AdvancedCond
from shared.exceptions.json import JsonDeserializeException
from shared.exceptions.search import SearchErrorException
from shared.utils.json_util import deserialize

SEARCH_MODE = ['and', 'or', 'not']
SEARCH_FIELD = ['all', 'title', 'keywords', 'abstract', 'areas', 'authors']

DEFAULT_FUZZY = "1"

def _construct_all(key) -> dict:
    ret = {}
    for field in SEARCH_FIELD:
        if field == 'all':
            continue
        ret[f"{field}__fuzzy"] = key
    return ret


def _search_and(search_set: SearchQuerySet, field, key):
    if field != 'all':
        args = {f"{field}__fuzzy": f"{key}"}
        return search_set.filter_and(**args)
    else:
        return search_set.filter(content=f"{key}")


def _search_or(search_set: SearchQuerySet, field, key):
    if field != 'all':
        args = {f"{field}__fuzzy": f"{key}"}
        return search_set.filter_or(**args)
    else:
        return search_set.filter(cnontet=f"{key}")


def _search_not(search_set: SearchQuerySet, field, key):
    if field != 'all':
        args = {f"{field}": key}
        return search_set.exclude(**args)
    else:
        return search_set.exclude(content__all=key)


SEARCHER = {
    'and': _search_and,
    'or': _search_or,
    'not': _search_not
}


def _search(search_set: SearchQuerySet, mode, field, key):
    if mode not in SEARCH_MODE:
        return None, f"'{mode}' is invalid"
    if field not in SEARCH_FIELD:
        return None, f"'{field}' is invalid"

    searcher = SEARCHER.get(mode)
    if searcher is None:
        return None, f"Missing searcher for '{mode}'"

    return searcher(search_set, field, key), None


"""
Ordinary Search:
{
    "ps": 20,
    "p": 1,
    "advanced": false,
    "cond": {
        "field": "all",
        "key": "algo"
    }
}
"""


def _ordinary_search(search_set, field, key):
    return _search(search_set, 'and', field, key)


def ordinary_search(dto: dict):
    try:
        cond_list: OrdinaryCondList = deserialize(dto, OrdinaryCondList)
    except JsonDeserializeException as e:
        return None, str(e)
    cond = cond_list.cond
    papers = SearchQuerySet().models(Paper).all()
    papers, hint = _ordinary_search(papers, cond.field, cond.key)
    if hint is not None:
        raise SearchErrorException(hint)
    return papers


"""
Advanced Search:
{
    "ps": 20,
    "p": 1,
    "advanced": true,
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
        cond_list: AdvancedCondList = deserialize(dto, AdvancedCondList)
    except JsonDeserializeException as e:
        raise e

    papers = SearchQuerySet().models(Paper).all()
    cond: AdvancedCond
    for cond in cond_list.cond:
        papers, hint = _search(papers, cond.mode, cond.field, cond.key)
        if hint is not None:
            raise SearchErrorException(hint)

    return papers
