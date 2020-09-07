from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView
from account.models import User
from account.forms import RestaurantRegisterForm, UserEditForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, FormView , DeleteView, ListView , View
from django.views.generic.edit import FormMixin, FormView
from restaurant.models import *
from restaurant.forms import *
from django.contrib import messages
import datetime
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.db.models import Sum, Avg
import json



class RestaurantRegisterView(CreateView):
    model = User
    form_class = RestaurantRegisterForm
    template_name = 'register-restaurant.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        send_mail(
            'New User in Website',
            'New company registered and wait allowing',
            'reservetimealligator@gmail.com',
            ['ruhinshukurlu@gmail.com'],
            fail_silently=False,
        )
        return redirect('core:register-completed')


class MenuView(CreateView):
    model = Menu
    form_class = MenuForm
    template_name = 'company-menus.html'
    success_url = reverse_lazy('restaurant:menu')
    
    def form_valid(self, form):
        form.instance.company = self.request.user
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menus"] = Menu.objects.filter(company=self.request.user)
        context["menu_categories"] = MenuCategory.objects.all()
        
        return context


class MenuUpdateView(UpdateView):
    model = Menu
    template_name = "menu-detail.html"
    form_class = MenuForm

    def get_success_url(self):
        return reverse_lazy('restaurant:menu')


class MenuDeleteView(DeleteView):
    model = Menu
    template_name = "menu-detail.html"
    
    def get_success_url(self):
        return reverse_lazy('restaurant:menu')


class PhotoView(CreateView):
    model = Photo
    form_class = PhotoForm
    template_name = 'company-photos.html'
    success_url = reverse_lazy('restaurant:photo')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Something went wrong!!')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photos"] = Photo.objects.filter(owner=self.request.user)
        
        return context


class PhotoUpdateView(UpdateView):
    model = Photo
    template_name = "photo-detail.html"
    form_class = PhotoForm
    context_object_name = 'photo'

    def get_success_url(self):
        return reverse_lazy('restaurant:photo')
    

class PhotoDeleteView(DeleteView):
    model = Photo
    template_name = "photo-detail.html"
    
    def get_success_url(self):
        return reverse_lazy('restaurant:photo')


class CompanyInfosView(UpdateView):
    model = Company
    template_name = "company-infos.html"
    form_class = CompanyInfosForm
    context_object_name = 'company'
    
    def get_success_url(self, **kwargs):
        return reverse_lazy("restaurant:company-infos", kwargs={'pk': self.object.pk})


class CompanyTablesView(CreateView):
    model = Table
    template_name = 'company-tables.html'
    form_class = TableForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        company_start_hour = self.request.user.company.work_hours_from
        company_finish_hour = self.request.user.company.work_hours_to

        if company_start_hour and company_finish_hour:

            today = TableDate.objects.filter(date=datetime.datetime.today())

            inside_tables = Table.objects.filter(table_place = 'inside', company=self.request.user).order_by('size')
            outside_tables = Table.objects.filter(table_place = 'outside', company=self.request.user).order_by('size')
            print(outside_tables.dates)

            outside_table_list = []
            inside_table_list=[]
            table_obj = {}

            for table in outside_tables:
                for date in table.dates.filter(date=datetime.datetime.today()):

                    table_obj = {
                        'table' : table,
                        'times' : date.times.all()
                    }
                    outside_table_list.append(table_obj)

            for table in inside_tables:
                for date in table.dates.filter(date=datetime.datetime.today()):

                    table_obj = {
                        'table' : table,
                        'times' : date.times.all()
                    }
                    inside_table_list.append(table_obj)

            return render(request, self.template_name, {
                    'form' : form, 
                    'inside_tables' : inside_table_list, 
                    'outside_tables' : outside_table_list,
                })
        else:
            return render(request, self.template_name, {
                    'message' : "You haven't included start and finish work hours of your company, please go to the informations page and include work hours."
                })



    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            amount = form.cleaned_data['amount']
            size = form.cleaned_data['size']
            place = form.cleaned_data['table_place']
             
            company_start_hour = self.request.user.company.work_hours_from
            company_finish_hour = self.request.user.company.work_hours_to
            free_times = []
            free_times.append(company_start_hour)
            if company_start_hour and company_finish_hour:
                while company_start_hour < company_finish_hour:
                    company_start_hour = (datetime.datetime.combine(  
                            datetime.date(1, 1, 1),  
                            company_start_hour
                        ) + datetime.timedelta(minutes=30)).time()

                    free_times.append(company_start_hour)
                free_times = free_times[:-1]
            
                reserve_start_date = datetime.date.today()
                reserve_finish_date = (datetime.date.today()+datetime.timedelta(days=30)).isoformat()
            
                reserve_dates = []
                for i in range(31):
                    reserve_dates.append(reserve_start_date)
                    reserve_start_date = (reserve_start_date+datetime.timedelta(days=1))

                for i in range(amount): 
                    table = Table.objects.create(size = size, table_place = place, company = self.request.user)
                    
                    for free_date in reserve_dates:
                        date = TableDate.objects.create(date=free_date)
                        for free_time in free_times:
                            time = Time.objects.create(free_time = free_time, reserved = False)
                            date.times.add(time)

                        table.dates.add(date)
                        
            else:
                pass
            
            return HttpResponseRedirect(reverse_lazy('restaurant:company-tables', kwargs={'pk': self.request.user.pk}))

        return render(request,self.template_name, {'form' : form})


