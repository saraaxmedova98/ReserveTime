from django.shortcuts import render, redirect
from django.urls import reverse
import json
from django.http import HttpResponse, HttpResponseRedirect
from restaurant.models import *
from django.views.generic import DetailView,TemplateView, ListView, UpdateView, FormView , DeleteView, View
from django.views.generic.edit import FormMixin, FormView
from core.forms import *
from django.shortcuts import get_list_or_404, get_object_or_404 
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Avg
from itertools import chain

from core.tasks import complete_reserve, give_feedback

import stripe
stripe.api_key = "sk_test_51HGewRGdwSoA84C6OD2Xuc3Mc3nM8czUjbfkzXJqCOgmsaCZ3wl3CTlhUZOKZbdiWTQ5Ila1d91uKTkNRkO0mDBM00KXkrNFWo"


class HomeView(TemplateView):
    template_name = "home-page.html"
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.order_by('-created_at')[:4]
        all_companies = Company.objects.all()

        def generateCompanies(companies):
            company_list = []
            for company in companies:
                if company.user.is_active:
                    comments = company.company_comment.all()
                    company_overall = comments.aggregate(Avg('overall'))
                    if company_overall.get('overall__avg', 0):
                        company_rating = int(company_overall.get('overall__avg', 0))
                        company.overall = company_rating
                        company.save()

                        company_dict = {
                            'company' : company,
                            'reservation_count' : company.reservation.filter(reserved_at=datetime.date.today()).count(),
                            'company_overall' : company_rating
                        }
                    else:
                        company_dict = {
                            'company' : company,
                            'reservation_count' : company.reservation.filter(reserved_at=datetime.date.today()).count(),
                            'company_overall' : 0
                        }
                        company.overall = 0
                    company_list.append(company_dict)
            return company_list
        
        context['companies'] = generateCompanies(companies)
        context['all_companies'] = generateCompanies(all_companies)


        companies_by_city = Company.objects.all().distinct('city_location')
        city_list = []
        for company in companies_by_city:
            city_groups= {
                'city_location' : company.city_location,
                'count' : Company.objects.filter(city_location = company.city_location).count()
            }
            city_list.append(city_groups)
        context['company_groups'] = city_list
        
        context['cuisines'] = Cuisine.objects.all()
        if self.request.user.is_authenticated:
            context['notifications'] = Notification.objects.filter(reciever=self.request.user, read=False)
        return context


class RegisterCompleted(TemplateView):
    template_name = "register-completed.html"

    
class ReadNotifications(View):

    def post(self, request, *args, **kwargs):

        if request.POST.get('form_id') == 'readNotifications':
            notifications = Notification.objects.filter(reciever=request.user, read=False)
            notifications.update(read=True)
            response_data = {}
            return HttpResponse(
                    json.dumps(response_data, indent=4, sort_keys=True, default=str),
                    content_type="application/json"
                )


class CommentFilterView(ListView):
    model = Comment
    template_name = "comment-filter.html"
    context_object_name = 'comments'
    show_change_link = True
    
    def get_queryset(self):
        queryset = super().get_queryset()
        company = Company.objects.filter(pk=self.kwargs.get('pk'))
        queryset = queryset.filter(company = company.first())

        sort_data = self.request.GET.get('commentSort')

        if sort_data == 'newest':
            return queryset.order_by('-commented_at')
        elif sort_data == 'highest':
            return queryset.order_by('-overall')
        elif sort_data == 'lowest':
            return queryset.order_by('overall')
        
        return queryset


