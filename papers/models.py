from django.db import models
from django.utils import timezone

"""
  When user edits paper, all changes will be saved to DraftPaper table,
and can be modified many times before really publishes.
  When user publishes a paper, it will then be stored to PublishedPaper
table, with the same 'uid' and 'pid', and set to PENDING.
  When a admin reviews paper, he/she will first see a list of papers of
PENDING status, and can select any of them.
  When admin reviews paper, the status of the paper will be set to
REVIEWING and block other admins. When quits, the client must send a
request to set it to PENDING again.
  When a paper passes review, it will be marked PASSED, and will then be
searched.
"""


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
            _publish_date = timezone.datetime.today()
        return cls(title=_title, keywords=_keywords, abstract=_abstract, publish_date=_publish_date)

    class Meta:
        verbose_name = 'paper_attr'


class PaperStatistics(models.Model):
    cites = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    @classmethod
    def create(cls, _cites=0, _downloads=0, _favorites=0, _clicks=0):
        return cls(cites=_cites, downloads=_downloads, favorites=_favorites, clicks=_clicks)

    class Meta:
        verbose_name = 'paper_stat'


class Paper(models.Model):
    class Status(models.IntegerChoices):
        # Only used in DraftPaper
        INCOMPLETE = 0, "Incomplete"
        DRAFT = 1, "Draft"

        # When paper is published, it will first be set to Pending
        PENDING = 2, "Pending"
        REVIEWING = 3, "Reviewing"

        REJECTED = 4, "Rejected"
        PASSED = 5, "Passed"

    pid = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=127, default="")

    status = models.PositiveSmallIntegerField(choices=Status.choices, default=Status.INCOMPLETE)

    # attribute & statistics
    attr = models.OneToOneField(PaperAttribute, related_name="paper", on_delete=models.CASCADE)
    stat = models.OneToOneField(PaperStatistics, related_name="paper", on_delete=models.CASCADE)

    @classmethod
    def create(cls, _path, _attr, _stat=None):
        if _path is None:
            _path = ""
        if _stat is None:
            _stat = PaperStatistics.create()
            _stat.save()
        return cls(path=_path, attr=_attr, stat=_stat)

    class Meta:
        ordering = ['pid']
        verbose_name = 'paper'


class Area(models.Model):
    aid = models.BigAutoField(primary_key=True)
    primary = models.IntegerField()
    secondary = models.IntegerField()
    name = models.CharField(max_length=63)

    papers = models.ManyToManyField(Paper, related_name="areas")

    @classmethod
    def create(cls, _primary, _secondary, _name):
        return cls(primary=_primary, secondary=_secondary, name=_name)

    class Meta:
        verbose_name = "area"


class Author(models.Model):
    email = models.EmailField()  # will be linked to User via email
    name = models.CharField(max_length=63)
    order = models.PositiveSmallIntegerField()  # order in author list

    paper = models.ForeignKey(Paper, related_name="authors", on_delete=models.CASCADE)

    @classmethod
    def create(cls, _paper, _email, _name, _order):
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

    paper = models.ForeignKey(Paper, related_name="references", on_delete=models.CASCADE)

    @classmethod
    def create(cls, _paper, _ref, _link=""):
        return cls(ref=_ref, link=_link, paper=_paper)

    class Meta:
        verbose_name = 'reference'


class FavoritePaper(models.Model):
    uid = models.BigIntegerField()
    pid = models.BigIntegerField()

    @classmethod
    def create(cls, _uid, _pid):
        """
        Please verify parameters before you call this function!
        """
        return cls(uid=_uid, pid=_pid)

    class Meta:
        verbose_name = 'fav_paper'


class PublishRecord(models.Model):
    uid = models.BigIntegerField()
    pid = models.BigIntegerField()
    lead = models.BooleanField()  # whether is lead-author or not

    @classmethod
    def create(cls, _uid, _pid, _lead):
        return cls(uid=_uid, pid=_pid, lead=_lead)

    class Meta:
        verbose_name = 'publish_record'


class PaperUpdateRecord(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    update_time = models.DateTimeField()

    @classmethod
    def create(cls, _pid, _update_time=None):
        if _update_time is None:
            _update_time = timezone.now()
        return cls(pid=_pid, update_time=_update_time)

    class Meta:
        verbose_name = 'update_record'


class PaperReviewRecord(models.Model):
    """
    This is merely a history record.
    """
    pid = models.BigIntegerField()  # paper id
    uid = models.BigIntegerField()  # admin id
    comment = models.TextField(default="")
    status = models.PositiveSmallIntegerField(choices=Paper.Status.choices, default=Paper.Status.REJECTED)

    @classmethod
    def create(cls, _pid, _uid, _status, _comment=""):
        return cls(pid=_pid, uid=_uid, status=_status, comment=_comment)

    class Meta:
        verbose_name = 'paper_review_record'


######################################################################
# Hot Statistics
#

class AreaStatistics(models.Model):
    aid = models.BigIntegerField()
    year = models.IntegerField()
    month = models.IntegerField()
    cnt = models.IntegerField(default=0)

    @classmethod
    def create(cls, _aid, _year, _month):
        return cls(aid=_aid, year=_year, month=_month)

    class Meta:
        verbose_name = 'area_stat'


class PaperRank(models.Model):
    pid = models.BigIntegerField(primary_key=True)
    rank = models.FloatField(default=0.0)

    @classmethod
    def create(cls, _pid, _rank=0.0):
        return cls(pid=_pid, rank=_rank)

    class Meta:
        verbose_name = 'paper_rank'
