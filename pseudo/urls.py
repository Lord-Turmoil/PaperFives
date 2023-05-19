from django.urls import path

from .views import *

urlpatterns = [
    path('', sample),
    path('login/', login),
    path('logout/', logout),
    path('register/', register_user),
    path('register-admin/', register_admin),
    path('cancel/', cancel),
    path('profile/', profile),

]
