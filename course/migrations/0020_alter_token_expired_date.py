# Generated by Django 4.0.5 on 2022-08-02 17:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0019_alter_token_expired_date_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expired_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 2, 17, 48, 2, 670270, tzinfo=utc)),
        ),
    ]