from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.views.generic import DetailView, UpdateView
from account.models import *
from account.forms import *
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from restaurant.models import *
from django.db.models import Sum, Avg
import datetime


class CustomerRegisterView(CreateView):
    model = User
    form_class = CustomerRegisterForm
    template_name = 'register-user.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)
        return redirect('core:home')



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        email = request.POST['username']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('core:home')
        else:
            messages.error(request,'Email or password is not correct')
            return redirect('account:login')

    else:
        form = LoginForm()
    return render(request, 'login-user.html', {'form': form})




class ChangePasswordView(PasswordChangeView):
    template_name = 'change-password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('core:home')


class ChangePasswordDoneView(PasswordChangeDoneView):
    template_name = 'change_password_done.html'


class CustomerProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user-profile.html'
    context_opject_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        upcoming_reservations = Reservation.objects.filter(user=self.request.user, accept=True, reserved_date__gte=datetime.datetime.today())
        past_reservations = Reservation.objects.filter(user=self.request.user, accept=True, reserved_date__lt=datetime.datetime.today())

        context["upcoming_reservations"] = upcoming_reservations
        context["past_reservations"] = past_reservations
        
        return context

    def get_object(self):
        return self.request.user


class CustomerUpdateView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user-edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('account:user-profile', kwargs={'pk': self.object.pk})


class CompanyProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'company-admin-page.html'
    context_opject_name = 'user'

    def get_object(self):
        return self.request.user
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        company = Company.objects.filter(pk=self.kwargs.get('pk'))
        comments = Comment.objects.filter(company = company.first())

        food = comments.aggregate(Avg('ratingFood'))
        service = comments.aggregate(Avg('ratingService'))
        ambience = comments.aggregate(Avg('ratingAmbience'))

        reservations = Reservation.objects.filter(company__in=company)

        all_reserved_user_list = []
        check_user_list = []
        
        for reservation in reservations:
            if reservation.user not in check_user_list:
                reserved_user_obj = {
                    'user' : reservation.user,
                    'reservation_count' : reservations.filter(user = reservation.user).count(),
                    'total_price' : reservations.filter(user = reservation.user).aggregate(Sum('total_price')).get('total_price__sum' , 0),
                    'last_reserved_date' : reservations.filter(user = reservation.user).last().reserved_date,
                    'reviews' : reservation.user.user_comment.all().count()
                }
                all_reserved_user_list.append(reserved_user_obj)
            check_user_list.append(reservation.user)

        context['reserved_users_count'] = len(all_reserved_user_list)
        

        if food.get('ratingFood__avg', 0) and service.get('ratingService__avg', 0) and ambience.get('ratingAmbience__avg', 0)   :
            print('ok')
            context['food_avg'] = "{:.1f}".format(food.get('ratingFood__avg', 0))

            context['service_avg'] = "{:.1f}".format(service.get('ratingService__avg', 0))

            context['ambience_avg'] = "{:.1f}".format(ambience.get('ratingAmbience__avg', 0))

        return context
    


class CompanyUpdateView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user-edit.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('account:company-profile', kwargs={'pk': self.object.pk})