class CompanyProfile(FormMixin, DetailView):
    model = Company
    template_name = 'company-profile.html'
    form_class = FindTableForm
    
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        company = Company.objects.filter(pk=self.kwargs.get('pk'))
        company_photos = Photo.objects.filter(owner=company.first().user)
        context['photos'] = company_photos
        
        menu_categories = MenuCategory.objects.all()
        context['menu_categories'] = menu_categories

        menus = Menu.objects.filter(company = company.first().user)
        context['menus'] = menus

        comments = Comment.objects.filter(company = company.first())
        
        company_overall = comments.aggregate(Avg('overall'))

        if company_overall.get('overall__avg', 0):
            context['company_overall'] = int(company_overall.get('overall__avg', 0))
            
            food = comments.aggregate(Avg('ratingFood'))
            context['food_avg'] = "{:.1f}".format(food.get('ratingFood__avg', 0))

            service = comments.aggregate(Avg('ratingService'))
            context['service_avg'] = "{:.1f}".format(service.get('ratingService__avg', 0))

            ambience = comments.aggregate(Avg('ratingAmbience'))
            context['ambience_avg'] = "{:.1f}".format(ambience.get('ratingAmbience__avg', 0))


        liked_users_count = Comment.objects.filter(company = company.first(), liked=1).count()
        disliked_users_count = Comment.objects.filter(company = company.first(), liked=0).count()
        context['liked_users_count'] = liked_users_count
        context['disliked_users_count'] = disliked_users_count
        context['all_likes'] = liked_users_count + disliked_users_count

       
        context['overall_count_5'] = comments.filter(overall=5).count()
        context['overall_count_4'] = comments.filter(overall=4).count()
        context['overall_count_3'] = comments.filter(overall=3).count()
        context['overall_count_2'] = comments.filter(overall=2).count()
        context['overall_count_1'] = comments.filter(overall=1).count()

        comment_list = []
        for comment in comments:
            comment_dict = {
                'comment' : comment,
                'overall' : int((comment.ratingFood + comment.ratingService + comment.ratingAmbience)/3)
            }
            comment_list.append(comment_dict)

        context['comments'] = comment_list

        context['users'] = User.objects.all()

        if self.request.user.is_authenticated:
            saved_restaurant = SavedRestaurant.objects.filter(company=company.first(), user= self.request.user)
            context['saved_restaurant'] = saved_restaurant.first()            

        company_start_hour = company.values('work_hours_from').first().get('work_hours_from')
        company_finish_hour = company.values('work_hours_to').first().get('work_hours_to')
        
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
        context["work_hours"] = free_times

        reserve_start_date = datetime.date.today()
        reserve_finish_date = (datetime.date.today()+datetime.timedelta(days=30)).isoformat()
        context['reserve_start_date'] = reserve_start_date
        context['reserve_finish_date'] = reserve_finish_date

        inside_tables = Table.objects.filter(company=company.values('user').first().get('user'), table_place='inside')
        outside_tables = Table.objects.filter(company=company.values('user').first().get('user'), table_place='outside')  

        inside_tables_sizes = []
        outside_tables_sizes = []

        for table in inside_tables:
            if table.size not in inside_tables_sizes:
                inside_tables_sizes.append(table.size)
        
        for table in outside_tables:
            if table.size not in outside_tables_sizes:
                outside_tables_sizes.append(table.size)

        context['inside_tables_sizes'] = inside_tables_sizes
        context['outside_tables_sizes'] = outside_tables_sizes

        menus = Menu.objects.filter(company=company.values('user').first().get('user'))
        context['menus'] = menus
        context['menu_categories'] = MenuCategory.objects.all()
        
        reserve_dates = []

        for i in range(31):
            reserve_dates.append(reserve_start_date)
            reserve_start_date = (reserve_start_date+datetime.timedelta(days=1))
        
        
        return context
       

    def post(self, request, *args, **kwargs):

        if request.method == 'POST':
                
            if request.POST.get('form_id') == 'FindTableForm':
                company = Company.objects.filter(pk=self.kwargs.get('pk'))

                

                party_size = request.POST.get('size')
                reserve_date = request.POST.get('date')
                reserve_time = request.POST.get('time')

                table_place = request.POST.get('table_place')
             
                party_size = int(party_size)
                reserve_date_obj = datetime.datetime.strptime(reserve_date, '%Y-%m-%d')
                reserve_time_obj = datetime.datetime.strptime(reserve_time, '%H:%M:%S').time()

                company_start_hour = company.first().work_hours_from

                reserve_start_date = datetime.date.today()
                reserve_finish_date = (datetime.date.today()+datetime.timedelta(days=30)).isoformat()
            
                reserve_dates = []
                for i in range(31):
                    reserve_dates.append(reserve_start_date)
                    reserve_start_date = (reserve_start_date+datetime.timedelta(days=1))

                response_data = {}
                
                tables = Table.objects.filter(company=company.values('user').first().get('user'), table_place=table_place, size=party_size)   
                thirty_minutes_less = (datetime.datetime.combine(datetime.date(1, 1, 1),reserve_time_obj) - datetime.timedelta(minutes=30)).time()
                thirty_minutes_great = (datetime.datetime.combine(datetime.date(1, 1, 1),reserve_time_obj) + datetime.timedelta(minutes=30)).time()

               

                for table in tables:
                    dates = table.dates.filter(date=reserve_date_obj)
                    for date in dates:
                        times = date.times.filter(reserved=False)
                        for time in times:
                            if reserve_time_obj != company_start_hour and thirty_minutes_less in times.values_list('free_time', flat=True) and thirty_minutes_great in times.values_list('free_time', flat=True) and reserve_time_obj == time.free_time:
                                print('okk')
                                found_result = {
                                    'table' : table,
                                    'time' : reserve_time_obj,
                                    'time_id' : time.id,
                                    'table_size' : party_size,
                                    'table_id' : table.id,
                                    'table_place' : table.table_place,
                                    'reserved_date' : reserve_date_obj
                                }
                                response_data['found_result'] = found_result
                                break

                            elif reserve_time_obj == company_start_hour and reserve_time_obj == time.free_time:
                                found_result = {
                                    'table' : table,
                                    'time' : time.free_time,
                                    'time_id' : time.id,
                                    'table_size' : party_size,
                                    'table_id' : table.id,
                                    'table_place' : table.table_place,
                                    'reserved_date' : reserve_date_obj
                                }
                                response_data['found_result'] = found_result
                                break

                            else:
                                response_data['not_found'] = 'We dont have any table in the particular time...'

               

                return HttpResponse(
                    json.dumps(response_data, indent=4, sort_keys=True, default=str),
                    content_type="application/json"
                )

            elif request.POST.get('form_id') == 'selectMenuForm':
                company = Company.objects.filter(pk=self.kwargs.get('pk'))

                reserve_date = request.POST.get('reserve_date')
                reserve_time = request.POST.get('reserve_time')
                table_id = request.POST.get('table_id')
                table = Table.objects.filter(pk=table_id)

                reserve_date_obj = datetime.datetime.strptime(reserve_date, '%Y-%m-%d')
                reserve_time_obj = datetime.datetime.strptime(reserve_time, '%H:%M:%S').time()
                total_price = request.POST.get('total_price')

                table = Table.objects.filter(pk=table_id)

                for date in table.first().dates.filter(date=reserve_date_obj):
                    date.times.filter(free_time=reserve_time_obj).update(reserved=True)

                response_data = {
                   
                }

                reservation = Reservation.objects.create(
                    user=request.user, 
                    company=company.first(), 
                    table_id=table_id, 
                    reserved_time= reserve_time_obj,
                    reserved_date=reserve_date_obj,
                    total_price = total_price
                )

                response_data['reservation_id'] = reservation.pk

                Notification.objects.create(
                    sender=request.user,
                    reciever=company.first().user, 
                    text = 'You have new reservation',
                    notified_at = datetime.datetime.now(),
                    notification_type = 'new_reservation'
                )   
                
                after_one_hour = (datetime.datetime.combine(datetime.date(1, 1, 1),reserve_time_obj) + datetime.timedelta(hours=1)).time()
                eta_date_time = datetime.datetime.combine(reserve_date_obj, after_one_hour)
                tomorrow = datetime.datetime.utcnow() + datetime.timedelta(minutes=1)

                # complete_reserve.apply_async(args=[reserve_time_obj, reserve_date_obj.date(), table_id], eta=eta_date_time)
                give_feedback.apply_async(args=[company.first().id, request.user.email], eta = eta_date_time)
                
                
                for i in range(0,int(request.POST.get('length'))):
                    menu_id = int(request.POST.get(f'selected_menus_list[{i}][menu_id]'))
                    portion_count = int(request.POST.get(f'selected_menus_list[{i}][portion_count]'))

                    portion = Portion.objects.create(menu_id=menu_id, portion_count=portion_count)
                    reservation.portions.add(portion)
                    

                return HttpResponse(
                    json.dumps(response_data, indent=4, sort_keys=True, default=str),
                    content_type="application/json"
                )
            
            elif request.POST.get('form_id') == 'saveRestaurantForm':
                company = Company.objects.filter(pk=self.kwargs.get('pk'))

                response_data = {}

                if request.user.is_authenticated:
                    if(SavedRestaurant.objects.filter(user=request.user, company=company.first())):
                        saved_restaurant = SavedRestaurant.objects.filter(company=company.first(), user=request.user)
                        if saved_restaurant.first().saved:
                            saved_restaurant.update(saved=False)    
                            response_data['saved'] = 'false'
                            response_data['text'] = 'Save this restaurant'
                        else:
                            saved_restaurant.update(saved=True)
                            response_data['saved'] = 'true'
                            response_data['text'] = 'Restaurant saved!'
                    else:
                        saved_restaurant = SavedRestaurant.objects.create(company=company.first(), user=request.user, saved=True)
                        response_data['saved'] = 'true'
                        response_data['text'] = 'Restaurant saved!'

                

                return HttpResponse(
                    json.dumps(response_data, indent=4, sort_keys=True, default=str),
                    content_type="application/json"
                )

            
        else:
            return HttpResponse(
                json.dumps({"nothing to see": "this isn't happening"}),
                content_type="application/json"
            )

        
