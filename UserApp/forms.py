from django import forms
from UserApp.models import User

class FormUser(forms.Form):

    sfirstname = forms.CharField(label='sfirstname', max_length=100)
    slastname = forms.CharField(label='slastname', max_length=100)
    semail = forms.CharField(label='semail', max_length=100)
    password = forms.CharField(label='spassword', max_length=100)


class UserInputForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('password','email')