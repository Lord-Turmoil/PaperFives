from django.contrib import admin

from users.models import *

# Register your models here.
admin.site.register(UserAttribute)
admin.site.register(UserStatistics)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(FavoriteUser)
