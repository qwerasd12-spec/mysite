from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'email': '이메일',
            'first_name': '이름',
            'last_name': '성',
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['major', 'student_id', 'address', 'phone', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False