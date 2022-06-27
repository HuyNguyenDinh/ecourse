from django.db import router
from django.urls import path, re_path, include
from . import views
from .admin import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("course", views.CourseViewSet)
    # /course/ get
    # path('course/', views.CourseViewSet.as_view())
    # /course/ post
    # /course/course_id retrive
    # /course/course_id update
    # /course/course_id delete
router.register("lesson", views.LessonViewSet)
router.register("users", views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin_site.urls, name='admin'),
    path('test/', views.TestView.as_view()), 
    path('welcome/<int:year>', views.welcome, name='welcome'),
    re_path(r'^welcome2/(?P<year>[0-9]{4})/$', views.welcome2, name='welcome2')
]