# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 11:59
# @Author  : Tony Skywalker
# @File    : review.py
#
# Description:
#   For review actions.
#
from celery import shared_task

from papers.models import Paper
from shared.exceptions.email import EmailException
from shared.utils.email_util import send_paper_passed_email, send_paper_rejected_email, send_promotion_email
from shared.utils.users.users import get_user_by_email
from users.models import User, Role


@shared_task
def _send_pass_task(email, dto: dict):
    """
    {
        'name': author name,
        'paper': paper title,
        'comment': optional
    }
    """
    try:
        send_paper_passed_email(email, dto)
    except EmailException:
        return


@shared_task
def _send_rejected_task(email, dto: dict):
    """
    {
        'name': author name,
        'paper': paper title,
        'comment': required
    }
    """
    try:
        send_paper_rejected_email(email, dto)
    except EmailException:
        return


@shared_task
def _send_promotion_task(email, dto: dict):
    """
    {
        "name": name
    }
    """
    try:
        send_promotion_email(email, dto)
    except EmailException:
        return


def pass_paper(paper: Paper, comment=None):
    paper.status = paper.Status.PASSED
    paper.save()

    user_list = []
    for author in paper.authors.all():
        user: User = get_user_by_email(author.email)
        if user is not None:
            user_list.append(user)
        if comment is not None:
            _send_pass_task.delay(author.email, {'name': author.name, 'paper': paper.attr.title, 'comment': comment})
        else:
            _send_pass_task.delay(author.email, {'name': author.name, 'paper': paper.attr.title})

    for user in user_list:
        user.stat.publish_cnt += 1
        user.stat.save()
        if user.scholar:
            continue
        _send_promotion_task.delay(user.email, {'name': user.username})
        user.scholar = True
        user.save()

        role = Role.create(Role.RoleName.SCHOLAR, user)
        role.save()


def reject_paper(paper: Paper, comment):
    paper.status = Paper.Status.REJECTED
    paper.save()

    for author in paper.authors.all():
        _send_rejected_task.delay(author.email, {'name': author.name, 'paper': paper.attr.title, 'comment': comment})
