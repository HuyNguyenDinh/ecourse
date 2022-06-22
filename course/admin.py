from urllib import response
from django.contrib import admin
from django import forms
from django.urls import path
from django.db.models import Count
from django.template.response import TemplateResponse
from ecourse.settings import MEDIA_URL, STATIC_URL
from .models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.

class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)
    class Meta:
        models = Lesson
        fields = '__all__'

class LessonTagInline(admin.TabularInline):
    model = Lesson.tags.through

class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'created_date', 'course']
    search_fields = ['subject', 'created_date', 'course__subject']
    readonly_fields = ['avatar']
    form = LessonForm       #if not use 'form' django will not apply modelform
    inlines = (LessonTagInline, )

    class Media:
        css = {
            'all': ('/static/css/style.css', )
        }
        js = ('/static/js/script.js', )

    def avatar(self, lesson):
        return mark_safe("<img src='{static_u}{img_url}' alt='{alt}' />"\
            .format(static_u=MEDIA_URL,img_url=lesson.image.name, alt=lesson.subject))

class LessonInline(admin.TabularInline):
    model = Lesson
    pk_name = 'course'

class CourseAdmin(admin.ModelAdmin):
    inlines = (LessonInline, )

class CourseAppAdminSite(admin.AdminSite):
    site_header = 'HE THONG QUAN LY KHOA HOC'
    
    def get_urls(self):
        return [
            path('course-stats/', self.course_stats)
        ] + super().get_urls()
    
    def course_stats(self, request):
        course_count = Course.objects.count()
        stats = Course.objects.annotate(lesson_count=Count('lesson_set')).values("id", "subject", "lesson_count")
        
        return TemplateResponse(request=request, template='admin/course-stats.html', context={
            'course_count': course_count,
        })

admin_site = CourseAppAdminSite("mycourse")

# admin.site.register(Category)
# admin.site.register(Course, CourseAdmin)
# admin.site.register(Lesson, LessonAdmin)
# admin.site.register(Tag)
admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, LessonAdmin)
admin_site.register(Tag)