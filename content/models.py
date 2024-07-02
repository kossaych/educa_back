from collections.abc import Iterable
from django.core.exceptions import ValidationError
from django.db import models
 
from custom_models import ModelWithSerializeOption
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone
from PIL import Image
from django.db.models import F
from rest_framework.authtoken.models import Token
import random
import string
import hashlib
import uuid

from django.contrib.auth.models import AbstractUser 
from django.core.mail import EmailMessage
from django_resized import ResizedImageField

import os
 
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
 
#import  fitz   
import pypdfium2 as pdfium

from django.conf import settings  
import os 

START_PHONE_NUMBER_OPERATORS = [2, 5, 9]
# validators 
def validate_discount(value):
            if value>100 :
                raise ValidationError('dicount must be in range 0 -> 100')

def validate_duration(value):
    if value < timezone.timedelta(days=1):
        raise ValidationError("Duration must be greater than or equal to one day.")

def validate_future_date(value):
    if value < timezone.now().date():
        raise ValidationError("Start date cannot be in the past.")

def validate_image_dimensions(value):
    max_width = 1920  # Maximum allowed width in pixels
    max_height = 1080  # Maximum allowed height in pixels

    image = Image.open(value)
    width, height = image.size

    if width > max_width or height > max_height:
        raise ValidationError(
            f'Image dimensions exceed the maximum allowed ({max_width}px width, {max_height}px height).'
        )

def validate_image_size(value):
    max_size = 2 * 1024 * 1024  # 2 MB
    if value.size > max_size:
        raise ValidationError(f'Image size exceeds the maximum allowed ({filesizeformat(max_size)}).')

def validate_image_format(value):
    allowed_formats = ['image/jpeg', 'image/png', 'image/gif']
    if value.content_type not in allowed_formats:
        raise ValidationError('Invalid image format. Please upload a JPEG, PNG, or GIF image.')

def validate_tunisian_phone_number(phone_number):
    if not phone_number.isalnum() :
         raise ValidationError('invalid phone number')
         
    if len(phone_number) != 8 or (int(phone_number[0]) not in START_PHONE_NUMBER_OPERATORS):
        raise ValidationError(' invalid phone number ')

def validate_alphanumeric_code(value):
    if not value.isalnum():
        raise ValidationError("Invalid code format. Please use only alphanumeric characters.")

def validate_adress(adress):
    
    CITY_CHOICES = [
        "ARIANA",
        "BEJA",
        "BEN AROUS",
        "BIZERTE",
        "GABES",
        "GAFSA",
        "JENDOUBA",
        "KAIROUAN", 
        "KASSERINE",
        "KEBILI",
        "LE KEF",
        "MAHDIA",
        "MANOUBA",
        "MEDENINE",
        "MONASTIR",
        "NABEUL",
        "SFAX",
        "SIDI BOUZID",
        "SILIANA",
        "SOUSSE",
        "TATAOUINE",
        "TOZEUR",
        "TUNIS",
        "ZAGHOUAN",
    ]
  
    if adress.upper() not in CITY_CHOICES :
        raise ValidationError("chose an address")

def validate_niveau_scolaire(niveau):
         
    NIVEAU_SCOLAIRE_CHOICES = [
           "BAC SCIENCE TECH", 
           "BAC MATH",
           "BAC SCIENCE EXP",
           "BAC SCIENCE INFO",
           "BAC ECONOMIE GESTION",
           "BAC LETTRES",
           "BAC SPORT",

           
           "3EME SCIENCE EXP", 
           "3EME SCIENCE INFO", 
           "3EME SCIENCE MATH",
           "3EME SCIENCE TECH", 
           "3EME ECONOMIE GESTION",
           "3EME LETTRES", 
           "3EME SPORT", 


           "2EME SCIENCE",
           "2EME TECH INFO",
           "2EME LETTRES", 
           "2EME ECONOMIE GESTION",

           "1ERE ANNEE",
    ]
    if niveau.upper() not in NIVEAU_SCOLAIRE_CHOICES :
         raise ValidationError('niveau scolaire invalide ')