class TableDeleteView(DeleteView):
    model = Table
    template_name = "company-tables.html"
    
    def get_success_url(self):
        return reverse_lazy('restaurant:company-tables', kwargs={'pk': self.object.pk})  


class ResevedUserList(DetailView):
    model = Company
    template_name = 'company-users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(pk=self.kwargs.get('pk'))

        reservations = Reservation.objects.filter(company__in=company)
        print(reservations)

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
            

        print(all_reserved_user_list)
        
        context['reserved_users'] = all_reserved_user_list

        return context


class CompanyReservations(ListView):
    model = Reservation
    context_object_name = 'reservations'
    template_name='reservations-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(pk=self.kwargs.get('pk'))
        upcoming_reservations = Reservation.objects.filter(company = company.first(),accept = False, denied=False)
        accepted_reservations = Reservation.objects.filter(company = company.first(),accept = True, denied=False, reserved_date__gte=datetime.datetime.today())
        past_reservations = Reservation.objects.filter(company = company.first(),accept = True, denied=False, reserved_date__lt=datetime.datetime.today())
        
        context["upcoming_reservations"] = upcoming_reservations
        context["accepted_reservations"] = accepted_reservations
        context["past_reservations"] = past_reservations

        return context


class ReservationDetail(DetailView):
    model = Reservation
    template_name='reservation-detail.html'
    context_object_name = 'reservation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(pk=self.kwargs.get('pk'))
        reservation = Reservation.objects.filter(pk=self.kwargs.get('pk'))
        reservation_obj = {}
        reservation_detail = []
        for reserve in reservation:
            table_size = Table.objects.filter(pk = int(reserve.table_id)).values_list('size', flat = True)
            reservation_obj = {
                'reservation' : reservation,
                'table_size' : table_size
            }
            reservation_detail.append(reservation_obj)
        portions = reservation.first().portions.all()
        menus_list = []
        for portion in portions:
            portion_count = portion.portion_count
            menu = Menu.objects.filter( pk = int(portion.menu_id))
            menu_obj ={
                'menu': menu,
                'portion_count': portion_count
            }
            menus_list.append(menu_obj)
            
        context["reservation_detail"] = reservation_detail
        context['menus'] = menus_list
        context['menu_categories'] = MenuCategory.objects.all()
        return context


    def post(self, request, *args, **kwargs):
        reservation = Reservation.objects.filter(pk=self.kwargs.get('pk'))
        print(reservation)
        if request.POST['form_id'] == 'acceptReservation':
            reservation.update(accept=True)
            response_data = {}
            response_data['result'] = 'You succcessfully accept reservation'

            Notification.objects.create(
                sender = request.user,
                reciever = reservation.first().user,
                text = 'Your reservation accepted',
                notification_type = 'accept_reservation'
            )

            return HttpResponse(
                    json.dumps(response_data, indent=4, sort_keys=True, default=str),
                    content_type="application/json"
                )

        elif request.POST['form_id'] == 'deniedReservation':
            reservation.update(denied=True)
            response_data = {}
            response_data['result'] = 'You succcessfully denied reservation'

            Notification.objects.create(
                sender = request.user,
                reciever = reservation.first().user,
                text = 'Your reservation denied'
            )

            return HttpResponse(
                    json.dumps(response_data, indent=4, sort_keys=True, default=str),
                    content_type="application/json"
                )


class CommentView(FormMixin, DetailView):
    template_name = 'write-comment.html'
    model = Company
    form_class = CommentForm
    context_object_name = 'company'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
            
    def form_valid(self, form):
        print(self.request.POST)
        comment = form.save(commit=False)
        form.instance.user = self.request.user
        
        company =  get_object_or_404(Company, pk=self.kwargs.get('pk'))
        company_1 = Company.objects.filter(pk=self.kwargs.get('pk'))
        comments = Comment.objects.filter(company=company)
        comment.company = company
        comment.ratingFood = self.request.POST.get('ratingFood')
        comment.ratingService = self.request.POST.get('ratingService')
        comment.ratingAmbience = self.request.POST.get('ratingAmbience')
        comment.overall = int((int(self.request.POST.get('ratingFood')) + int(self.request.POST.get('ratingService')) + int(self.request.POST.get('ratingAmbience')))/3)
        comment.liked = self.request.POST.get('like')
        company_1.update(
            overall = int(comments.aggregate(Avg('overall')).get('overall__avg' , 0))
        )
        print(company.overall, comments.aggregate(Avg('overall')).get('overall__avg' , 0))
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('core:company-profile', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(pk=self.kwargs.get('pk'))

        liked_users_count = Comment.objects.filter(company = company.first(), liked=1).count()
        disliked_users_count = Comment.objects.filter(company = company.first(), liked=0).count()

        context["liked"] = liked_users_count
        context["disliked"] = disliked_users_count
        context['all_likes'] = liked_users_count + disliked_users_count

        return context


class CompanyReviews(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name='company-comments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(pk=self.kwargs.get('pk'))
        comments = Comment.objects.filter(company = company.first())
        
        context["comments"] = comments
        return context
