# Generated by Django 4.1 on 2024-06-18 14:31

import content.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0010_remove_baseuser_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 18, 14, 31, 13, 823624, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 18, 14, 31, 13, 839247, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
        migrations.CreateModel(
            name='Correction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=content.models.upload_document_to)),
                ('serie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.contentdocument')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
