import datetime

from django.db import models


# Create your models here.

class Message(models.Model):
    class MessageType(models.IntegerChoices):
        TEXT = 0, "Text"
        LINK = 1, "Link"
        IMAGE = 2, "Image"

    # this is the payload id of the corresponding type
    # different payload may have the same mid
    mid = models.BigIntegerField(primary_key=True)

    # sender and receiver
    src_uid = models.BigIntegerField()
    dst_uid = models.BigIntegerField()

    # message attribute
    timestamp = models.DateTimeField()
    mtype = models.PositiveSmallIntegerField(choices=MessageType.choices, default=MessageType.TEXT)

    @classmethod
    def create(cls, _src, _dst, _type, _time=None):
        """
        by default, timestamp is the time when object is created
        """
        if _time is None:
            _time = datetime.datetime.now()
        return cls(src_uid=_src, dst_uid=_dst, timestamp=_time, mtype=_type)

    class Meta:
        verbose_name = "message"


class TextPayload(models.Model):
    mid = models.BigAutoField(primary_key=True)
    text = models.TextField()

    @classmethod
    def create(cls, _text):
        return cls(text=_text)

    class Meta:
        verbose_name = "text_payload"


class LinkPayload(models.Model):
    mid = models.BigAutoField(primary_key=True)
    text = models.CharField(max_length=127)
    link = models.CharField(max_length=127)

    @classmethod
    def create(cls, _text, _link):
        return cls(text=_text, link=_link)

    class Meta:
        verbose_name = "link_payload"


class ImagePayload(models.Model):
    mid = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=127)

    @classmethod
    def create(cls, _path):
        return cls(path=_path)

    class Meta:
        verbose_name = "image_payload"


class EmailRecord(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=15)
    expire = models.DateTimeField()
    usage = models.CharField(max_length=15)

    @classmethod
    def create(cls, _email, _code, _expire, _usage):
        return cls(email=_email, code=_code, expire=_expire, usage=_usage)

    class Meta:
        verbose_name = "email"
