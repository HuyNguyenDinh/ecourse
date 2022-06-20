from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='upload/%Y/%m')

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
    
class Course(ItemBase):

    class Meta:
        unique_together = ('subject', 'category')
        ordering = ["subject", "created_date"]
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

class Lesson(ItemBase):

    class Meta:
        unique_together = ('subject', 'course')
    content = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    tags = models.ManyToManyField('Tag', blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
