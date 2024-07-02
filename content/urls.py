from django.urls import path
from . import views
urlpatterns = [
    path('api/register/',views.RegisterView.as_view()),
    path('api/activate/',views.ActivateUser.as_view()),
    path('api/login/',views.Login.as_view(),name='login'),
    path('api/reset_password/',views.ResetPassword.as_view()),
    path('api/check_code/',views.CheckCode.as_view()),
    path('api/set_password/',views.SetPassword.as_view()),
    path('api/change_password/',views.ChangePassword.as_view()),
    path('api/profile/',views.ProfileApi.as_view(),name='profil'),

    path('api/get_levels/',views.GetLevelsAPI.as_view()),
    path('api/get_addreses/',views.GetAddresesAPI.as_view()),
    path('api/get_disciplines/',views.GetDesiplinesAPI.as_view()),
    path('api/subject/<int:id>',views.SubjectPkAPI.as_view()),
    path('api/get_subjects/',views.GetSubjectsAPI.as_view()),
    path('api/get_teacher_courses/',views.GetTeacherCoursesAPI.as_view()),
    path('api/get_teacher_desipline_chapiters/',views.GetTeacherDesiplineChapitersAPI.as_view()),


    path('api/course/',views.CourseAPI.as_view()),
    path('api/course_pk/<int:id>',views.CoursePkAPI.as_view()),
    path('api/video/',views.VideoAPI.as_view()),





    path('api/chapiter/<int:id>',views.ChapiterPkAPI.as_view()),


    path('api/get_video/<str:video_name>/', views.get_video, name='get_video'),#file transfer
    path('api/get_pdf/<str:pdf_filename>/', views.get_pdf, name='get_pdf'),#file transfert


    path('api/get_chapiter_levels/<int:id>/', views.GetChapiterLevels.as_view()),
    path('api/video/<int:id>/', views.VideoPkAPI.as_view()),




 

]