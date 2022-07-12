from django.db import router
from django.urls import path, re_path, include
from . import views
from .admin import *
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

router = DefaultRouter()
router.register("course", views.CourseViewSet)
router.register("lesson", views.LessonViewSet)
router.register("users", views.UserViewSet)
router.register("comment", views.CommentViewSet)
router.register("category", views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls, name='admin'),
    path('oauth2-info/', views.AuthInfo.as_view()),
]