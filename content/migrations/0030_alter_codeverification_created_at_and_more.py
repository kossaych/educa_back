# Generated by Django 5.0.6 on 2024-07-01 09:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0029_baseuser_username_alter_codeverification_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 9, 5, 0, 861037, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 7, 1, 9, 5, 0, 868624, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
    ]
