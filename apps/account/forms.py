from django import forms
from .models import SimpleUser

class SimpleUserForm(forms.ModelForm):
    class Meta:
        model = SimpleUser
        fields = ('username', 'email')
