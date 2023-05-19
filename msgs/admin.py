from django.contrib import admin

from msgs.models import *
from papers.models import *
from users.models import *

# Register your models here.

admin.site.register(UserAttribute)
admin.site.register(UserStatistics)
admin.site.register(User)
admin.site.register(FavoriteUser)

admin.site.register(PaperAttribute)
admin.site.register(PaperStatistics)
admin.site.register(Paper)
admin.site.register(Author)
admin.site.register(Reference)
admin.site.register(FavoritePaper)

admin.site.register(Message)
admin.site.register(TextPayload)
admin.site.register(LinkPayload)
admin.site.register(ImagePayload)
