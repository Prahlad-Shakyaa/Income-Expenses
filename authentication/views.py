from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token

from django.contrib import auth

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error':'username should only contain alphanumeric characters'})
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Sorry! the username is already taken. Please choose other one'})
        return JsonResponse({'username_valid': True})
    
class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error':'Email is Invalid'})
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error':'Sorry! the email is already taken. Please choose other one'})
        return JsonResponse({'email_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'password too short')
                    return render(request, 'authentication/register.html')
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse('activate',kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
                activate_url = 'http://' + domain + link

                email_subject = 'activate your account'
                email_body = 'Hi' + user.username + 'Please click on the link to activate your account \n' + activate_url
                email = EmailMessage(
                    email_subject,
                    email_body,
                    'noreply@semycolon.com',
                    [email]
                )
                email.send(fail_silently=False)

                messages.success(request, 'Account created successfully, Please check your email to Activate your Account')
                return render(request, 'authentication/register.html')
                
        return render(request, 'authentication/register.html')

    
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated Successfully.')
            return redirect('login')
        except Exception as ex:
            pass
        return redirect('login')
    

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')
    
    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request,user)
                    messages.success(request,'Welcome, ' + user.username + 'you are now logged in')
                    return redirect('expenses')

                messages.error(request,'Account is not active, Please check your email to activate your account')
                return render(request, 'authentication/login.html')
                
            messages.error(request,'Invalid credentials, Please try again')
            return render(request, 'authentication/login.html')
        
        messages.error(request,'Please fill all the fields')
        return render(request, 'authentication/login.html')
    

class LogoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'you have been logged out')
        return redirect('login')
    
    
# class RequestPasswordResetEmail(View):
#     def get(self, request):
#         return render(request,'authentication/reset-password.html')
    
#     def post(self, request):
#         email = request.POST['email']
#         context = {
#             'values': request.POST
#         }
#         if not validate_email(email):
#             messages.error(request, 'Please provide a proper email used to register the account ')
#             return render(request,'authentication/reset-password.html')
        
#         uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#         domain = get_current_site(request).domain
#         link = reverse('activate',kwargs={'uidb64': uidb64, 'token': account_activation_token.make_token(user)})
#         activate_url = 'http://' + domain + link

#         email_subject = 'activate your account'
#         email_body = 'Hi' + user.username + 'Please click on the link to activate your account \n' + activate_url
#         email = EmailMessage(
#             email_subject,
#             email_body,
#             'noreply@semycolon.com',
#         [email]
#         )
#         email.send(fail_silently=False)
#         return render(request,'authentication/reset-password.html')
        