from rest_framework.serializers import  ModelSerializer
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

class ResetPasswordSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email"]
        extra_kwargs = {
            'id': {'read_only': 'true'},
        }

class TokenSerializer(ModelSerializer):
    user = ResetPasswordSerializer
    class Meta:
        model = Token
        fields = ["code", "user"]

class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name"]

class ActionSerializer(ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "type", "created_date"]

class CommentSerializer(ModelSerializer):
    creator = UserSerializer()
    class Meta:
        model = Comment
        fields = "__all__"

class LessonSerializer(ModelSerializer):
    tags = TagSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ["id", "subject", "content", "image", "created_date", "updated_date", "tags", "comment_count", "action_count"]

class PointSerializer(ModelSerializer):
    class Meta:
        model = Point
        fields = "__all__"


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
    class Meta:
        model = Course
        fields = ['id', 'subject', 'image', 'created_date', "updated_date", 'category', 'views', 'average_rating']

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]