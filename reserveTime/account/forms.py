from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.db import transaction
from .models import User,Company,Customer

class CustomerRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
                    'class': 'form-control height',
                    'placeholder' : 'First Name *',
                }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
                    'class': 'form-control height',
                    'placeholder' : 'Last Name *',
                }))
    username = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
                    'class': 'form-control height',
                    'placeholder' : 'Email *',
                }))
    password1 = forms.CharField(required=True, widget = forms.PasswordInput(attrs={
                    'class': 'form-control height',
                    'placeholder' : 'Password *',
                }))
    password2 = forms.CharField(required=True, widget = forms.PasswordInput(attrs={
                    'class': 'form-control height',
                    'placeholder' : 'Re-enter Password *',
                }))
                
    # profile_image = forms.FileField('Profile', max_length=, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.is_active = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('username')
        user.save()
        customer = Customer.objects.create(user=user)
        customer.phone_number=self.cleaned_data.get('phone_number')
        # customer.location=self.cleaned_data.get('location')
        customer.save()
        return user


class RestaurantRegisterForm(UserCreationForm):
    password1 = forms.CharField(required=True, widget = forms.PasswordInput(attrs={
                    'class': 'form-control register-input',
                    
                }), label = 'Password')
    password2 = forms.CharField(required=True, widget = forms.PasswordInput(attrs={
                    'class': 'form-control register-input',
                    
                }), label = 'Confirm Password')
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
                    'class': 'form-control register-input',
                }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
                    'class': 'form-control register-input',
                }))
    username = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
                    'class': 'form-control register-input',
                }), label='Email Address')

    company_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={
                    'class': 'form-control register-input',
                }))
    phone_number = forms.CharField(required=True, widget=forms.TextInput(attrs={
                    'class': 'form-control register-input',
                }))

    city_location = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
                    'class': 'form-control register-input',
                }))
    province_location = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
                    'class': 'form-control register-input',
                }))
    country_location = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
                    'class': 'form-control register-input',
                }))

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_company = True
        user.is_active = False
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('username')
        user.save()
        company = Company.objects.create(user=user)
        company.phone_number=self.cleaned_data['phone_number']
        company.company_name=self.cleaned_data['company_name']
        company.city_location=self.cleaned_data['city_location']
        company.province_location=self.cleaned_data['province_location']
        company.country_location=self.cleaned_data['country_location']
        company.save()
        return user
 
  
class LoginForm(forms.Form):
    username = forms.EmailField(widget = forms.EmailInput(attrs = {
        'placeholder' : 'Email',
        'class' : 'form-control',
    }))
    password = forms.CharField(widget = forms.PasswordInput(attrs = {
        'placeholder' : 'Password',
        'class' : 'form-control',
    }))


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
        'placeholder' : 'Old password'
    }), required=True)

    new_password1 = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
        'placeholder' : 'New password'
    }), required=True)

    new_password2 = forms.CharField(widget = forms.PasswordInput(attrs = {
        'class' : 'form-control',
        'placeholder' : 'Re-enter new password'
    }), required=True)
    
    
class UserEditForm(forms.ModelForm):
    # profile_img = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email','profile_img']

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control height mb-4',
                'placeholder' : 'First Name',
                }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control height mb-4',
                'placeholder' : 'Last Name',
                }),
            'email' : forms.EmailInput(attrs = {
                'class' : 'form-control height mb-4',
                'placeholder' : 'Email'
            })
        }