# ------- Litang Save The World! -------
#
# @Time    : 2023/5/22 8:39
# @Author  : Lynx
# @File    : listing.py
from papers.models import Paper


def get_top_clicked_papers(listnum: int = 20):
    top_clicked_papers_set = Paper.objects.all().order_by('-stat__clicks')[:listnum]
    top_clicked_papers_dict = []
    for i in top_clicked_papers_set:
        top_clicked_papers_dict.append({
            'title': i.attr.title,
            'abstract': i.attr.abstract,
            'areas': [area.name for area in i.areas]
        })
    return top_clicked_papers_dict
