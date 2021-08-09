from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from . forms import CreateUser
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.

def creatingOTP():
    otp = ""
    for i in range(6):
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
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            otp = sendEmail(email)
            request.session['email'] = otp
            return HttpResponseRedirect('/')
            
            return HttpResponseRedirect('/')
    else:
        form = CreateUser()
    return render(request,"html/register.html",{'form':form})

def verifyUser(request):
    return render(request,'html/veify.html')