class SavedRestaurantsView(ListView):
    model = SavedRestaurant
    template_name = "user-saved-restaurants.html"
    context_object_name = 'saved_restaurants'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saved_restaurants = SavedRestaurant.objects.filter(user=self.request.user, saved=True)
        company_list = []
        for saved_restaurant in saved_restaurants:
            comments = saved_restaurant.company.company_comment.all()
            company_overall = comments.aggregate(Avg('overall'))

            if company_overall.get('overall__avg', 0):
                company_rating = int(company_overall.get('overall__avg', 0))
                company_dict = {
                    'saved_restaurant' : saved_restaurant,
                    'reservation_count' : saved_restaurant.company.reservation.filter(reserved_at=datetime.date.today()).count(),
                    'company_overall' : company_rating
                }
            else:
                company_dict = {
                    'saved_restaurant' : saved_restaurant,
                    'reservation_count' : saved_restaurant.company.reservation.filter(reserved_at=datetime.date.today()).count(),
                    'company_overall' : 0
                }
            company_list.append(company_dict)
        
        context['saved_restaurants'] = company_list
        return context
    

class CompanyCategoryList(ListView):
    context_object_name = 'companies'
    template_name='company-list.html'
    model = Company
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        companies_list = []
        for company in companies:
            company_obj = {
                'company' : company,
                'reservation_count' : company.reservation.filter(reserved_at=datetime.date.today()).count(),
            }
            companies_list.append(company_obj)
        context["comments"] = companies_list
        print(Company.objects.distinct('city_location').get(city_location=self.kwargs['city_location']))
        context['company'] = Company.objects.distinct('city_location').get(city_location=self.kwargs['city_location'])
        return context


    def get_queryset(self):
        self.queryset2 = Company.objects.distinct('city_location').get(city_location=self.kwargs['city_location'])
        queryset2 =  Company.objects.filter(city_location=self.queryset2.city_location)
        if self.request.method == 'GET':
            queryset1 = Company.objects.filter(city_location=self.queryset2.city_location)
            title_name = self.request.GET.get('q', None)
            if title_name is not None:
                queryset1 = queryset1.filter(company_name__icontains=title_name)
                return queryset1
        
        return queryset2
  

