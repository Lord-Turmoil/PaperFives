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
from json import JSONDecodeError

from django.utils import timezone

from shared.exceptions.json import JsonSerializeException, JsonDeserializeException


######################################################################
# Serializer Fundamental
#

class AdvancedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.astimezone(datetime.timezone(datetime.timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        return obj.__dict__


def object_hook(obj):
    for key, value in obj.items():
        if isinstance(value, str):
            try:
                obj[key] = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pass
            else:
                continue
            try:
                obj[key] = datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                pass
            else:
                continue
    return obj


class AdvancedDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=object_hook)


######################################################################
# Serializer
#

def serialize(obj) -> str:
    try:
        return json.dumps(obj, cls=AdvancedEncoder)
    except TypeError:
        raise JsonSerializeException("Failed to serialize", obj)


def serialize_as_dict(obj):
    return deserialize(serialize(obj))


######################################################################
# Deserializer
#

# Utility functions

def __check_type_dict(src, model):
    if not isinstance(src, dict):
        hint = f"Type mismatch, '{src}' should be 'dict'"
        raise AttributeError(hint)

    if not src.keys() == model.keys():
        hint = "Attribute set does not match:\n\t"
        hint += f"Expected: {model.keys()}\n\t"
        hint += f"     Got: {src.keys()}"
        raise AttributeError(hint)

    for key in model.keys():
        __check_type(src[key], model[key])


def __check_type_list(src, model):
    if not isinstance(src, list):
        hint = f"Type mismatch, '{src}' should be 'list'"
        raise AttributeError(hint)
    try:
        m = model[0]
    except IndexError:
        raise AttributeError(f"Missing default value for '{src}'")
    for v in src:
        __check_type(v, m)


def __check_type(src, model):
    t = type(model)
    if issubclass(t, dict):
        __check_type_dict(src, model)
    elif issubclass(t, list):
        __check_type_list(src, model)
    else:
        # So ugly
        if not isinstance(src, t) and not isinstance(model, datetime.date):
            hint = f"Value '{src}' type mismatch:\n\t"
            hint += f"Expected: {type(model)}\n\t"
            hint += f"     Got: {type(src)}"
            raise AttributeError(hint)


def _check_type(src, cls):
    __check_type(src, serialize_as_dict(cls()))


def __construct_cls(src, cls, model):
    if issubclass(cls, list):
        if not isinstance(src, list):
            return None
        obj = []
        try:
            _type = type(model[0])
        except IndexError:
            raise AttributeError(f"Missing default value for '{cls}'")
        for v in src:
            obj.append(__construct_cls(v, _type, model[0]))
    elif isinstance(src, cls):
        obj = src
    else:
        if not isinstance(src, dict):
            return None
        obj = cls()
        for (k, v) in model.__dict__.items():
            obj.__dict__[k] = __construct_cls(src.get(k), type(v), v)

    return obj


def _construct_cls(src, cls):
    try:
        return __construct_cls(src, cls, cls())
    except Exception as e:
        raise AttributeError(f"Unexpected error: '{e}'")


def deserialize(obj, cls=None):
    if isinstance(obj, dict):
        dict_obj = obj
    else:
        try:
            dict_obj = json.loads(obj, cls=AdvancedDecoder)
        except JSONDecodeError as e:
            raise JsonDeserializeException(f"Failed to deserialize!\n\t{e}", obj)

    if cls is None:
        return dict_obj

    try:
        _check_type(dict_obj, cls)
        obj = _construct_cls(dict_obj, cls)
    except AttributeError as e:
        raise JsonDeserializeException(f"Type mismatch, should be {cls.__name__}\n\t{e}", obj)

    return obj
