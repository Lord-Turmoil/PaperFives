# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/24/2023 10:41
# @Author  : Tony Skywalker
# @File    : papers.py
#
from PaperFives.settings import ERROR_CODE
from shared.dtos.response.base import BaseResponseDto


class NotYourPaperErrorDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['NOT_YOUR_PAPER'], "This is not your paper.")


class NotLeadAuthorErrorDto(BaseResponseDto):
    def __init__(self, msg="You are not the lead author"):
        super().__init__(ERROR_CODE['NOT_LEAD'], msg)


class NoSuchPaperErrorDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['NO_SUCH_PAPER'], "No such paper")


class PaperNotCompleteErrorDto(BaseResponseDto):
    def __init__(self, msg="Paper not complete yet"):
        super().__init__(ERROR_CODE['NOT_COMPLETE'], msg)


class PaperFileMissingErrorDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['FILE_MISSING'], "Paper file missing")