def validate_password(password) :
        if len(password) < 8 and password.isascii() == False :
            raise ValidationError('password should have more then 8 chars')
        nb_digits = 0
        nb_carecters = 0
        nb_letters = 0
        index = 0
        while (nb_digits < 1 or nb_carecters < 1 or nb_letters) and index < len(password) :
            if password[index] in string.digits :
                nb_digits += 1
            elif password[index] in string.ascii_letters :
                nb_letters += 1  
            else :
                nb_carecters += 1
            index += 1
        if  (nb_digits < 1 or nb_carecters < 1 or nb_letters < 1) :
            raise ValidationError('password invalid')

def validate_alpha(value) : 
     if not(value.isalpha()) :
        raise ValueError('first and last name should contain only letters')
 
# to ensure that each video is related to its course
def validate_chapiter_levels_is_in_its_subject_levels(level) : 
    level = Level.objects.get(id = level,)
 
##################### upload to functions #############################""
def upload_user_image_to(instance,filename):
    extention = filename.split('.')[-1]
    filename = str(uuid.uuid4())+"."+(extention)
    return '/'.join([str(instance.first_name+instance.last_name),filename])

def upload_videos_to(instance,filename):
    extention = filename.split('.')[-1]
    filename = str(uuid.uuid4())+"."+(extention) 
    
    try : 
        os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.course.id)])) 
    except FileExistsError : 
        try : 
            os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.course.id),instance.type])) 
        except FileExistsError : 
            try :    
                os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.course.id),instance.type,'video'])) 
            except FileExistsError : 
                pass

    return '/'.join([str(instance.course.id),instance.type,'video',str(filename)]) 
 
def upload_attachment_to(instance,filename):
    extention = filename.split('.')[-1]
    filename = str(uuid.uuid4())+"."+(extention) 
    
    try : 
        os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.course.id)])) 
    except FileExistsError : 
        try : 
            os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.course.id),instance.type])) 
        except FileExistsError : 
            try :    
                os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.course.id),instance.type,'attachment'])) 
            except FileExistsError : 
                pass

    return '/'.join([str(instance.course.id),instance.type,'attachment',str(filename)]) 

def upload_document_to(instance,filename):
    extention = filename.split('.')[-1]
    filename = str(uuid.uuid4())+"."+(extention)  
    return '/'.join([instance.make_directorie(),str(filename)]) 

def upload_correction_to(instance,filename):
    extention = filename.split('.')[-1]
    filename = str(uuid.uuid4())+"."+(extention) 
    
    try :  
        os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.serie.course.id)])) 
    except FileExistsError : 
        try : 
            os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.serie.course.id),instance.serie.type])) 
        except FileExistsError : 
            try :    
                os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(instance.serie.course.id),instance.serie.type,'serie_correction'])) 
            except FileExistsError : 
                pass

    return '/'.join([str(instance.serie.course.id),instance.serie.type,'serie_correction',str(filename)]) 
  
class CodeVerification(models.Model):
    user = models.ForeignKey('BaseUser',editable=False, on_delete=models.CASCADE,primary_key  = True)
    code = models.CharField(
        max_length=255,
        editable=False,
        null = False,
        unique=True,
        validators=[validate_alphanumeric_code],
        error_messages={
            "unique": "This code is already in use. Please choose a different code.",
            "max_length": "The code is too long. Please use up to %(max)d characters.",
            "invalid": "Invalid code format. Please use alphanumeric characters only.",
        }
    )
    created_at = models.DateTimeField(default=timezone.now(), editable=False) 
    # virifier la validité du code au raport du temps 
    def check_code_time(self):     
         
        if (timezone.now()-self.created_at)<(timezone.timedelta(days=0,minutes=5,seconds=0)):
            return True
        return False
     
    # generate a verification code 
    @staticmethod
    def generate_code():
        letters =  string.digits
        letters_list = [random.choice(letters) for _ in range(6)]
        return ''.join(letters_list)
   #this function run out before each save
    def clean(self) :
        if  self.is_valid != True or self.code != "" :
                raise ValidationError("created_at and code should be automatecly genered")
    
    def save(self, *args, **kwargs) :
        code = self.code
        code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest()
        self.code = code_hash 
        self.created_at = timezone.now()
        super(CodeVerification, self).save(*args, **kwargs)
 
