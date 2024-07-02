# Generated by Django 4.1.5 on 2024-06-29 09:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0025_alter_codeverification_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 29, 9, 10, 1, 520073, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='contentdocument',
            name='type',
            field=models.CharField(choices=[('serie', 'serie'), ('summary', 'summary'), ('correction', 'correction')], max_length=100),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 29, 9, 10, 1, 535697, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
    ]
