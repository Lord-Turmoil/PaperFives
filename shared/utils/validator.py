# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 17:46
# @Author  : Tony Skywalker
# @File    : validator.py
#
# Description:
#   For data validations.
#
import re

VALID_IMAGE_FILE_EXT = ['.jpg', '.jpeg', '.png']


def validate_image_name(filename: str) -> bool:
    for ext in VALID_IMAGE_FILE_EXT:
        if filename.endswith(ext):
            return True
    return False


def validate_pdf_name(filename: str) -> bool:
    return filename.endswith('.pdf')


def validate_email(email: str) -> bool:
    if re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', email):
        return True
    return False


def validate_password(password: str) -> bool:
    if re.match('^[a-zA-Z0-9_]{6,16}$', password):
        return True
    return False
