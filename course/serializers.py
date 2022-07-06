from rest_framework.serializers import  ModelSerializer, SerializerMethodField, ImageField
from django.conf import settings
from .models import *

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "username", "password", "avatar"]
        extra_kwargs = {
            'password': {'write_only': 'true'},
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]

class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "type", "created_date"]

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class LessonSerializer(ModelSerializer):
    action_set = ActionSerializer(many=True)
    tags = TagSerializer(many=True)
    comment_set = CommentSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ["id", "subject", "content", "image", "created_date", "tags", "comment_set", "action_set"]

class PointSerializer(ModelSerializer):
    class Meta:
        model = Point
        fields = "__all__"


class LessonsCourseSerializer(LessonSerializer):
    image = SerializerMethodField()
    def get_image(self, obj):
        request = self.context['request']
        return request.build_absolute_uri('/')[:-1] + obj.image.url
    class Meta:
        model = Lesson
        fields = ["id", "subject", "content", "image", "created_date", "tags", "comment_set", "action_set"]

class CourseViewSerializer(ModelSerializer):
    class Meta:
        model = CourseView
        fields = ["id", "view"]

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    views = CourseViewSerializer()
    ratings = RatingSerializer
    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', 'category', 'ratings', 'views']