class BaseUser(AbstractUser,ModelWithSerializeOption) :
    phone = models.CharField(
        validators=[validate_tunisian_phone_number],
        max_length = 50,
        error_messages={
            "blank" : 'please write your phone number',
            "unique" : "phone number already used",
            "max_length": "Phone number should have 8  digits.",
            "invalid": "Please provide a valid Tunisian phone number.",
    },    )
    address = models.CharField(
        max_length=50,
        null=False,
        blank=False,    
        validators=[validate_adress],
        error_messages={
            "blank": "chose an address",
            "max_length": "address is to long !",
            "invalid": "chose a valid address",
    }, )
    first_name = models.CharField(
        max_length = 30,
        validators = [validate_alpha],
        error_messages = {
            "blank" : 'write your first name',
            "max_length": "first name is to long",
            'invalid' : 'first name should contain only letters'
        }
        )
    password = models.CharField(
         max_length = 128 ,
         validators = [validate_password],
         error_messages = {
              "blank" : "write your password" ,
              "max_length": "password is to long",
              'invalid' : "password should contain 8 carcteres a mix of letters numbers and special caracters"
    })
    last_name = models.CharField(
        max_length = 150,
        validators = [validate_alpha],
        error_messages = {
            "blank" : 'write your last name',
            "max_length": "last name is to long",
            'invalid' : 'last name should contain only letters'
        }
        )
    email = models.EmailField(
        unique = True,
        error_messages = {
                    'blank' : 'write your email address !',
                    "max_length": "email is to long !",
                    'invalid' : 'invalid email  !'
                }
    )
    role = models.CharField(choices = [('admin','admin'),('teacher','teacher'),('student','student')],max_length = 10)
    sex = models.CharField(
                            max_length = 20,
                            choices = [('male','male'),('female','female')],
                            error_messages = {
                                        'blank' : 'chose a sex',
                                        "max_length": "invalid sex",
                                        'invalid_choice' : 'invalid sex',
                                    }
                           ) 
    date_of_birth = models.DateField(null=True, blank=True)
    image_cover = models.ImageField(upload_to = upload_user_image_to ,blank=True,default='default_user_cover.jpg')
    image_profile = models.ImageField(upload_to = upload_user_image_to,blank=True,default='default_user_profile.jpg')
  
    username = None
    REQUIRED_FIELDS = ['role','first_name','last_name','password']
    USERNAME_FIELD = 'email'
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    def get_level_or_descepline(self) :
        if self.role == 'student' : 
            student = Student.objects.get(user_id = self.pk)            
            return student.level 
        elif self.role == 'teacher' :
            teacher = Professor.objects.get(user = self)
            return teacher.discipline
        else :  raise ('this user is not student or a teacher')
 
    def  send_email (self,label,messege) :
            email = EmailMessage(label,str(messege), to=[self.email])
            print(str(messege))
            """try : 
                email.send()
            except Exception as e :
                raise (e)"""

class Professor(ModelWithSerializeOption) :
 
    user = models.ForeignKey(
        BaseUser,
        db_constraint=False ,
        on_delete = models.CASCADE
        )
    discipline = models.ForeignKey(
        'Subject',
        on_delete = models.CASCADE
        ) 

class Student(ModelWithSerializeOption) : 
    user = models.ForeignKey(
        BaseUser,
        db_constraint=False ,
        on_delete = models.CASCADE
        )
    level =  models.ForeignKey(
        'Level',
        db_constraint=False ,
        on_delete = models.PROTECT
        )

class Course(ModelWithSerializeOption) :
    title = models.CharField(
        null=False,
        blank=False,
        max_length=100,  
    )
    teacher = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role' : 'teacher'},
        null=False,
        blank=False,
    )
    chapiter = models.ForeignKey(
        'Chapiter',
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
      
    )     
    status = models.CharField(choices = (('published','published'),('unpublished','unpublished')),max_length = 20)
    levels =   models.ManyToManyField(
        'Level',
        related_name = 'course_levels',
        null=False,
        blank=False
    )
    class Meta() :
        unique_together = [["title", "chapiter"]]
    def __str__(self) :
        return str(self.title) + ' made by ' + str(self.teacher)

