from rest_framework import status
from account.models import *
from core.api.serializers import *
                        
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework import generics
from rest_framework import permissions
from core.api.permissions import IsOwnerOrReadOnly

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from rest_framework import viewsets
from rest_framework.decorators import action

from django.contrib.auth import get_user_model
User = get_user_model()




class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserRegisterView(CreateAPIView):
    model = User
    serializer_class = RegisterSerializer
    

class CompanyViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class TableViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class MenuViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

class MenuCategoryViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer

class PhotoViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

class SavedRestaurantViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = SavedRestaurant.objects.all()
    serializer_class = SavedRestaurantSerializer

class PortionViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Portion.objects.all()
    serializer_class = PortionSerializer

class TimeViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Time.objects.all()
    serializer_class = TimeSerializer