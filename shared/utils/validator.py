# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 17:46
# @Author  : Tony Skywalker
# @File    : validator.py
#
# Description:
#   For data validations.
#

VALID_IMAGE_FILE_EXT = ['.jpg', '.jpeg', '.png']


def validate_image_name(filename: str):
    for ext in VALID_IMAGE_FILE_EXT:
        if filename.endswith(ext):
            return True
    return False
