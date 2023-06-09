# References:
# - https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/
# - https://docs.djangoproject.com/en/4.2/topics/db/examples/one_to_one/
# - https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_many/
#
from django.db import models

from PaperFives.settings import CONFIG
from shared.utils.str_util import is_no_content


# Create your models here.
class UserAttribute(models.Model):
    class Sex(models.IntegerChoices):
        UNKNOWN = 0, "Unknown"
        MALE = 1, "Male"
        FEMALE = 2, "Female"

    sex = models.PositiveSmallIntegerField(choices=Sex.choices, default=Sex.UNKNOWN)
    institute = models.CharField(max_length=127)
    motto = models.CharField(max_length=127)

    @classmethod
    def create(cls, _sex=Sex.UNKNOWN, _institute="", _motto=""):
        return cls(sex=_sex, institute=_institute, motto=_motto)

    class Meta:
        verbose_name = "user_attr"


class UserStatistics(models.Model):
    publish_cnt = models.IntegerField(default=0)
    message_cnt = models.IntegerField(default=0)

    @classmethod
    def create(cls, _publish=0, _message=0):
        return cls(publish_cnt=_publish, message_cnt=_message)

    class Meta:
        verbose_name = "user_stat"


class User(models.Model):
    # primary properties
    uid = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=63)
    username = models.CharField(max_length=63)
    password = models.CharField(max_length=71)

    # extra properties
    avatar = models.CharField(max_length=127)

    # attribute & statistics
    attr = models.OneToOneField(UserAttribute, related_name='user', on_delete=models.CASCADE)
    stat = models.OneToOneField(UserStatistics, related_name='user', on_delete=models.CASCADE)

    # scholar tag
    scholar = models.BooleanField(default=False)

    @classmethod
    def create(cls, _email, _username, _password, _avatar="", _attr=None, _stat=None):
        if is_no_content(_avatar):
            _avatar = CONFIG['DEFAULT_AVATAR']
        if _attr is None:
            _attr = UserAttribute.create()
            _attr.save()
        if _stat is None:
            _stat = UserStatistics.create()
            _stat.save()
        return cls(email=_email, username=_username, password=_password, avatar=_avatar, attr=_attr, stat=_stat)

    class Meta:
        ordering = ['uid']
        verbose_name = 'user'


class Role(models.Model):
    class RoleName(models.IntegerChoices):
        VISITOR = 0, "Visitor"
        USER = 1, "User"
        SCHOLAR = 2, "Scholar"
        ADMIN = 3, "Admin"

    name = models.PositiveSmallIntegerField(choices=RoleName.choices, default=RoleName.VISITOR)
    user = models.ForeignKey(User, related_name='roles', on_delete=models.CASCADE)

    @classmethod
    def create(cls, _name, _user):
        return cls(name=_name, user=_user)

    class Meta:
        verbose_name = 'role'


class FavoriteUser(models.Model):
    # Two fields with the same foreign key seems to cause conflict?
    src_uid = models.BigIntegerField()
    dst_uid = models.BigIntegerField()

    @classmethod
    def create(cls, src, dst):
        """
        Please validate src and dst before you call this!
        """
        return cls(src_uid=src, dst_uid=dst)

    class Meta:
        verbose_name = 'fav_user'


######################################################################
# Hot Statistics
#

class PublishStatistics(models.Model):
    """
    Record user publish count annually.
    """
    uid = models.BigIntegerField()
    year = models.IntegerField()
    lead_cnt = models.IntegerField(default=0)  # as lead-author
    co_cnt = models.IntegerField(default=0)  # as co-author

    @classmethod
    def create(cls, _uid, _year):
        return cls(uid=_uid, year=_year)

    class Meta:
        verbose_name = 'publish_stat'


class AreaPublishStatistics(models.Model):
    """
    Record areas user publishes paper in.
    """
    uid = models.BigIntegerField()
    aid = models.BigIntegerField()
    cnt = models.IntegerField(default=0)

    @classmethod
    def create(cls, _uid, _aid):
        return cls(uid=_uid, aid=_aid)

    class Meta:
        verbose_name = 'area_pub_stat'


class UserRank(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    rank = models.FloatField(default=0.0)

    @classmethod
    def create(cls, _uid, _rank=0.0):
        return cls(uid=_uid, rank=_rank)

    class Meta:
        ordering = ['rank']
        verbose_name = 'user_rank'


class Top20User(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    rank = models.FloatField(default=0.0)

    @classmethod
    def create(cls, _uid, _rank=0.0):
        return cls(uid=_uid, rank=_rank)

    class Meta:
        ordering = ['rank']
        verbose_name = 'top_20_user'
