from .models import Member
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class AddMemberForm(forms.ModelForm):
    class Meta:
        model=Member
        fields=['name','age','image']
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise forms.ValidationError("パスポートの上にある「名前/name」を入力してください")
        
        if len(name) >50:
            raise forms.ValidationError("50文字以下でお願いします")
        return name
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

