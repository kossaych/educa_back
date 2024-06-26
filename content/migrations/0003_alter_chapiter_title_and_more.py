# Generated by Django 4.1 on 2024-03-26 11:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_alter_codeverification_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapiter',
            name='title',
            field=models.CharField(error_messages={'blank': 'The title cannot be left blank.', 'null': 'The title cannot be null.'}, max_length=200),
        ),
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 26, 11, 34, 46, 834590, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 3, 26, 11, 34, 46, 850217, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
    ]