class Video(ModelWithSerializeOption):
    title = models.CharField( 
        max_length=100,  
        null=False,
        blank=False
    )
    course  = models.ForeignKey(
        'Course',
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
      
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    url = models.CharField( 
        max_length  = 255,
        blank = True,
        null = False, 
    )
    students_complete_content = models.ManyToManyField(
        BaseUser, 
        limit_choices_to= {'role' : 'student'},
        related_name = 'completed_videos',
        null=True,
        blank=True
    )
    type = models.CharField(choices = [('exercice','exercice'),('course','course')],max_length = 100,null=False,blank=False)
    video = models.FileField(blank=True ,upload_to= upload_videos_to)
    attachment = models.FileField(blank=True,null=True,upload_to= upload_attachment_to) 
    status = models.CharField(choices = (('published','published'),('unpublished','unpublished')),max_length = 20)
    is_free = models.BooleanField(default = False)
    # people with these levels can see this video
    levels =   models.ManyToManyField(
        'Level',
        related_name = 'level_videos',
        null=False,
         
        blank=False
    )
    # people who got this offer can watch the video 
    offers =   models.ManyToManyField(
        'Offer',
        related_name = 'offer_videos',
        blank=True,
        null =True, 
    )
    def completed(self,user) :
        return user in self.students_complete_content.all()
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs) :
        if str(self.video) not in ['','1']:
            self.url = str(settings.HOST) + str(settings.MEDIA_URL) + str(self.video)
        super(Video, self).save(*args, **kwargs)
    def delete(self): 
        print('*'*10000)
        if self.video and os.path.isfile(self.video.path) : 
            print( str(self.video.path))
            os.remove(str(self.video.path))
        if self.attachment and os.path.isfile(self.attachment.path) : 
            print( str(self.attachment.path))
            os.remove(str(self.attachment.path))
        
        super(Video, self).delete()
        
    
    class Meta() :
        unique_together = [["title", "course"]]

class Page(ModelWithSerializeOption) : 
    title = models.CharField(
        null=False,
        blank=False,
        max_length=100,  
    ) 
    document = models.ForeignKey(
        'ContentDocument',
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
      
    )
    path = models.CharField(
        null=False,
        blank=False,
        max_length=100, 
        unique = True
    ) 
    def __str__(self) :
        if self.document.type != 'correction' : 
            return self.document.type +" "+ self.document.title + ' : ' + self.title[1:self.title.index('.')]
        else : 
            return self.document.type +" "+ self.document.serie.title + ' : ' + self.title[1:self.title.index('.')]

