from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


ROLE_CHOICES = [
    ('Author', 'Author — Write, edit and publish blog posts'),
    ('Reader', 'Reader — Read, comment and follow authors'),
]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.RadioSelect,
        initial='Reader',
        label='Join as',
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'bio', 'avatar', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
