import datetime

from django.db import models
from typing import List


# Create your models here.

class PaperAttribute(models.Model):
    title = models.CharField(max_length=127)
    keywords = models.CharField(max_length=127)
    abstract = models.TextField()

    publish_date = models.DateField()

    @classmethod
    def create(cls, _title, _keywords, _abstract, _publish_date=None):
        """
        If _publish_date is None, it implies that the paper is published
        on creation.
        """
        if _publish_date is None:
            _publish_date = datetime.date.today()
        return cls(title=_title, keywords=_keywords, abstract=_abstract, publish_date=_publish_date)

    class Meta:
        verbose_name = 'paper_attr'


class PaperStatistics(models.Model):
    cites = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)

    @classmethod
    def create(cls, _cites=0, _downloads=0, _favorites=0):
        return cls(cites=_cites, downloads=_downloads, favorites=_favorites)

    class Meta:
        verbose_name = 'paper_stat'


class Paper(models.Model):
    PID_OFFSET = 1000000000

    pid = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=127)

    # attribute & statistics
    attr = models.OneToOneField(PaperAttribute, on_delete=models.CASCADE)
    stat = models.OneToOneField(PaperStatistics, on_delete=models.CASCADE)

    @classmethod
    def create(cls, _path, _attr, _stat=None):
        if _stat is None:
            _stat = PaperStatistics.create()
        return cls(path=_path, attr=_attr, stat=_stat)

    class Meta:
        ordering = ['pid']
        verbose_name = 'paper'


class Author(models.Model):
    email = models.EmailField()  # will be linked to User via email
    name = models.CharField(max_length=63)
    order = models.PositiveSmallIntegerField()  # order in author list

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    @classmethod
    def create(cls, _email, _name, _order, _paper):
        """
        Please verify parameters before you call this function!
        _order is the display order in the author list
        """
        return cls(email=_email, name=_name, order=_order, paper=_paper)

    class Meta:
        verbose_name = 'author'


class Reference(models.Model):
    ref = models.CharField(max_length=255)  # reference text
    link = models.CharField(max_length=255)  # reference link if possible

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    @classmethod
    def create(cls, _paper, _ref, _link=""):
        return cls(ref=_ref, link=_link, paper=_paper)

    class Meta:
        verbose_name = 'reference'


class FavoritePaper(models.Model):
    uid = models.BigIntegerField(primary_key=True)
    pid = models.BigIntegerField()

    @classmethod
    def create(cls, _uid, _pid):
        """
        Please verify parameters before you call this function!
        """
        return cls(uid=_uid, pid=_pid)

    class Meta:
        verbose_name = 'fav_paper'
