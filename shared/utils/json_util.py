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

from shared.exceptions.json import JsonSerializeException, JsonDeserializeException


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


def serialize(obj) -> str:
    try:
        return json.dumps(obj, cls=AdvancedEncoder)
    except Exception:
        raise JsonSerializeException("Failed to serialize", obj)


def serialize_as_dict(obj) -> dict:
    if not hasattr(obj, '__dict__'):
        return obj
    ret = obj.__dict__
    for key in obj.__dict__.keys():
        ret[key] = serialize_as_dict(obj.__dict__[key])
    return ret


def _check_type(dict_obj, cls_obj) -> bool:
    if not dict_obj.keys() == cls_obj.__dict__.keys():
        hint = "Attribute set does not match:\n\t"
        hint += f"Expected: {cls_obj.__dict__.keys()}\n\t"
        hint += f"     Got: {dict_obj.keys()}"
        raise AttributeError(hint)

    for key in cls_obj.__dict__.keys():
        cls_type = type(cls_obj.__dict__[key])
        if isinstance(dict_obj[key], cls_type):
            continue

        try:
            if not isinstance(dict_obj[key], dict):
                hint = "Attribute type mismatch:\n\t"
                hint += f"Expected: Attribute '{key}' should be '{type(cls_obj.__dict__[key])}'\n\t"
                hint += f"     Got: '{dict_obj[key]}' of type {type(dict_obj[key])}"
                raise AttributeError(hint)

            _check_type(dict_obj[key], cls_obj.__dict__[key])
        except AttributeError as e:
            raise e
    return True


def _construct_cls(dict_obj, cls):
    model = cls()
    obj = cls()
    for key in model.__dict__.keys():
        if isinstance(dict_obj[key], type(model.__dict__[key])):
            obj.__dict__[key] = dict_obj[key]
            continue
        obj.__dict__[key] = _construct_cls(dict_obj[key], type(model.__dict__[key]))
    return obj


def deserialize(obj, cls=None):
    if isinstance(obj, dict):
        pass
    else:
        try:
            obj = json.loads(obj, cls=AdvancedDecoder)
        except:
            raise JsonDeserializeException("Failed to deserialize", obj)

    if cls is None:
        return obj

    try:
        _check_type(obj, cls())
        obj = _construct_cls(obj, cls)
    except AttributeError as e:
        print(e)
        raise JsonDeserializeException(f"Type mismatch, should be {cls.__name__}", obj)

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
