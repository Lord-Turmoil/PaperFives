from django.urls import path
from .views import *

urlpatterns = [
    path('', sample),
    path('login/', login),
    path('register/', register)
]
