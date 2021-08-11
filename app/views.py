from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . forms import CreateUser
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import random
from .models import PreRegistration
from .forms import VerifyForm,LoginForm
from django.contrib.auth import login,logout,authenticate
# Create your views here.

def creatingOTP():
    otp = ""
    for i in range(11):
        otp+= f'{random.randint(0,9)}'
    return otp

def sendEmail(email):
    otp = creatingOTP()
    send_mail(
    'One Time Password',
    f'Your OTP pin is {otp}',
    settings.EMAIL_HOST_USER,
    [email],
    fail_silently=False,
    )
    return otp


def createUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateUser(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                otp = sendEmail(email)
                dt = PreRegistration(first_name=form.cleaned_data['first_name'],last_name=form.cleaned_data['last_name'],username= form.cleaned_data['username'],email=email,otp=otp,password1 = form.cleaned_data['password1'],password2 = form.cleaned_data['password2'])
                dt.save()
                return HttpResponseRedirect('/verify/')
                
                
        else:
            form = CreateUser()
        return render(request,"html/register.html",{'form':form})
    else:
        return HttpResponseRedirect('/success/')

def login_function(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usr = authenticate(username=username,password = password)
                if usr is not None:
                    login(request,usr)
                    return HttpResponseRedirect('/success/')
        else:
            form = LoginForm()
        return render(request,'html/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/success/')

def verifyUser(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = VerifyForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                data = PreRegistration.objects.filter(otp = otp)
                if data:
                    username = ''
                    first_name = ''
                    last_name = ''
                    email = ''
                    password1 = ''
                    for i in data:
                        print(i.username)
                        username = i.username
                        first_name = i.first_name
                        last_name = i.last_name
                        email = i.email
                        password1 = i.password1

                    user = User.objects.create_user(username, email, password1)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    data.delete()
                    messages.success(request,'Account is created successfully!')
                    return HttpResponseRedirect('/verify/')   
                else:
                    messages.success(request,'Entered OTO is wrong')
                    return HttpResponseRedirect('/verify/')
        else:            
            form = VerifyForm()
        return render(request,'html/verify.html',{'form':form})
    else:
        return HttpResponseRedirect('/success/')

def success(request):
    if request.user.is_authenticated:
        return render(request,'html/success.html')
    else:
        return HttpResponseRedirect('/')

def logout_function(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')