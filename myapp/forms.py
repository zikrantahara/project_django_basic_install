from django import forms
from .models import Dreamreal

class DreamrealForm(forms.ModelForm):
    class Meta:
        model = Dreamreal
        fields = "__all__"
        
    def __init__(self, *args, **kwargs):
        super(DreamrealForm, self).__init__(*args, **kwargs)
        self.fields['website'].widget.attrs['readonly'] = True
        self.fields['mail'].widget.attrs['readonly'] = True

class LoginForm(forms.Form):
    # Menggunakan 'username' agar konsisten dengan file views
    username = forms.CharField(max_length = 100)
    password = forms.CharField(widget = forms.PasswordInput())

    # Custom Validation: Mengecek apakah user ada di database
    def clean_username(self):
        username = self.cleaned_data.get("username")
        dbuser = Dreamreal.objects.filter(name = username)
        
        if not dbuser:
            raise forms.ValidationError("User does not exist in our db!")
        return username