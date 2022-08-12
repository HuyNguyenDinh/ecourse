from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from ckeditor.fields import RichTextField
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_mentor = models.BooleanField(default=False, null=False)
    avatar = models.ImageField(upload_to='upload/%Y/%m')

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    expired_date = models.DateTimeField(default = timezone.now() + timezone.timedelta(minutes=30))

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100 ,null=False, unique=True)
    def __str__(self):
        return self.name

class ItemBase(models.Model):

    class Meta:
        abstract = True
    
    subject = models.CharField(max_length=100, null=False)
    image = models.ImageField(upload_to='courses/%Y/%m', default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.subject
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='rating_of_course_of_user'
            )
        ]

class ActionBase(models.Model):
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Action(ActionBase):
    LIKE, HAHA, HEART = range(3)
    ACTIONS = [
        (LIKE, 'like'),
        (HAHA, 'haha'),
        (HEART, 'heart')
    ]
    type = models.PositiveSmallIntegerField(choices=ACTIONS, default=LIKE)
    
    class Meta:
        constraints = [models.UniqueConstraint(
                fields=['lesson', 'creator'],
                name='action_of_creator_of_lesson'
            )
        ]

class Comment(ActionBase):
    content = models.TextField()

    def __str__(self):
        return self.content

class CourseView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    view = models.IntegerField(default=0)
    course = models.OneToOneField('Course', on_delete=models.CASCADE, related_name="views")

class Course(ItemBase):

    class Meta:
        unique_together = ('subject', 'category')
        ordering = ["-created_date"]
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    students = models.ManyToManyField(User, related_name="students")
    ratings = models.ManyToManyField(User, through='Rating', related_name='ratings')

    @property
    def average_rating(self):
        return Rating.objects.filter(course=self).aggregate(models.Avg('rating')).get('rating__avg')

class Lesson(ItemBase):
    content = RichTextField()
    courses = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", unique=False)
    tags = models.ManyToManyField('Tag', null=True, blank=True)
    points = models.ManyToManyField(User, through='Point', related_name='points')
    class Meta:
        ordering = ["created_date"]
        constraints = [
            models.UniqueConstraint(
                fields=['subject', 'courses'],
                name='lesson_of_course'
            )
        ]
    comments = models.ManyToManyField(User, through='Comment', related_name='comments')
    actions = models.ManyToManyField(User, through="Action", related_name="actions")

    @property
    def comment_count(self):
        return Comment.objects.filter(lesson=self).aggregate(models.Count('id')).get("id__count")

    @property
    def action_count(self):
        return Action.objects.filter(lesson=self).aggregate(models.Count('id')).get("id__count")


class Point(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    point = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'lesson'],
                name='point_of_lesson_of_user'
            )
        ]

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


