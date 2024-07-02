# Generated by Django 4.2.4 on 2024-02-16 10:24

import content.models
import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_resized.forms


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(error_messages={'blank': 'please write your phone number', 'invalid': 'Please provide a valid Tunisian phone number.', 'max_length': 'Phone number should have 8  digits.', 'unique': 'phone number already used'}, max_length=50, validators=[content.models.validate_tunisian_phone_number])),
                ('address', models.CharField(error_messages={'blank': 'chose an address', 'invalid': 'chose a valid address', 'max_length': 'address is to long !'}, max_length=50, validators=[content.models.validate_adress])),
                ('first_name', models.CharField(error_messages={'blank': 'write your first name', 'invalid': 'first name should contain only letters', 'max_length': 'first name is to long'}, max_length=30, validators=[content.models.validate_alpha])),
                ('password', models.CharField(error_messages={'blank': 'write your password', 'invalid': 'password should contain 8 carcteres a mix of letters numbers and special caracters', 'max_length': 'password is to long'}, max_length=128, validators=[content.models.validate_password])),
                ('last_name', models.CharField(error_messages={'blank': 'write your last name', 'invalid': 'last name should contain only letters', 'max_length': 'last name is to long'}, max_length=150, validators=[content.models.validate_alpha])),
                ('email', models.EmailField(error_messages={'blank': 'write your email address !', 'invalid': 'invalid email  !', 'max_length': 'email is to long !'}, max_length=254, unique=True)),
                ('role', models.CharField(choices=[('admin', 'admin'), ('teacher', 'teacher'), ('student', 'student')], max_length=10)),
                ('sex', models.CharField(choices=[('male', 'male'), ('female', 'female')], error_messages={'blank': 'chose a sex', 'invalid_choice': 'invalid sex', 'max_length': 'invalid sex'}, max_length=20)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('image_cover', models.ImageField(blank=True, default='default_user_cover.jpg', upload_to=content.models.upload_user_image_to)),
                ('image_profile', models.ImageField(blank=True, default='default_user_profile.jpg', upload_to=content.models.upload_user_image_to)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Chapiter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(error_messages={'blank': 'The title cannot be left blank.', 'null': 'The title cannot be null.'}, max_length=200, unique=True)),
                ('description', models.TextField(db_index=True, error_messages={'blank': 'The description cannot be left blank.'})),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(error_messages={'max_length': 'Title is to long '}, max_length=100)),
                ('image', models.ImageField(upload_to='subject_images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(upload_to='subject_images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('title', models.CharField(error_messages={'max_length': 'Title should not exceed %(max)d characters.'}, max_length=100, primary_key=True, serialize=False)),
                ('description', models.TextField(error_messages={'blank': 'Price per year cannot be left empty. Please provide a price.', 'null': 'Price per year cannot be null. Please provide a price.'})),
                ('price_per_month', models.DecimalField(decimal_places=2, error_messages={'blank': 'Price per year cannot be left empty. Please provide a price.', 'null': 'Price per year cannot be null. Please provide a price.'}, max_digits=3)),
                ('discount', models.PositiveIntegerField(default=0, error_messages={'blank': 'Price per year cannot be left empty. Please provide a price.', 'null': 'Price per year cannot be null. Please provide a price.'}, validators=[content.models.validate_discount])),
                ('image', models.ImageField(error_messages={'invalid_image': 'Invalid image format. Please upload a valid image.'}, upload_to='offer_images/')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CodeVerification',
            fields=[
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('code', models.CharField(editable=False, error_messages={'invalid': 'Invalid code format. Please use alphanumeric characters only.', 'max_length': 'The code is too long. Please use up to %(max)d characters.', 'unique': 'This code is already in use. Please choose a different code.'}, max_length=255, unique=True, validators=[content.models.validate_alphanumeric_code])),
                ('created_at', models.DateTimeField(default=datetime.datetime(2024, 2, 16, 10, 24, 4, 217764, tzinfo=datetime.timezone.utc), editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, quality=-1, scale=None, size=[64, 46], upload_to='subject_images/')),
                ('levels', models.ManyToManyField(related_name='level_subjects', to='content.level')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.PROTECT, to='content.level')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.subject')),
                ('user', models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ParentOfStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.parent')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='level',
            name='subjects',
            field=models.ManyToManyField(blank=True, null=True, related_name='subjects', to='content.subject'),
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='group',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.level'),
        ),
        migrations.AddField(
            model_name='group',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='content.professor'),
        ),
        migrations.CreateModel(
            name='GetOffer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.datetime(2024, 2, 16, 10, 24, 4, 224748, tzinfo=datetime.timezone.utc), error_messages={'invalid': 'Invalid date format. Please provide a valid date.'})),
                ('duration', models.DurationField(error_messages={'blank': 'Duration cannot be left empty. Please provide a duration.', 'invalid': 'Invalid duration format. Please provide a valid duration.', 'null': 'Duration cannot be null. Please provide a duration.'}, validators=[content.models.validate_duration])),
                ('cost', models.DecimalField(decimal_places=2, error_messages={'blank': 'Cost cannot be left empty. Please provide a cost.', 'invalid': 'Invalid cost format. Please provide a valid cost.', 'null': 'Cost cannot be null. Please provide a cost.'}, max_digits=8)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_offer', related_query_name='get_offer', to='content.offer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='get_offers', related_query_name='get_offers', to='content.student')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('published', 'published'), ('unpublished', 'unpublished')], max_length=20)),
                ('chapiter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.chapiter')),
                ('levels', models.ManyToManyField(related_name='course_levels', to='content.level')),
                ('teacher', models.ForeignKey(limit_choices_to={'role': 'teacher'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('title', 'chapiter')},
            },
        ),
        migrations.CreateModel(
            name='ContentDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('serie', 'serie'), ('summary', 'summary')], max_length=100)),
                ('file', models.FileField(upload_to=content.models.upload_document_to)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.course')),
                ('students_complete_content', models.ManyToManyField(blank=True, limit_choices_to={'role': 'student'}, null=True, related_name='completed_series', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='content_type_comments', to='contenttypes.contenttype')),
            ],
            options={
                'get_latest_by': 'created_at',
            },
        ),
        migrations.AddField(
            model_name='chapiter',
            name='levels',
            field=models.ManyToManyField(related_name='chapiter_levels', to='content.level'),
        ),
        migrations.AddField(
            model_name='chapiter',
            name='subject',
            field=models.ForeignKey(error_messages={'blank': 'Please select a subject.'}, on_delete=django.db.models.deletion.PROTECT, to='content.subject'),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('type', models.CharField(choices=[('exercice', 'exercice'), ('course', 'course')], max_length=100)),
                ('video', models.FileField(blank=True, upload_to=content.models.upload_videos_to)),
                ('attachment', models.FileField(blank=True, null=True, upload_to=content.models.upload_attachment_to)),
                ('status', models.CharField(choices=[('published', 'published'), ('unpublished', 'unpublished')], max_length=20)),
                ('is_free', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.course')),
                ('levels', models.ManyToManyField(related_name='level_videos', to='content.level')),
                ('offers', models.ManyToManyField(blank=True, null=True, related_name='offer_videos', to='content.offer')),
                ('students_complete_content', models.ManyToManyField(blank=True, limit_choices_to={'role': 'student'}, null=True, related_name='completed_videos', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('title', 'course')},
            },
        ),
    ]
