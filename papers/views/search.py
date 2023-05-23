# ------- Litang Save The World! -------
#
# @Time    : 2023/5/21 15:44
# @Author  : Lynx
# @File    : search.py
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

from papers.models import Paper, Area, PaperAreaRelation
from papers.views.utils.listing import get_top_clicked_papers
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.parameter import parse_param
from shared.utils.str_util import is_no_content


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

    data = {
        'papers': top_clicked_papers
    }

    return GoodResponse(GoodResponseDto(data=data))


def list_search(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    params = parse_param(request)
    cont = params.get('content')
    area_name = params.get('area')

    if not is_no_content(area_name):
        area_set = Area.objects.filter(name__icontains=area_name)
        paper_set = PaperAreaRelation.objects.filter(area__in=area_set).values('paper')
    else:
        paper_set = Paper.objects.all()

    if not is_no_content(cont):
        term_list = str(cont).split(' ')
        for word in term_list:
            paper_set = paper_set.filter(attr__keywords__icontains=word)

    try:
        ps = params.get('page_size')
        page_size = 20 if is_no_content(ps) else int(ps)
        p = params.get('page_num')
        page_num = 1 if is_no_content(p) else int(p)
    except:
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))

    paginator = Paginator(paper_set, page_size)
    page = paginator.get_page(page_num)

    data = {
        'page_size': page_size,
        'page_num': page.number,
        'total': paginator.num_pages,
        'next': paginator.num_pages > page.number,
        'papers': [
            {
                'title': paper.attr.title,
                'author': [author.name for author in paper.authors],
                'publish_date': paper.attr.publish_date,
                'cites': paper.stat.cites,
                'abstract': paper.attr.abstract,
                'area': [area.name for area in paper.areas],
                'keywords': paper.attr.keywords,
            }
            for paper in page.object_list
        ]
    }

    return GoodResponse(GoodResponseDto(data=data))


def detail(request):
    return