class ContentDocument(ModelWithSerializeOption) :
    title = models.CharField(
        null=False,
        blank=False,
        max_length=100, 
        unique = True
    ) 
    course  = models.ForeignKey(
        'Course',
        null=False,
        blank=False,
        on_delete=models.CASCADE, 
      
    ) 
    created_at = models.DateTimeField(
        auto_now_add=True
    ) 
    students_complete_content = models.ManyToManyField(
        BaseUser, 
        limit_choices_to= {'role' : 'student'},
        related_name = 'completed_series',
        null=True,
        blank=True
    ) 
    type = models.CharField(choices = [('serie','serie'),('summary','summary'),('correction','correction')],max_length = 100,null=False,blank=False)
    file = models.FileField(upload_to= upload_document_to)
    serie = models.ForeignKey(
        'self',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        unique=True
      
    )
    serie = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT, 
    )
    def make_file_pages(self,image_format='png') :   
          
        pdf_path = os.path.join(settings.MEDIA_ROOT, str(self.file))
        pdf = pdfium.PdfDocument(pdf_path) 

        pages_path = self.make_directorie()
         
        for i in range(len(pdf)):
            page = pdf[i]
            image = page.render(scale=4).to_pil()
            image_name = str("\\page" + str(i))+"."+(image_format)
            page_instance = Page(
                title = image_name,
                document = self,
                path = self.type +'/'+ self.title +'/'+ image_name[1:]
            ) 
            page_instance.save()
            image.save(pages_path + image_name)     
 
    def make_directorie(self) :  
        try : 
            os.mkdir('\\'.join([str(settings.BASE_DIR),'media',str(self.type)])) 
        except FileExistsError : 
            try : 
                os.mkdir('\\'.join([str(settings.BASE_DIR),'media',self.type,self.title])) 
            except FileExistsError : 
                pass 
        return '\\'.join([str(settings.BASE_DIR),'media',self.type,self.title ])
   
    def completed(self,user) :
        return user in self.students_complete_content.all() 
  
    def save(self, *args, **kwargs) :
        if self.type == 'correction' and self.serie == None:
            raise ValidationError('correction instance must have a serie document') 
        if self.type != 'correction' and self.serie != None :
            raise ValidationError('serie or summary instance Do not have a related document') 
        super(ContentDocument, self).save(*args, **kwargs) 
        self.make_file_pages() 
    
    def delete(self, *args, **kwargs):
        # Custom behavior before deletion
        print(f'{self.name} is about to be deleted.')
        super().delete(*args, **kwargs)
        # Custom behavior after deletion
        print(f'{self.name} has been deleted.')
    def __str__(self) :
        return 'chapitre ' + str(self.course) + ' : ' + str(self.title)
    
# only administration can add and change thise tables
class Subject(ModelWithSerializeOption) : 
    title = models.CharField(max_length=50) 
    image = ResizedImageField(size=[64,46],upload_to='subject_images/', null=False, blank=False) 
    levels =   models.ManyToManyField(
        'Level',
        related_name = 'level_subjects',
        null=False,
        blank=False
    )
    def progress_subject(self,user) :  
        try :
           progress =   int((     (len(user.completed_videos.all()) + len(user.completed_series.all()))  * 100)/ (len(Video.objects.filter(course__chapiter__subject = self)) + len(Serie.objects.filter(course__chapiter__subject = self)))    )
        except : 
            progress = 0
        return progress
    def __str__(self):
        return self.title

class Level(ModelWithSerializeOption) : 
    title = models.CharField(
        max_length=100,
        unique  = True,
    )
    image = models.ImageField(upload_to='subject_images/', null=False, blank=False)     
    subjects = models.ManyToManyField(
        Subject,
        related_name = 'subjects',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.title

class Offer(ModelWithSerializeOption): 
    title = models.CharField(
        max_length=100,
        primary_key=True,
        error_messages={
        "max_length": "Title should not exceed %(max)d characters.",
    },)
    description = models.TextField(null=False,blank=False  ,
             error_messages={
            "null": "Price per year cannot be null. Please provide a price.",
            "blank": "Price per year cannot be left empty. Please provide a price.",
    },)
    price_per_month = models.DecimalField(max_digits=3, decimal_places=2,null=False,blank=False ,
             error_messages={
            "null": "Price per year cannot be null. Please provide a price.",
            "blank": "Price per year cannot be left empty. Please provide a price.",
    },)
    discount = models.PositiveIntegerField(default= 0,null=False,
            validators=[validate_discount],
            error_messages={
            "null": "Price per year cannot be null. Please provide a price.",
            "blank": "Price per year cannot be left empty. Please provide a price.",
    },)
    image = models.ImageField(
            upload_to='offer_images/',
            error_messages={
            'invalid_image': 'Invalid image format. Please upload a valid image.',
    },) 
    teacher = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role' : 'teacher'},
        null=False,
        blank=False,
    )
    def __str__(self):
        return self.title

