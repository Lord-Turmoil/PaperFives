# ------- Litang Save The World! -------
#
# @Time    : 2023/5/21 15:44
# @Author  : Lynx
# @File    : search.py
from django.views.decorators.csrf import csrf_exempt

from shared.dtos.response.errors import RequestMethodErrorDto
from shared.response.basic import BadRequestResponse
from shared.utils.parameter import parse_param


@csrf_exempt
def search(request):
    return

def detail(request):
    return

def list(request):
    return