from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.utils.translation import ugettext_lazy as _

from restaurant.models import Company
from account.managers import UserManager


class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_company = models.BooleanField(default=False)
    
    email = models.EmailField(_("Email"), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    profile_img = models.ImageField(_("Profile image"),upload_to='profile-pictures/', null=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'    
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email



class Customer(models.Model):
    user = models.OneToOneField("account.User", verbose_name=_("customer"), on_delete=models.CASCADE, primary_key=True, related_name='customer')
    
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.user.email
    

