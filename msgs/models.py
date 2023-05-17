from django.db import models


# Create your models here.

class Message(models.Model):
    class MessageType(models.IntegerChoices):
        TEXT = 0, "Text"
        LINK = 1, "Link"
        IMAGE = 2, "Image"

    mid = models.BigAutoField(primary_key=True)

    # sender and receiver
    src_uid = models.BigIntegerField()
    dst_uid = models.BigIntegerField()

    # message attribute
    timestamp = models.DateTimeField()
    mtype = models.PositiveSmallIntegerField(choices=MessageType.choices, default=MessageType.TEXT)

    # get payload based on mtype

    class Meta:
        verbose_name = "message"


class TextPayload(models.Model):
    mid = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.TextField()

    class Meta:
        verbose_name = "text_payload"


class LinkPayload(models.Model):
    mid = models.ForeignKey(Message, on_delete=models.CASCADE)
    text = models.CharField(max_length=127)
    link = models.CharField(max_length=127)

    class Meta:
        verbose_name = "link_payload"


class ImagePayload(models.Model):
    mid = models.ForeignKey(Message, on_delete=models.CASCADE)
    path = models.CharField(max_length=127)

    class Meta:
        verbose_name = "image_payload"
