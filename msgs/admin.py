from django.contrib import admin

from msgs.models import *

# Register your models here.


admin.site.register(Message)
admin.site.register(TextPayload)
admin.site.register(LinkPayload)
admin.site.register(ImagePayload)
admin.site.register(EmailRecord)
