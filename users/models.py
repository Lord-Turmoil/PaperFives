from django.db import models


# Create your models here.

class User(models.Model):
    class Sex(models.IntegerChoices):
        UNKNOWN = 0, "Unknown"
        MALE = 1, "Male"
        FEMALE = 2, "Female"

    # primary properties
    uid = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=63)
    username = models.CharField(max_length=63)

    # extra properties
    sex = models.PositiveSmallIntegerField(choices=Sex.choices, default=Sex.UNKNOWN)
    publish_cnt = models.IntegerField(default=0)
    message_cnt = models.IntegerField(default=0)
    institute = models.CharField(max_length=127)
    avatar = models.CharField(max_length=127)

    class Meta:
        ordering = ['uid']
        verbose_name = 'user'


class Role(models.Model):
    rid = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=7)

    class Meta:
        ordering = ['rid']
        verbose_name = 'role'


class RoleRecord(models.Model):
    rid = models.ForeignKey(Role, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'role_record'


class FavoriteUser(models.Model):
    # Two fields with the same foreign key seems to cause conflict?
    src_uid = models.BigIntegerField()
    dst_uid = models.BigIntegerField()

    class Meta:
        verbose_name = 'fav_user'
