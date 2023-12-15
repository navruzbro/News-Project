from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Parol", widget=forms.PasswordInput)
    password_2 = forms.CharField(label="Parolni qayta kiriting", widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = ['username','first_name','email']

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password_2']:
            raise forms.ValidationError("Parol mos emas!")
        return data['password2']
    

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth','photo','bio']
