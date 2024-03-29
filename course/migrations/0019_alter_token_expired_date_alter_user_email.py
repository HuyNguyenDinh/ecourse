# Generated by Django 4.0.5 on 2022-08-02 12:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_token_code_alter_token_expired_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 19, 55, 23, 268620)),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