class CompanyFilterView(ListView):
    model = Company
    template_name = "company-filter.html"
    context_object_name = 'companies'
    show_change_link = True
    
    def get_queryset(self):
        # queryset = super().get_queryset()
        self.queryset = Company.objects.distinct('city_location').get(city_location=self.kwargs['city_location'])
        queryset =  Company.objects.filter(city_location=self.queryset.city_location)
        sort_data = self.request.GET.get('companySort')
        if sort_data == 'newest':
            return queryset.order_by('-created_at')
        elif sort_data == 'highest':
            return queryset.order_by('-overall')
        elif sort_data == 'lowest':
            return queryset.order_by('overall')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        companies_list = []
        for company in companies:
            company_obj = {
                'company' : company,
                'reservation_count' : company.reservation.filter(reserved_at=datetime.date.today()).count(),
            }
            companies_list.append(company_obj)
        context["comments"] = companies_list
        print(Company.objects.distinct('city_location').get(city_location=self.kwargs['city_location']))
        context['company'] = Company.objects.distinct('city_location').get(city_location=self.kwargs['city_location'])
        return context


class CompanyCuisineListView(ListView):
    context_object_name = 'companies'
    model = Cuisine
    template_name = "cuisines-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        companies_list = []
        for company in companies:
            company_obj = {
                'company' : company,
                'rating' : company.company_comment.all().aggregate(Avg('overall')).get('overall__avg', 0),
            }
            companies_list.append(company_obj)

        context["comments"] = companies_list
        context['cuisine'] = self.kwargs['cuisine']
        print(Cuisine.objects.distinct('title').get(title=self.kwargs['cuisine']))
        context['cuisine'] = Cuisine.objects.distinct('title').get(title=self.kwargs['cuisine'])

        return context

    def get_queryset(self):
        self.cuisine = get_object_or_404(Cuisine, title=self.kwargs['cuisine'])
        if self.request.method == 'GET':
            queryset1 = Company.objects.filter(cuisine=self.cuisine)
            title_name = self.request.GET.get('q', None)
            if title_name is not None:
                queryset1 = queryset1.filter(company_name__icontains=title_name)
                return queryset1
        
        return Company.objects.filter(cuisine=self.cuisine)

 
