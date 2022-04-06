from rest_framework import serializers
from .models import *
from django.conf import settings
import boto3
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'name', 'image', 'price', 'description', 'stock']

    # Update Return Serializer
    def to_representation(self, instance):

        s3 = boto3.resource('s3')

        url = str("https://" + str(settings.AWS_STORAGE_BUCKET_NAME) + ".s3." +
                  str(settings.AWS_S3_REGION_NAME) + ".amazonaws.com/" + str(instance.image))

        print(url)
        self.file = url
        return {
            'id' : instance.id,
            'category': instance.category.name,
            'name': instance.name,
            'image': url,
            'price': instance.price,
            'description': instance.description,
            'stock': instance.stock,
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class EmailOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password', None)  # Get Password
        user = self.Meta.model(**validated_data)  # User Model
        user.username = validated_data.pop('email', None)
        user.is_active = False

        if(password is not None):
            user.set_password(password)
            user.save()
        return user


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'



