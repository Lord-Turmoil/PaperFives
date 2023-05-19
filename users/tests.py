from django.test import TestCase
from django.utils import timezone

from msgs.models import EmailRecord
from shared.utils.token import generate_token, verify_token


# Create your tests here.

class TokenTestCase(TestCase):
    def test_token(self):
        identity = "demo"
        token = generate_token(identity)
        t1 = token[1:]
        t2 = "this is not even a token"
        self.assertTrue(verify_token(identity, token), "0: should be true")
        self.assertFalse(verify_token(identity, t1), "1: should be false")
        self.assertFalse(verify_token(identity, t2), "2: should be false")


class PassTestCase(TestCase):
    def test_pass(self):
        if True:
            pass
        print("hello there")


class DateTimeTestCase(TestCase):
    def test_time(self):
        emails = EmailRecord.objects.all()
        if not emails.exists():
            print('Bad')
        else:
            email = emails.first()
            if timezone.now() > email.expire:
                print('Yes')
            else:
                print('No')
