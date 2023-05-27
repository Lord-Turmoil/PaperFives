# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/26/2023 23:10
# @Author  : Tony Skywalker
# @File    : papers.py
#
from django.http import FileResponse


class PdfFileResponse(FileResponse):
    def __init__(self, file, filename=None):
        if filename is None:
            super().__init__(file, content_type='application/pdf')
        else:
            super().__init__(file, content_type='application/pdf', filename=filename)
