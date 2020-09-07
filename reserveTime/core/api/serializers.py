from rest_framework import serializers
from account.models import *
from restaurant.models import *


from django.contrib.auth import get_user_model
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile_img']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name','username','email', 'password']

        def create(self, validated_data):
            user = User.objects.create(
                first_name = validated_data['first_name'],
                last_name = validated_data['last_name'],
                username = validated_data['username'],
                email = validated_data['email']
            )
            password = validated_data['password']
            user.set_password(password)
            user.save()
            return user


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'company_name','phone_number','city_location','province_location','country_location','work_hours_from','work_hours_to','cuisines','dining_style','parking_details','public_transit','payment_options','executive_chef','website','private_party_contact','description']


class TableSerializer(serializers.ModelSerializer):

    class Meta:
        model = Table
        fields = ['id','company','size','table_place']


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['id', 'company','title','price','description','menu_type']


class MenuCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = MenuCategory
        fields = ['id', 'title']


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'owner',"photo",'photo_url','photo_type',]


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id','company','user','text','commented_at','raiting']


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id','company','user','table_id','reserved_time','reserved_date', 'total_price', 'accessed', 'denied']

class SavedRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavedRestaurant
        fields = ['id','company','user','saved']

class PortionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Portion
        fields = ['id','menu_id','portion_count']

class TimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Time
        fields = ['id','free_time','reserved']