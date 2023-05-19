from django.urls import path
from .views import *

urlpatterns = [
    path('', sample),
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('profile/', profile)
]
