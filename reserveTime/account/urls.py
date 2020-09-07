from django.urls import path
from account.views import *
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views 
from django.urls import reverse_lazy


app_name = 'account'

urlpatterns = [
    path('user/register', CustomerRegisterView.as_view(), name= 'user-register'),
    
    path('login', login_view, name='login'),
    path('logout', LogoutView.as_view(), name = 'logout'),

    path('change_password/',ChangePasswordView.as_view(), name = 'change-password'),
    path('change_password_done/',ChangePasswordDoneView.as_view(), name = 'change-password-done'),

    path("user/<int:pk>", CustomerProfileView.as_view(), name="user-profile"),
    path("user/<int:pk>/update", CustomerUpdateView.as_view(), name="user-update"),

    path("company/<int:pk>", CompanyProfileView.as_view(), name="company-profile"),
    path("company/<int:pk>/update", CompanyUpdateView.as_view(), name="company-update"),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name = 'reset_password.html',
     success_url = reverse_lazy('account:password_reset_done')),
     name="password_reset"),

    path('reset_password_done/', 
        auth_views.PasswordResetDoneView.as_view(template_name = 'reset_password_done.html'), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name = 'password_reset_confirm.html',success_url = reverse_lazy('account:password_reset_complete')), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name = 'password_reset_complete.html'), 
        name="password_reset_complete"),
]



'''
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''
