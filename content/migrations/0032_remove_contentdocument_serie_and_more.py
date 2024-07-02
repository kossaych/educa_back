# Generated by Django 5.0.6 on 2024-07-01 19:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0031_remove_baseuser_username_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentdocument',
            name='serie',
        ),
        migrations.RemoveField(
            model_name='contentdocument',
            name='type',
        ),
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 19, 6, 22, 73392, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 7, 1, 19, 6, 22, 81821, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
    ]