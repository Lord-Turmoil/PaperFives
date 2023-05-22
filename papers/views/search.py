# ------- Litang Save The World! -------
#
# @Time    : 2023/5/21 15:44
# @Author  : Lynx
# @File    : search.py
from django.views.decorators.csrf import csrf_exempt

from papers.views.utils.listing import get_top_clicked_papers
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.parameter import parse_param


@csrf_exempt
def brief_search(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    params = parse_param(request)
    listnum = params.get('listnum')
    if listnum is not None:
        top_clicked_papers = get_top_clicked_papers(listnum)
    else:
        top_clicked_papers = get_top_clicked_papers()

    return GoodResponse(GoodResponseDto(data=top_clicked_papers))

def detail(request):
    return

def list(request):
    return