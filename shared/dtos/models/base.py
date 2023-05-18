# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 14:43
# @Author  : Tony Skywalker
# @File    : base.py
#
from shared.utils.str_util import is_no_content


class BaseDto:
    def is_valid_base(self) -> bool:
        for key in self.__dict__.keys():
            if is_no_content(self.__dict__[key]):
                return False
        return True

    def is_valid(self) -> bool:
        return self.is_valid_base()
