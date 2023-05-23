# ------- Litang Save The World! -------
#
# @Time    : 2023/5/23 19:03
# @Author  : Lynx
# @File    : statistic.py
#

# Tip:
# ------ update in DB using method save() ------
def add_paper_clicks(paper):
    paper.attr.clicks += 1
    paper.save()


def add_paper_downloads(paper):
    paper.attr.download += 1
    paper.save()


def add_paper_cites(paper):
    paper.stat.cites += 1
    paper.save()


def add_paper_favorites(paper):
    paper.stat.favorites += 1
    paper.save()
