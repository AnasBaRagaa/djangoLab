from django import forms
from django.forms import ModelChoiceField, DateInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Entry, Contact

"""
owner : Anas Ba Ragaa

This based lab 11 and 12 requirements for CMP416

"""


# defining a base form class to add the user attribute
class BaseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        # pass the user argument to the form from the base view classes inside get_form_kwargs()
        if 'user' in kwargs.keys():
            user = kwargs.pop('user')
            self.user = user
        else:
            self.user = None
        super(BaseForm, self).__init__(*args, **kwargs)


class ContactForm(BaseForm):
    class Meta:
        model = Contact
        exclude = ['owner']
        widgets = {
            # attrs is used to pass html parameters
            # this is equivalent to <input type="date">
            'added_on': DateInput(attrs={'type': 'date'})
        }


class EntryForm(BaseForm):
    def __init__(self, *args, **kwargs):
        super(EntryForm, self).__init__(*args, **kwargs)
        self.fields['contact'] = ModelChoiceField(queryset=Contact.objects.all().filter(
            owner=self.user))  # show only the contacts belonging to the current user

    class Meta:
        # specify which model and fields to use
        model = Entry
        fields = ['contact', 'entry_value', 'entry_type']


# not my code
class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user
