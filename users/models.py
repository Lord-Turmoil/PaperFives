# References:
# - https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_one/
# - https://docs.djangoproject.com/en/4.2/topics/db/examples/one_to_one/
# - https://docs.djangoproject.com/en/4.2/topics/db/examples/many_to_many/
#
import django.conf
from django.db import models

from shared.utils.str_util import is_no_content


# Create your models here.
class UserAttribute(models.Model):
    class Sex(models.IntegerChoices):
        UNKNOWN = 0, "Unknown"
        MALE = 1, "Male"
        FEMALE = 2, "Female"

    sex = models.PositiveSmallIntegerField(choices=Sex.choices, default=Sex.UNKNOWN)
    institute = models.CharField(max_length=127)
    avatar = models.CharField(max_length=127)  # avatar path

    @classmethod
    def create(cls, _sex=Sex.UNKNOWN, _institute="", _avatar=""):
        if is_no_content(_avatar):
            _avatar = django.conf.settings.CONFIG['DEFAULT_AVATAR_PATH']
        return cls(sex=_sex, institute=_institute, avatar=_avatar)

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
    UID_OFFSET = 1000000000

    # primary properties
    uid = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=63)
    username = models.CharField(max_length=63)

    # attribute & statistics
    attr = models.OneToOneField(UserAttribute, related_name='user', on_delete=models.CASCADE)
    stat = models.OneToOneField(UserStatistics, related_name='user', on_delete=models.CASCADE)

    @classmethod
    def create(cls, _email, _username, _attr=None, _stat=None):
        if _attr is None:
            _attr = UserAttribute.create()
        if _stat is None:
            _stat = UserStatistics.create()
        return cls(email=_email, username=_username, _attr=_attr, stat=_stat)

    @classmethod
    def get_external_uid(cls, _uid):
        if _uid < User.UID_OFFSET:
            return _uid + User.UID_OFFSET
        return _uid

    @classmethod
    def get_internal_uid(cls, _uid):
        if _uid < User.UID_OFFSET:
            return _uid
        return _uid - User.UID_OFFSET

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
    src_uid = models.BigIntegerField(primary_key=True)
    dst_uid = models.BigIntegerField()

    @classmethod
    def create(cls, src, dst):
        """
        Please validate src and dst before you call this!
        """
        return cls(src_uid=src, dst_uid=dst)

    class Meta:
        verbose_name = 'fav_user'
