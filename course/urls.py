from django.urls import path
from . import views
from .admin import *

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin_site.urls, name='admin')
]