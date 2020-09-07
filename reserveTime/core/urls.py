from django.urls import path
from core.views import *

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view() , name='home'),
    path("readNotifications/", ReadNotifications.as_view(), name="read-notifications"),
    path("company/profile/<int:pk>", CompanyProfile.as_view(), name="company-profile"),
    path("company/<int:pk>/filter", CommentFilterView.as_view(), name="comment-filter"),
    path("user/<int:pk>/savedRestaurants", SavedRestaurantsView.as_view(), name="user-saved-restaurants"),
    path("companies/<city_location>", CompanyCategoryList.as_view(), name="city-categories"),
    path("companies/<city_location>/filter", CompanyFilterView.as_view(), name="company-filter"),
    path("company_list/<cuisine>", CompanyCuisineListView.as_view(), name="company-cuisine"),
    path("company_list/<cuisine>/filter", CuisineFilterView.as_view(), name="cuisine-filter"),
    path("company/register/compelted", RegisterCompleted.as_view(), name="register-completed"),
    path("reservation/<int:pk>/payment", PaymentView.as_view(), name="payment"),
    path("charge/", charge, name="charge"),
    path("payment/success", SuccessView.as_view(), name="payment-success"),
]