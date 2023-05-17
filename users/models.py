from django.db import models


# Create your models here.
class UserAttribute(models.Model):
    class Sex(models.IntegerChoices):
        UNKNOWN = 0, "Unknown"
        MALE = 1, "Male"
        FEMALE = 2, "Female"

    sex = models.PositiveSmallIntegerField(choices=Sex.choices, default=Sex.UNKNOWN)
    institute = models.CharField(max_length=127)
    avatar = models.CharField(max_length=127)  # avatar path

    class Meta:
        verbose_name = "user_attr"


class UserStatistics(models.Model):
    publish_cnt = models.IntegerField(default=0)
    message_cnt = models.IntegerField(default=0)

    class Meta:
        verbose_name = "user_stat"


class User(models.Model):
    UID_OFFSET = 1000000000

    # primary properties
    uid = models.BigAutoField(primary_key=True)
    email = models.EmailField(max_length=63)
    username = models.CharField(max_length=63)

    # attribute & statistics
    attr = models.OneToOneField(UserAttribute, on_delete=models.CASCADE)
    stat = models.OneToOneField(UserStatistics, on_delete=models.CASCADE)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['rid']
        verbose_name = 'role'


class FavoriteUser(models.Model):
    # Two fields with the same foreign key seems to cause conflict?
    src_uid = models.BigIntegerField()
    dst_uid = models.BigIntegerField()

    class Meta:
        verbose_name = 'fav_user'
