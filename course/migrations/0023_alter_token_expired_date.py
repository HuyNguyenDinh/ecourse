# Generated by Django 4.1 on 2022-08-13 10:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0022_alter_course_image_alter_lesson_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 13, 10, 54, 16, 16917, tzinfo=datetime.timezone.utc)),
        ),
    ]
