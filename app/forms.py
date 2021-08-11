from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.contrib.auth.models import User
from django.core import validators
def validete_username(value):
    if len(value)<=2:
        raise forms.ValidationError(f"Your username cannot be of {len(value)}  word")

class CreateUser(UserCreationForm):
    password1 = forms.CharField(label="Password", widget = forms.PasswordInput(attrs={"placeholder":"Password",'autocomplete':'new-password','class':'form-control'}),error_messages={"required":"Please enter password"},)
    password2 = forms.CharField(label="Re-enter",widget= forms.PasswordInput(attrs={"placeholder":"Re-Enter",'autocomplete':'new-password','class':'form-control'}),help_text="Make sure your password contains 'small letter','capital letter','numbers' and 'symbols'",error_messages={"required":"Re-Enter password field cannot be empty"})
    username = forms.CharField(label="username",widget=forms.TextInput(attrs={"placeholder":"Username","id":"username",'class':'form-control'}),validators=[validete_username])
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"First Name","required":True,'class':'form-control'}),error_messages={"required":"First name cannot be empty"})
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"First Name","required":True,'class':'form-control'}),error_messages={"required":"Last name cannot be empty"})
    email = forms.CharField(widget=forms.EmailInput(attrs={"required":True,"Placeholder":"Email",'class':'form-control'}),error_messages={'required':'Email fields should not be empty'})
    class  Meta:
        model = User
        fields =['username','first_name','last_name','email','password1','password2']
    

class VerifyForm(forms.Form):
    otp = forms.CharField(label='OTP',max_length=70,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'OTP','required':True}),error_messages={'required':'Enter a otp'})


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"placeholder":"Username","class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"password",'autocomplete':'current-password',"class":"form-control"}))  