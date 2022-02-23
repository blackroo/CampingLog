from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView, PasswordResetCompleteView



app_name = 'common'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),

    path('password_reset/', 
    PasswordResetView.as_view(template_name='common/password_reset_form.html'), 
    name='password_reset'),


    path('password_reset/done/', 
    PasswordResetDoneView.as_view(
        template_name='common/password_reset_done.html'), 
    name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/ ', 
    PasswordResetConfirmView.as_view(
        template_name='common/password_reset_confirm.html'), 
    name='password_reset_confirm'),

    path('reset/done/', 
    PasswordResetCompleteView.as_view(
        template_name='common/password_reset_complete.html'), 
    name='password_reset_complete'),


    path('delete/', views.delete, name='delete')
]
