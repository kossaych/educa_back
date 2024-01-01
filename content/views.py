from .models import *
 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
 
from django.core.mail import EmailMessage
  
from serialiser import *


from django.conf import settings 
from django.http import FileResponse
import os

def get_video(request, video_name):
    video_path = os.path.join(settings.MEDIA_ROOT, 'videos', video_name)
    return FileResponse(open(video_path, 'rb'), content_type='video/mp4')

def get_pdf(request, pdf_filename):
    pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdf_files', pdf_filename) 
    resp = FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    return resp
  
class ProfileApi(APIView) :
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
            #get data 
            try :  
                first_name = request.data.get('firstName').strip()
                last_name = request.data.get('lastName').strip() 
                address = request.data.get('address').strip() 
                sex = request.data.get('sex').strip()
                role =  request.data.get('role').strip() 
                image_cover  = request.data.get('imgCover') 
                image_profile  = request.data.get('imgProfile') 

            except Exception as e : 
                return Response('Incomplete data',status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user
            if role == 'teacher' : 
                discipline = request.data.get('descepline') 
                if discipline != '' : 
                    discipline = Subject.objects.get(id = discipline)
                    print(discipline)
                    teacher = Professor.objects.get(user = user) 
                    teacher.discipline = discipline
                    teacher.save() 
                    print(teacher.discipline)

            if role == 'student' :
                level = request.data.get('level') 
                if level != '': 
                    level = Level.objects.get(id=level)
                    student = Student.objects.get(user = user)
                    student.level = level
                    student.save()
                
            try : 
                user.first_name = first_name
                user.last_name = last_name
                user.address = address
                user.sex = sex
                if image_cover != "" :
                   user.image_cover = image_cover
                if image_profile != "" :
                   user.image_profile = image_profile
                user.save() 
            except Exception as e :  
                try :
                    return Response(str(e.messages[0]),status=status.HTTP_400_BAD_REQUEST)
                except :
                    return Response(str(e),status=status.HTTP_400_BAD_REQUEST) 
    
            return Response(Token.objects.get(user=user).key,status=status.HTTP_200_OK)

    def get(self,request) :
        user = request.user.serialize(
            address = Field('address'),
            firstName = Field('first_name'),
            lastName = Field('last_name') ,
            level =  FunctionField('get_level_or_descepline'),
            descepline =  FunctionField('get_level_or_descepline'),
            email = Field('email'),
            phone = Field('phone'),
            imgCoverUrl = Field('image_cover'),
            imgProfileUrl = Field('image_profile'),
            sex = Field('sex') , 
            role = Field('role')
     
        ) 
   
        return Response(user,status = status.HTTP_200_OK)

class GetAddresesAPI(APIView) : 
    def get(self,request) :
        addreses = [
            {"address" : "ARIANA", "id" : "1"},
            {"address" : "BEJA", "id" : "2"},
            {"address" : "BEN AROUS", "id" : "3"},
            {"address" : "BIZERTE", "id" : "4"},
            {"address" : "GABES", "id" : "5"},
            {"address" : "GAFSA", "id" : "6"},
            {"address" : "JENDOUBA", "id" : "7"},
            {"address" : "KAIROUAN", "id" : "8"}, 
            {"address" : "KASSERINE", "id" : "9"},
            {"address" : "LE KEF", "id" : "10"},
            {"address" : "MAHDIA", "id" : "11"},
            {"address" : "MANOUBA", "id" : "12"},
            {"address" : "MEDENINE", "id" : "13"},
            {"address" : "MONASTIR", "id" : "14"},
            {"address" : "NABEUL", "id" : "15"},
            {"address" : "SFAX", "id" : "16"},
            {"address" : "SIDI BOUZID", "id" : "17"},
            {"address" : "SILIANA", "id" : "18"},
            {"address" : "SOUSSE", "id" : "19"},
            {"address" : "TATAOUINE", "id" : "20"},
            {"address" : "TOZEUR", "id" : "2"},
            {"address" : "TUNIS", "id" : "22"},
            {"address" : "ZAGHOUAN", "id" : "23" },
            {"address" : "KEBILI", "id" : "24"},

        ]
        return Response(addreses,status=status.HTTP_200_OK)
    
class RegisterView(APIView): 
    def post(self,request):
            #get data 
            try :
                email = request.data.get('email').strip()
                password = request.data.get('password1')
                first_name = request.data.get('firstName').strip()
                last_name = request.data.get('lastName').strip()
                phone = request.data.get('phone').strip()
                address = request.data.get('address').strip() 
                sex = request.data.get('sex').strip() 
                role = request.data.get('role') 
            except Exception as e :
                 return Response('Incomplete data',status=status.HTTP_400_BAD_REQUEST)
             # create user acount
            try : 
                user = BaseUser(role = role,first_name = first_name,last_name = last_name,phone = phone,address = address, email = email,password = password,is_active = False,sex = sex)
                BaseUser.objects.filter(email = email,is_active = False).delete()
                BaseUser.objects.filter(phone = phone,is_active = False).delete()
                user.full_clean()
                user.set_password(password)
                user.save() 
            except Exception as e:  
                try :
                    return Response(str(e.messages[0]),status=status.HTTP_400_BAD_REQUEST)
                except :
                    return Response(str(e),status=status.HTTP_400_BAD_REQUEST) 
           
            if role == 'student'  : 
                print(role)
                try : 
                    level = request.data.get('level').strip()
                    level = Level.objects.get(id = level)    
                except Exception as e : 
                     return Response('chose a division',status=status.HTTP_400_BAD_REQUEST) 
                try : 
                    student = Student(level = level,user = user)
                    student.save()

                except Exception as e:   
                    user.delete()
                    return Response(str(e),status=status.HTTP_400_BAD_REQUEST)

            elif role == 'teacher' :   
                try : 
                    discipline = request.data.get('discipline').strip() 
                    discipline = Subject.objects.get(id = discipline)
                except : 
                    return Response('invalid discipline',status=status.HTTP_400_BAD_REQUEST)  
                # create teacher instance  
                try :
                    professor = Professor (user = user,discipline = discipline)    
                    professor.save()
                    print(professor)
                except Exception as e:
                    user.delete()
                    return Response(str(e),status=status.HTTP_400_BAD_REQUEST)
             # create verification code and send email
            try : 
                #  create verification code 
                code = CodeVerification.generate_code()  
                code_inst =  CodeVerification(user = user,code = code)
                code_inst.save()    
                user.send_email('Activate your account.',code) 
            except Exception as e :  
                user.delete()
                #return Response('test',status=status.HTTP_400_BAD_REQUEST)
                raise e   
 
            
            
            
            return Response('Please confirm your email address to complete the registration',status=status.HTTP_200_OK)
 
class ActivateUser(APIView):
    def post(self,request):
                email = request.data.get('email')
                code = request.data.get('code')  

                try :
                    user = BaseUser.objects.get(email=email)
                except : 
                    return Response('user not registed',status=status.HTTP_400_BAD_REQUEST)
                
              
                code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest() 

                try :
                    code_registed = CodeVerification.objects.get(user=user.pk) 
                except :
                    import time
                    time.sleep(1)
                    return Response("code not sended to your email",status = status.HTTP_400_BAD_REQUEST) 

                if code_hash == code_registed.code :
                        if code_registed.check_code_time() :
                            code_registed.delete() 
                            user.is_active = True
                            user.save() 
                        else :
                            import time
                            time.sleep(1)
                            return Response("code time out",status = status.HTTP_400_BAD_REQUEST)
                else : 
                    import time
                    time.sleep(1)
                    return Response("invalid code",status = status.HTTP_400_BAD_REQUEST)  

                return Response(Token.objects.get(user=user).key,status=status.HTTP_200_OK) 
             
class Login(APIView):       
    def post(self,request):
        email=request.data.get('email')
        password = request.data['password']

        try :
            user = BaseUser.objects.get(email=email)
        except :
            return Response('email not regested',status=status.HTTP_400_BAD_REQUEST)    
  
        user = BaseUser.objects.get(email=request.data.get('email'))

        if user.check_password(password) : 
            print(user.phone)
            if user.is_active :    
                return Response(Token.objects.get(user=user).key,status=status.HTTP_200_OK)
            else :   
                return Response('account not active and activation failed try to register agian',status=status.HTTP_400_BAD_REQUEST)
        else :
            import time
            time.sleep(1)
            return Response('false data',status=status.HTTP_400_BAD_REQUEST) 

class ResetPassword(APIView):
    def post(self,request):
        email = request.data['email']
        try :
            user = BaseUser.objects.get(email=email)
        except :
            return Response('email not regested')
        
        code = CodeVerification.generate_code()
        code_inst =  CodeVerification(user = user,code = code)
        code_inst.save() 
        # send email with code
        email = EmailMessage('Activate your account.',str(code), to=[email])
        try :
            email.send()
        except Exception as e:
            user.delete()
            return Response('sending email failed please try again ! ',status=status.HTTP_400_BAD_REQUEST)

        return Response('check your email',status=status.HTTP_200_OK)

class CheckCode(APIView):    
    def post(self,request):
        email = request.data.get('email')
        code = request.data.get('code')

        try :
            user = BaseUser.objects.get(email=email)
        except :
             return Response('user not found',status=status.HTTP_400_BAD_REQUEST)
        
        code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest() 

        try :
            code_registed = CodeVerification.objects.get(user=user.pk) 
        except :
            import time
            time.sleep(1)
            return Response("code not sended to your email",status = status.HTTP_400_BAD_REQUEST) 

        if code_hash == code_registed.code :
                if code_registed.check_code_time() :
                    code_registed.delete()
                    return Response(True,status=status.HTTP_200_OK) 
                else :
                    import time
                    time.sleep(1)
                    return Response("code time out",status = status.HTTP_400_BAD_REQUEST)
        else : 
            import time
            time.sleep(1)
            return Response("invalid code",status = status.HTTP_400_BAD_REQUEST) 

class SetPassword(APIView):
    def post(self,request):

        email = request.data.get('email')
        code = request.data.get('code')
        new_password=request.data.get('password')

        try :
            user = BaseUser.objects.get(email=email)
        except :
            return Response('user not registed',status=status.HTTP_400_BAD_REQUEST)  
    



        code_hash = hashlib.sha256(code.encode('utf-8')).hexdigest() 

        try :
            code_registed = CodeVerification.objects.get(user=user.pk) 
        except :
            import time
            time.sleep(1)
            return Response("code not sended to your email",status = status.HTTP_400_BAD_REQUEST) 

        if code_hash == code_registed.code :
                if code_registed.check_code_time() : 

                    code_registed.delete()
                    user.set_password(new_password)
                    user.is_active = True
                    user.full_clean() 
                    user.save() 
                    return Response(Token.objects.get(user=user).key,status=status.HTTP_200_OK)
                
                else :
                    import time
                    time.sleep(1)
                    return Response("code time out",status = status.HTTP_400_BAD_REQUEST)
        else : 
            import time
            time.sleep(1)
            return Response("invalid code",status = status.HTTP_400_BAD_REQUEST) 
 
class ChangePassword(APIView) :
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        current_password =request.data.get('current_password')
        new_password=request.data.get('password')
        user = request.user 
        if  user.check_password(current_password):
                    try :
                        user.set_password(new_password)
                        user.full_clean
                        user.save() 
                        return Response(status=status.HTTP_200_OK)
                    except Exception as e :
                        try :
                            return Response(str(e.messages[0]),status=status.HTTP_400_BAD_REQUEST)
                        except Exception as e:
                            return Response(str(e),status=status.HTTP_400_BAD_REQUEST) 
        else :
            import time
            time.sleep(1)
            return Response('current password uncorrect',status.HTTP_400_BAD_REQUEST)                           

class GetLevelsAPI(APIView) : 
    def get(self,request) :
        data = Level.objects.all()
        serialised_data = Serializer(data,id = Field('id'),level = Field('title')).serialize()
        return Response(serialised_data,status=status.HTTP_200_OK)

class GetSubjectsAPI(APIView) :
    def get(self,request) :
        data = Subject.objects.all()
        serialised_data = Serializer(
            data,
            id = Field('id'),
            title = Field('title'),
            image = Field('image')
            ).serialize()
        return Response(serialised_data,status=status.HTTP_200_OK)
      
class SubjectPkAPI(APIView) : 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id) :
        user = request.user
        data = Subject.objects.filter(id = id).serialize(
            id = Field('id'),
            title = Field('title'),
            image = Field('image'), 

            chapiters = RelationField('subject',Chapiter).set_fields(
                
                progress = FunctionField('progress_chapiter',user),
                title = Field('title'),
                id = Field('id')
                ),   

            progress = FunctionField('progress_subject',user)
           )
             
        return Response(data,status=status.HTTP_200_OK)




