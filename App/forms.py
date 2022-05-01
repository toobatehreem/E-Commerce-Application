from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    address = forms.CharField(max_length=200)
    phone = PhoneNumberField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'address', 'phone')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.address = self.cleaned_data['address']
        user.phone = self.cleaned_data['phone']
        if commit:
            user.save()
        return user