from xmlrpc.client import ResponseError
from django import views
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status, generics, views
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
from .paginators import *
from ecourse import settings
from .perms import *
from django.db.models import F

# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, ]
    def get_permissions(self):
        if self.action in ["current_user", "get_courses_of_user"]:
            return [permissions.IsAuthenticated(), ]
        else:
            return [permissions.AllowAny(), ]

    @action(methods=['get'], detail=False, url_path='current-user')
    def current_user(self, request):
        return Response(self.serializer_class(request.user).data, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=True, url_path='courses')
    def get_courses_of_user(self, request, pk):
        courses = User.objects.get(pk=pk).students
        if courses:
            return Response(CourseSerializer(courses, many=True).data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

class AuthInfo(views.APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = CourseSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        courses = Course.objects.filter(active=True)

        search = self.request.query_params.get("search")
        if search is not None:
            courses = courses.filter(subject__icontains=search)

        cate_id = self.request.query_params.get('category_id')
        if cate_id is not None:
            courses = courses.filter(category_id=cate_id)

        return courses

    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        course = Course.objects.get(pk=pk).lessons
        search = request.query_params.get('search')

        lessons = course.filter(active=True)
        if search:
            lessons = lessons.filter(subject__icontains=search)
        return Response(LessonsCourseSerializer(lessons, context={'request': self.request}, many=True).data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=True, url_path='register')
    def register_course(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            user = request.user
            course.students.add(user)
            course.save()
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(status=status.HTTP_202_ACCEPTED)

    @action(methods=['get'], detail=True, url_path='students')
    def get_students(self, request, pk):
            students = Course.objects.get(pk=pk).students
            if students:
                return Response(UserSerializer(students, many=True).data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='rating')
    def course_rating(self, request, pk):
        point = request.data.get("point")
        if point:
            try:
                r = Rating.objects.create(point=point, course=self.get_object(), user=request.user)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(RatingSerializer(r).data,status=status.HTTP_201_CREATED)

    # @action(methods=['get'], detail=True, url_path='get-ratings')
    # def get_course_rating(self, request, pk):
    #     try:
    #         course = self.get_object()
    #         course_ratings = Rating.objects.filter(course=course)
    #         if not course_ratings:
    #             raise ValueError
    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response(RatingSerializer(course_ratings, many=True).data, status=status.HTTP_200_OK)
   

    @action(methods=['get'], detail=True, url_path='view')
    def course_views(self, request, pk):
        course = self.get_object()
        v, created = CourseView.objects.get_or_create(course=course)
        v.view = F('view') + 1
        v.save()
        v.refresh_from_db()
        return Response(CourseViewSerializer(v).data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action == "course_views":
            return [permissions.AllowAny(), ]
        elif self.action in ["update", "get_students"]:
            return [MentorPermission(), ]
        elif self.action == ["create"]:
            return [permissions.IsAdminUser(), ]
        elif self.action in ["list", "retrieve", "course_rating"]:
            return [permissions.AllowAny(), ]
        else:
            return [permissions.IsAuthenticated(), ]


class LessonViewSet(viewsets.ViewSet, generics.ListCreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            return [MentorPermission(), ]
        else:
            return [permissions.IsAuthenticated(), ]

    @action(methods=['post'], detail=True, url_path="hide-lesson", url_name="hide-lesson")
    def hide_lesson(self, request, pk):
        try:
            l = Lesson.objects.get(pk=pk)
            l.active = False
            l.save()
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(data=LessonSerializer(l, context={'request': request}).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True, url_path="add-comment", url_name="add-comment")
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content, lesson=self.get_object(), creator=request.user)
            
            return Response(CommentSerializer(c).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=["get"], detail=True, url_path="get-comments", url_name="get-comments")
    # def get_comments(self, request, pk):
    #     try:
    #         lesson = self.get_object()
    #         c = Comment.objects.filter(lesson=lesson)
    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response(CommentSerializer(c, many=True).data, status=status.HTTP_200_OK)
    
    @action(methods=['post'], detail=True, url_path="like")
    def take_action(self, request, pk):
        try:
            action_type = int(request.data.get('type'))
            action = Action.objects.create(type=action_type, lesson=self.get_object(), creator=request.user)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(ActionSerializer(action).data, status=status.HTTP_201_CREATED)

    # @action(methods=["get"], detail=True, url_path="get-actions", url_name="get-actions")
    # def get_actions(self, request, pk):
    #     try:
    #         lesson = self.get_object()
    #         a = Action.objects.filter(lesson=lesson)
    #     except:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
    #     else:
    #         return Response(ActionSerializer(a, many=True).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().partial_update(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().creator:
            return super().destroy(request, *args, **kwargs)
        return Response(status=status.HTTP_403_FORBIDDEN)