from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from account.models import User
from restaurant.models import *

class CompanyEditForm(forms.ModelForm):
    profile_img = forms.ImageField(required=False, widget=forms.FileInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control height',
                'placeholder' : 'First Name',
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control height',
                'placeholder' : 'Last Name',
                }),
            'email' : forms.EmailInput(attrs = {
                'class' : 'form-control height',
                'placeholder' : 'Email'
            }),
        }

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ('title','price','description','menu_type',)

        widgets = {
            'title' : forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Title'
            }),
            'price' : forms.NumberInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Price'
            }),
            'menu_type' : forms.Select(attrs={
                'class' : 'form-control',
                'placeholder' : 'Type'
            }),
            'description' : forms.Textarea(attrs={
                'class' : 'form-control',
                'placeholder' : 'Write description ...',
                'rows' : '5'
            })
        }

class PhotoForm(forms.ModelForm):
    photo_url = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class' : 'form-control mr-2',
        'placeholder' : 'Photo Url'
    }))

    class Meta:
        model = Photo
        fields = ("photo",'photo_url','photo_type',)

        widgets = {
            'photo' : forms.ClearableFileInput(attrs = {
                'id' : 'upload-img'
            }),
            'photo_type' : forms.Select(attrs={
                'class' : 'select-img-type form-control',
                'placeholder' : 'Type'
            })
        }


class CompanyInfosForm(forms.ModelForm):
    work_hours_from = forms.TimeField( widget=forms.TimeInput(attrs={
        'class' : 'form-control',
        'type' : 'time'
    }))
    work_hours_to = forms.TimeField( widget=forms.TimeInput(attrs={
        'class' : 'form-control',
        'type' : 'time'
    }))
    
    class Meta:
        model = Company
        fields = ['company_name','phone_number','city_location','province_location',
                  'country_location','work_hours_from','work_hours_to','cuisine',
                  'dining_style','parking_details','public_transit','payment_options',
                  'executive_chef','website','private_party_contact','description','cover_photo']

        widgets = {
            'company_name' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'cover_photo' : forms.ClearableFileInput(attrs={
                'class' : 'form-control'
            }),
            'phone_number' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'city_location' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'province_location' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'country_location' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'cuisine' : forms.Select(attrs={
                'class' : 'form-control'
            }),
            'dining_style' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'parking_details' : forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : '5'
            }),
            'public_transit' : forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : '5'
            }),
            'payment_options' : forms.Select(attrs={
                'class' : 'form-control'
            }),
            'executive_chef' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'website' : forms.URLInput(attrs={
                'class' : 'form-control'
            }),
            'private_party_contact' : forms.TextInput(attrs={
                'class' : 'form-control'
            }),
            'description' : forms.Textarea(attrs={
                'class' : 'form-control',
                'rows' : '5'
            }),
        }


class TableForm(forms.ModelForm):
    amount = forms.IntegerField(widget= forms.NumberInput(attrs={
        'class' : 'form-control'
    }), required=True)

    class Meta:
        model = Table
        fields = ("size",'table_place')

        widgets = {
            'size' : forms.NumberInput(attrs={
                'class' : 'form-control'
            }),
            'table_place' : forms.Select(attrs={
                'class' : 'form-control'
            })
        }

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ("text",'comment_image',)

        widgets = {
            'text' : forms.Textarea(attrs={
                'class' : 'form-control',
                'cols' : "30",
                'rows' : "5",
                'placeholder':"Please, write your review about foods and service in the restaurant"
            }),
            'comment_image' : forms.ClearableFileInput(attrs = {
                'class' : 'form-control',
                'id' : 'upload-img'
            })

        }
