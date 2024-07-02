# Generated by Django 4.1.5 on 2024-06-29 07:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0017_alter_codeverification_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentdocument',
            name='serie',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='content.contentdocument', unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 29, 7, 57, 45, 32768, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 29, 7, 57, 45, 37046, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
    ]
