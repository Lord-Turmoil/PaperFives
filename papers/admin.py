from django.contrib import admin

from papers.models import *

# Register your models here.

admin.site.register(PaperAttribute)
admin.site.register(PaperStatistics)
admin.site.register(Paper)
admin.site.register(Area)
admin.site.register(Author)
admin.site.register(Reference)
admin.site.register(FavoritePaper)
admin.site.register(PublishRecord)
admin.site.register(PaperUpdateRecord)
