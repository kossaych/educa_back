# Generated by Django 4.1 on 2024-06-18 14:34

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0011_alter_codeverification_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='correction',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='content.course'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='codeverification',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 18, 14, 34, 24, 338060, tzinfo=datetime.timezone.utc), editable=False),
        ),
        migrations.AlterField(
            model_name='getoffer',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 6, 18, 14, 34, 24, 345067, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'}),
        ),
    ]