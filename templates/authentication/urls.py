from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views

from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('register/',RegistrationView.as_view(),name='register'),
    path('employer/register/', EmployerRegistrationView.as_view(), name='employer_register'),  # Employer Registration

    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),

    path('authentication/validate-username',csrf_exempt(UsernameValidationView.as_view()),name='validate-username'),
    path('authentication/validate-email',csrf_exempt(EmailValidationView.as_view()),name='validate-email'),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name='activate'),

    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name='password_reset_complete'),

]
