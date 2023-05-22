# ------- Litang Save The World! -------
#
# @Time    : 2023/5/22 8:39
# @Author  : Lynx
# @File    : listing.py
from papers.models import Paper, PaperAreaRelation


def get_top_clicked_papers(listnum: int = 20):
    top_clicked_papers_set = Paper.objects.all().order_by('-stat__clicks')[:listnum]
    top_clicked_papers_dict = []
    for i in top_clicked_papers_set:
        area_list = PaperAreaRelation.objects.filter(paper=i).values('area__name')
        top_clicked_papers_dict.append({
            'title': i.attr.title,
            'abstract': i.attr.abstract,
            'areas': [area['area__name'] for area in area_list]
        })
    return top_clicked_papers_dict