class ChapiterPkAPI(APIView) : 
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request,id) :
        user = request.user
        data = Chapiter.objects.get(id = id).serialize( 

            id = Field('id'),
            title = Field('title'),   
            videos_cour = RelationField('chapiter',Video).set_fields(
                    title = Field('title'),
                    type = Field('type'),
                    createdAt  = Field('created_at'),
                    url = Field('url'),
                    completed = FunctionField('completed',user),
                    attachment = RelationField('video',AttachmentVideo),

                    teacher = RelationField('teacher').set_fields(
                        id = Field('id'),
                        firstName = Field('first_name'),
                        lastName = Field('last_name'),
                        imgProfile = Field('image_profile'),
                        imgCover = Field('image_cover') 
                    )

                ).set_filters(type = 'cour'),
            videos_exercice = RelationField('chapiter',Video).set_fields(
                    title = Field('title'),
                    type = Field('type'),
                    createdAt  = Field('created_at'),
                    url = Field('url'),
                    completed = FunctionField('completed',user),
                    attachment = RelationField('video',AttachmentVideo),
                    teacher = RelationField('teacher').set_fields(
                        id = Field('id'),
                        firstName = Field('first_name'),
                        lastName = Field('last_name'),
                        imgProfile = Field('image_profile'),
                        imgCover = Field('image_cover') 
                    )

                ).set_filters(type = 'exercice'),
            series = RelationField('chapiter',Serie).set_fields(
                    title = Field('title'),
                    created_at  = Field('created_at'), 
                    pagesj = RelationField('serie',SeriePage).set_fields(content = Field('content')),  
                    pages = FunctionField('get_content_images'),  

                    completed = FunctionField('completed',user),
                    attachment = RelationField('serie',AttachmentSerie),
                    correction = RelationField('serie',Correction).set_fields(
                            title = Field('title'), 
                            attachment = RelationField('correction',AttachmentCorrection),
                            pages = RelationField('correction',CorrectionPage),
                            teacher = RelationField('teacher').set_fields(
                                id = Field('id'),
                                firstName = Field('first_name'),
                                lastName = Field('last_name'),
                                imgProfile = Field('image_profile'),
                                imgCover = Field('image_cover') 
                            )
                    ),
                    teacher = RelationField('teacher').set_fields(
                        id = Field('id'),
                        firstName = Field('first_name'),
                        lastName = Field('last_name'),
                        imgProfile = Field('image_profile'),
                        imgCover = Field('image_cover') 
                    )
                )
            
            )
 
        return Response(data,status=status.HTTP_200_OK)
   

