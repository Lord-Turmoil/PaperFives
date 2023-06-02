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

from shared.exceptions.json import JsonSerializeException, JsonDeserializeException
from shared.utils.parser import parse_value


######################################################################
# Serializer Fundamental
#

class AdvancedEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
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
        if not isinstance(src, t):
            hint = f"Value '{src}' type mismatch:\n\t"
            hint += f"Expected: {type(model)}\n\t"
            hint += f"     Got: {type(src)}"
            raise AttributeError(hint)


def _check_type(src, cls):
    __check_type(src, serialize_as_dict(cls()))


BASIC_TYPE_LIST = [int, float, str]


def _is_basic(_type):
    return _type in BASIC_TYPE_LIST

def _construct_cls(src, cls):
    if _is_basic(cls):
        obj = parse_value(src, cls)
        if obj is None:
            raise AttributeError("Not basic type!")
        return obj

    try:
        model = cls()
        obj = cls()
    except TypeError as e:
        raise AttributeError(e)

    for key in model.__dict__.keys():
        t = type(model.__dict__[key])
        if isinstance(src[key], t):
            if issubclass(t, list):
                try:
                    k = type(model.__dict__[key][0])
                except IndexError:
                    raise AttributeError("Missing default value")
                obj.__dict__[key].clear()  # clear default value
                for v in src[key]:
                    obj.__dict__[key].append(_construct_cls(v, k))
                continue
            obj.__dict__[key] = src[key]
            continue
        obj.__dict__[key] = _construct_cls(src[key], type(model.__dict__[key]))
    return obj


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
