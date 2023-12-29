# Generated by Django 4.2.4 on 2023-12-29 18:30

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_serie_students_complete_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 29, 18, 30, 56, 285180, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 29, 18, 30, 56, 288179, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
        migrations.AlterField(
            model_name='serie',
            name='students_complete_content',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'student'}, null=True, related_name='completed_series', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='video',
            name='students_complete_content',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'student'}, null=True, related_name='completed_videos', to=settings.AUTH_USER_MODEL),
        ),
    ]
