# Generated by Django 4.1 on 2022-08-13 10:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0021_alter_token_expired_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(upload_to='upload/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='image',
            field=models.ImageField(upload_to='upload/%Y/%m'),
        ),
        migrations.AlterField(
            model_name='token',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 13, 10, 44, 51, 886158, tzinfo=datetime.timezone.utc)),
        ),
    ]
