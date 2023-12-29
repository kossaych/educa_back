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
    path('api/get_disciplines/',views.GetSubjectsAPI.as_view()),
    path('api/subject/<int:id>',views.SubjectPkAPI.as_view()),
 
]