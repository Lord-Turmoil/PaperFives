from django.db import models


# Create your models here.

class PaperAttribute(models.Model):
    title = models.CharField(max_length=127)
    keyword = models.CharField(max_length=127)
    abstract = models.TextField()

    publish_date = models.DateField()

    class Meta:
        verbose_name = 'paper_attr'

class PaperStatistics(models.Model):
    cites = models.IntegerField(default=0)
    downloads = models.IntegerField(default=0)
    favorites = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'paper_stat'


class Author(models.Model):
    uid = models.IntegerField(default=None, null=True)  # null if user not registered
    name = models.CharField(max_length=63)
    order = models.PositiveSmallIntegerField()  # order in author list

    class Meta:
        verbose_name = 'author'


class Paper(models.Model):
    PID_OFFSET = 1000000000

    pid = models.BigAutoField(primary_key=True)
    path = models.CharField(max_length=127)

    # attribute & statistics
    attr = models.OneToOneField(PaperAttribute, on_delete=models.CASCADE)
    stat = models.OneToOneField(PaperStatistics, on_delete=models.CASCADE)

    # author
    authors = models.ForeignKey(Author, on_delete=models.CASCADE)

    class Meta:
        ordering = 'pid'
        verbose_name = 'paper'


class Reference(models.Model):
    ref = models.CharField(max_length=255)  # reference text
    link = models.CharField(max_length=255)  # reference link if possible

    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'reference'


class FavoritePaper(models.Model):
    uid = models.BigIntegerField()
    pid = models.BigIntegerField()

    class Meta:
        verbose_name = 'fav_paper'