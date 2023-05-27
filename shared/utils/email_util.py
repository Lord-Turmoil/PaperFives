# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 10:38
# @Author  : Tony Skywalker
# @File    : email_util.py
#
# Description:
#   Send email...
#

from random import Random

from django.core.mail import EmailMessage
from django.template import loader

from PaperFives.settings import EMAIL_FROM
from shared.exceptions.email import EmailException

CODE_CHARACTER_SET = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'


def generate_code(length=6) -> str:
    code = ""
    max_idx = len(CODE_CHARACTER_SET) - 1
    random = Random()
    for i in range(length):
        code += CODE_CHARACTER_SET[random.randint(0, max_idx)]
    return code


def _send_email(title, template_name, email, dto: dict):
    template = loader.get_template(template_name)
    content = template.render(dto)

    msg = EmailMessage(title, content, EMAIL_FROM, [email])
    msg.content_subtype = 'html'

    try:
        send_status = msg.send()
        if not send_status:
            raise EmailException(send_status['errmsg'])
    except EmailException as e:
        raise e
    except Exception as e:
        raise EmailException(str(e))


def send_code_email(email, code):
    """
    Send code email to target email
    :param email: target email address
    :param code: the code to send
    :return:
    """
    _send_email("PaperFives Verification Email", 'code.html', email, {'code': code})


def send_paper_passed_email(email, dto: dict):
    _send_email('PaperFives: Paper passed', 'paper_passed.html', email, dto)


def send_paper_rejected_email(email, dto: dict):
    _send_email('PaperFives: Paper rejected', 'paper_rejected.html', email, dto)


def send_promotion_email(email, dto: dict):
    _send_email('PaperFives: Promoted', 'promotion.html', email, dto)
