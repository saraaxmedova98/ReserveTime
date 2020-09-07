from django.urls import path
from restaurant.views import *

app_name = 'restaurant'

urlpatterns = [
    path('register', RestaurantRegisterView.as_view(), name='company-regsiter'),
    path("menus", MenuView.as_view(), name="menu"),
    path("menus/<int:pk>/update", MenuUpdateView.as_view(), name="menu-update"),
    path("menus/<int:pk>/delete", MenuDeleteView.as_view(), name="menu-delete"),
    path("photos", PhotoView.as_view(), name="photo"),
    path("photos/<int:pk>/update", PhotoUpdateView.as_view(), name="photo-update"),
    path("photos/<int:pk>/delete", PhotoDeleteView.as_view(), name="photo-delete"),
    path("<int:pk>/informations", CompanyInfosView.as_view(), name="company-infos"),
    path("<int:pk>/tables", CompanyTablesView.as_view(), name="company-tables"),
    path("tables/<int:pk>/delete", TableDeleteView.as_view(), name="table-delete"),
    path("<int:pk>/users", ResevedUserList.as_view(), name="company-users"),
    path("<int:pk>/reservations", CompanyReservations.as_view(), name="company-reservations"),
    path("<int:pk>/reviews", CompanyReviews.as_view(), name="company-reviews"),
    path("reservation/<int:pk>", ReservationDetail.as_view(), name="reservation-detail"),
    # path("reservation/<int:pk>", AcceptReservation.as_view(), name='accept-reservation'),
    path("<int:pk>/comment", CommentView.as_view(), name="write-comment")
]