class GetOffer(ModelWithSerializeOption):
    offer = models.ForeignKey('Offer', on_delete=models.CASCADE,related_name='get_offer',related_query_name='get_offer')
    user = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='get_offers',related_query_name='get_offers')
    start_date = models.DateField (
        default = timezone.now(),
         error_messages={
            "invalid": "Invalid date format. Please provide a valid date.",
        },
    )
    duration = models.DurationField(
        null=False,
        blank=False,
        validators=[validate_duration],  # Add the custom duration validator here
        error_messages={
            "null": "Duration cannot be null. Please provide a duration.",
            "blank": "Duration cannot be left empty. Please provide a duration.",
            "invalid": "Invalid duration format. Please provide a valid duration.",
        },
    )
    cost = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=False,
        blank=False,
        error_messages={
            "null": "Cost cannot be null. Please provide a cost.",
            "blank": "Cost cannot be left empty. Please provide a cost.",
            "invalid": "Invalid cost format. Please provide a valid cost.",
        },
    )
    
    def __str__(self) :
        return f"Get Offer {self.offer.title} for {self.user.user.first_name +'  '+self.user.user.last_name}"
    
    def save(self, *args, **kwargs):
        if self.pk: 
                raise ValueError("update not enable for  this data")
        
        offers = GetOffer.objects.filter(user=self.User,offer = self.offer,start_date__gt = timezone.now() + F('duration')) 



        if  self.pk == None and len(offers) > 0:
                raise ValueError("you can not get this offer you are alredy have a one")
        super(GetOffer, self).save(*args, **kwargs)
 

# to ensure that each chapiter is related to its subject
def validate_chapiter_levels_is_in_its_subject_levels(level) : 
    pass # you have to use this function in Chapiter save method 


class Chapiter(ModelWithSerializeOption):
    title = models.CharField( 
        max_length=200, 
        null=False,
        blank=False, 
        error_messages={'blank': 'The title cannot be left blank.','null': 'The title cannot be null.'}
    )
    description = models.TextField(
        db_index=True,
        null=False,
        blank=False,
        #db_comment="Chapiter description",
        error_messages={'blank': 'The description cannot be left blank.'}
    )
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.PROTECT,
        #db_comment="Chapiter subject",
        error_messages={'blank': 'Please select a subject.'}
    )
    levels =   models.ManyToManyField(
        Level,
        related_name = 'chapiter_levels',
        null=False, 
        blank=False
    )

    def progress_chapiter(self,user) :  
        try : 
           progress =   int((len(user.completed_videos.filter(course__chapiter = self)) * 100)/ len(Video.objects.filter(course__chapiter = self)))
        except : 
            progress = 0 
        return progress
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        unique_together = (("title", "subject"),)
##### soon ##########
    
class Group (ModelWithSerializeOption) :
    professor =  models.ForeignKey('Professor',on_delete = models.PROTECT)  
    title = models.CharField(
        max_length=100,
        error_messages={
            "max_length": "Title is to long ",
        },) 
    level = models.ForeignKey('Level',on_delete = models.PROTECT) 
    image = models.ImageField(upload_to='subject_images/', null=False, blank=False)  
    def __str__(self):
        return self.title

class Inscription(ModelWithSerializeOption) :
    student =  models.ForeignKey('Student',on_delete = models.PROTECT)
    group =  models.ForeignKey('Group',on_delete = models.PROTECT)

class Comment(ModelWithSerializeOption):
    content_type = models.ForeignKey(ContentType,on_delete = models.PROTECT, related_name="content_type_comments")
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') 
    content = models.TextField(
        #db_comment="Comment content",
        null=False,
        blank=False,
    )
    author = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        #db_comment="Comment author"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    
    def __str__(self):
        return f"Comment by {self.author.role}     {self.author.first_name }    {self.author.last_name}"
    
    class Meta: 
        get_latest_by = 'created_at'
 
class ParentOfStudent(ModelWithSerializeOption) : 
    student =  models.ForeignKey('Student',on_delete = models.PROTECT)
    parent =   models.ForeignKey('Parent',on_delete = models.PROTECT)

class Parent(ModelWithSerializeOption) :
    user = models.ForeignKey(
        BaseUser,
        db_constraint=False ,
        on_delete = models.PROTECT
        )
 
####################################
@receiver(post_save,sender = BaseUser)
def add_profil_and_token(sender,instance,created,**kwargs):
        if created:
            Token.objects.create(
                                    user = instance
                                )  