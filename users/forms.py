
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from random import choices
from string import ascii_letters, digits

def generate_password(length=7):
    return ''.join(choices(ascii_letters + digits, k=length))+"$"

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not password1 and not password2:
            auto_password = generate_password()
            cleaned_data['password1'] = auto_password
            cleaned_data['password2'] = auto_password
            self.data = self.data.copy()
            self.data['password1'] = auto_password
            self.data['password2'] = auto_password

        return cleaned_data

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