class CuisineFilterView(ListView):
    model = Cuisine
    template_name = "cuisine-filter.html"
    context_object_name = 'companies'
    show_change_link = True
    
    def get_queryset(self):
        # queryset = super().get_queryset()
        self.cuisine = get_object_or_404(Cuisine, title=self.kwargs['cuisine'])
        queryset = Company.objects.filter(cuisine=self.cuisine)
        sort_data = self.request.GET.get('cuisineSort')
        if sort_data == 'newest':
            return queryset.order_by('-created_at')
        elif sort_data == 'highest':
            return queryset.order_by('-overall')
        elif sort_data == 'lowest':
            return queryset.order_by('overall')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        companies = Company.objects.all()
        companies_list = []
        for company in companies:
            company_obj = {
                'company' : company,
                'reservation_count' : company.reservation.filter(reserved_at=datetime.date.today()).count(),
            }
            companies_list.append(company_obj)
        context["comments"] = companies_list
        context['cuisine'] = Cuisine.objects.distinct('title').get(title=self.kwargs['cuisine'])

        return context
        

class PaymentView(DetailView, LoginRequiredMixin):
    model = Reservation
    context_object_name = 'reservation'
    template_name = "payment.html"


def charge(request):
    
    if request.method == 'POST':

        reservation = Reservation.objects.filter(id=int(request.POST['reservation_id']))
        
        reservation.update(
            payment=True,
            phone_number = request.POST['phone'],
            occasion = request.POST['occasion'],
            special_request = request.POST['special_request']
        )

        print(request.POST)
        customer = stripe.Customer.create(
            name = request.POST['username'],
            email = request.user.email,
            source = request.POST['stripeToken']
        )

        total_price = int(request.POST['total_price'])

        stripe.Charge.create(
            customer = customer,
            amount=total_price*100,
            currency="usd",
            description="Reservation payment",
        )
    return redirect(reverse('core:payment-success'))


class SuccessView(TemplateView):
    template_name = "payment-success.html"
