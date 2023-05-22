# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/16/2023 22:18
# @Author  : Tony Skywalker
# @File    : json_util.py
#
# Description:
#   This util file is a replacement of native support of JSON
# converter in C#. It can be used to convert object to JSON string,
# or a JSON string to a Python object.
#   These functions has passed basic tests, and is guaranteed to
# support datetime and date type, which is used in Django models. :)
#

import datetime
import json
from json import JSONEncoder

from shared.exceptions.json import JsonSerializeException, JsonDeserializeException


class AdvancedEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        return obj.__dict__


def serialize(obj) -> str:
    try:
        return json.dumps(obj, cls=AdvancedEncoder)
    except Exception:
        raise JsonSerializeException("Failed to serialize", obj)


def _check_type(dict_obj, cls_obj) -> bool:
    if not dict_obj.keys() == cls_obj.__dict__.keys():
        raise AttributeError()
    for key in cls_obj.__dict__.keys():
        if isinstance(dict_obj[key], type(cls_obj.__dict__[key])):
            continue
        if not _check_type(dict_obj[key], cls_obj.__dict__[key]):
            raise AttributeError()
    return True


def _construct_cls(dict_obj, cls):
    model = cls()
    obj = cls()
    for key in model.__dict__.keys():
        if isinstance(dict_obj[key], type(model.__dict__[key])):
            obj.__dict__[key] = dict_obj[key]
            continue
        attr = _construct_cls(dict_obj[key], type(model.__dict__[key]))
        if attr is None:
            raise AttributeError()
        obj.__dict__[key] = attr
    return obj


def deserialize(json_str: str, cls=None):
    """
    Deserialize json string to object of specific class
    :param json_str: raw json string
    :param cls: class to convert, if None, will leave json as dict
    :return: object of class cls, or dict
    """
    obj = None
    try:
        obj = json.loads(json_str)
    except Exception:
        raise JsonDeserializeException("Failed to deserialize", json_str)
    if cls is not None:
        try:
            _check_type(obj, cls())
        except AttributeError:
            raise JsonDeserializeException(f"Type mismatch, should be {cls.__name__}", json_str)
    if cls is not None:
        try:
            ret = _construct_cls(obj, cls)
        except AttributeError:
            raise JsonDeserializeException(f"Type mismatch, should be {cls.__name__}", obj)
        return ret
    return obj


def deserialize_dict(dict_obj, cls):
    """
    Deserialize dict object to object of specific class
    """
    dict_obj.pop('csrfmiddlewaretoken', None)
    obj = None
    try:
        _check_type(dict_obj, cls())
        obj = _construct_cls(dict_obj, cls)
    except AttributeError:
        raise JsonDeserializeException(f"Type mismatch, should be {cls.__name__}", dict_obj)

    return obj
