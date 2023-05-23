# ------- Litang Save The World! -------
#
# @Time    : 2023/5/21 14:31
# @Author  : Lynx
# @File    : papers.py
#
from shared.dtos.models.base import BaseDto


class PaperAttrDto(BaseDto):
    def __init__(self):
        self.title: str = ""
        self.abstract: str = ""
        self.area_name: str = ""

class PaperDto:
    def __init__(self):
        self.pid: int = 0 # is that appropriate?
        self.path: str = ""

class AuthorDto:
    def __init__(self):
        self.email: str = ""
        self.name: str = ""
        self.order: int = 0