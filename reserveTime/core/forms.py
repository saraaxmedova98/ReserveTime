from django import forms
from account.models import User
from restaurant.models import *

class FindTableForm(forms.Form):

    size = forms.IntegerField( required=True, widget=forms.NumberInput(attrs={
        'id' : 'party-size'
    }))
    date = forms.DateField( required=True, widget=forms.DateInput(attrs={
        'id': 'date',
        'type': 'date'
    }))
    time = forms.TimeField( required=True, widget=forms.TextInput(attrs={
        'type': 'time',
        'id': 'time'
    }))
    

