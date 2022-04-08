import random
import uuid
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters

from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from .serializers import *
from .models import *

from django.conf import settings
from django.core.mail import send_mail

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import *

from rest_framework.views import APIView
from rest_framework_simplejwt.backends import TokenBackend
from django.core.mail import send_mail
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate
# Category

from django.utils import six
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.hashers import check_password
from datetime import datetime, timedelta

from modules import awsSns, otpMail

class CategoryList(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        return Response(self.serializer_class(Category.objects.all(), many=True).data)

    def post(self, request):

        if request.user.is_superuser:
            newObj = Category.objects.create(**request.data)
            serializer = self.serializer_class(newObj)
            return Response(serializer.data, status=201)
        else:
            return Response({'message': 'Not authorized', 'status': 401})


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def patch(self, request, pk):
        if request.user.is_superuser:
            obj = Category(pk=pk)
            serializer = CategorySerializer(
                obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=204)
        else:
            return Response({'message': 'Not authorized', 'status': 401})

    def delete(self, request, pk):
        if request.user.is_superuser:
            Category(pk=pk).delete()
            return Response(status=300)
        else:
            return Response({'message': 'Not authorized', 'status': 401})


# Product
class ProductList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']  # Search Filter DRF
    def get(self, request):        
        return Response(self.serializer_class(Product.objects.all(), many=True).data)

    def post(self, request):
        print(request.data.get('category'))
        if request.user.is_superuser:
            category = Category.objects.filter(
                id=request.data.get('category')).first()
            newObj = Product(category=category, name=request.data.get('name'), image=request.data.get(
                'image'), price=request.data.get('price'), description=request.data.get('description'))
            newObj.save()
            serializer = self.serializer_class(newObj)
            return Response(serializer.data, status=201)
        else:
            return Response({'message': 'Not authorized', 'status': 401})


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def patch(self, request, pk):
        if request.user.is_superuser:
            obj = Product(pk=pk)
            serializer = ProductSerializer(
                obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=204)
        else:
            return Response({'message': 'Not authorized', 'status': 401})

    def delete(self, request, pk):
        if request.user.is_superuser:
            Product(pk=pk).delete()
            return Response(status=300)
        else:
            return Response({'message': 'Not authorized', 'status': 401})


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
        except Exception as error:
            return Response({'message' : 'Email Already Registered', 'status':400})

        user = User.objects.filter(email=request.data.get('email')).first()
        context = {
            "SMS_TO"  : request.data['sms_to'],
            "MESSAGE" : request.data['message'],
        }

        # SNS Method
        result = awsSns.AWS_SNS.sendSms(context)
        OTP.objects.create(otp=result[1],user=user) #storing OTP in db
        user = UserSerializer(user)
        if result[0]['ResponseMetadata']['HTTPStatusCode'] == 200:
            # context = request.data
            context['email'] = request.data['email']
            context['otp'] = result[1]
            context['subject'] = 'Register Mail.'
            context['otp_body'] = 'Register email otp body will be here'
            context['otp_text'] = 'Register email otp text will be here'
            customMail = otpMail.OTP_MAIL.sendMailTemplate(context)
            return Response({
                "user": user.data,
                'msg': 'Please verify your email address via OTP sent.',
                'status': 201})

        return Response({
                "user": user.data,
                'msg': 'OTP not sent.',
                'status': 400})


class EmailOTPVerifyView(APIView):
    serializer_class = EmailOTPSerializer

    def post(self, request):

        if not (request.data.get('id') and request.data.get('otp')):
            return Response({'message': 'Fill all fields', 'status':400}, status=400)

        user = User.objects.filter(id=request.data.get('id')).first()
        if not user:
            return Response({'message': 'No user', 'status':400}, status=400)
        
        if user.is_active:
            return Response({'message': 'Already an active user', 'status':400}, status=400)


        otp = OTP.objects.filter(user=user)#.reverse().first()
        if otp.exists():
            otp = otp.reverse().first()
            # Check OTP Validation 
            otp_time = datetime.strptime(str(otp.timestamp)[:19], "%Y-%m-%d %H:%M:%S")
            current_time = datetime.strptime(str(datetime.now())[:19], "%Y-%m-%d %H:%M:%S")
            diff = (current_time - otp_time).total_seconds() / 60
            if diff > int(settings.OTP_TIME_OUT):
                return Response({'message': 'OTP Expired', 'status':400}, status=400)

            if str(otp.otp) == str(request.data.get('otp')):
                user.is_active = True
                user.save()

                refresh = RefreshToken.for_user(user)  # Get Token
                userObj = User.objects.filter(id=request.data.get('id')).first()

                user = UserSerializer(user)
                # otp = request.data['otp']
                context = {}
                context['otp'] = request.data['otp']
                context['email'] = userObj
                context['subject'] = 'Verify OTP Mail.'
                context['otp_body'] = 'verify email otp body will be here'
                context['otp_text'] = 'verify email otp text will be here'
                customMail = otpMail.OTP_MAIL.sendMailTemplate(context)
                return Response({
                    "user": user.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'status': 201})
            else:
                return Response({
                    'message': 'Invalid OTP',
                    'status': 404})
        else:
            return Response({
                'message': 'Invalid OTP',
                'status': 404})


class LoginAPI(APIView):
    def post(self, request):
        print(request.data)

        Account = User.objects.get(username=request.data['username'])

        if not check_password(request.data['password'], Account.password):
            return Response({
                "message": "invalid credentials",
                'status': 400})
        elif Account.is_active:
            user = UserSerializer(Account)
            refresh = RefreshToken.for_user(Account)  # Get Token

            return Response({
                "user": user.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'status': 201})

        else:
            return Response({
                "message": "Please verify your account",
                'status': 400})

            # No backend authenticated the credentials
# Cart APIViews


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get(self, request):
        print(self.request.user)
        cartObj = Cart.objects.filter(
            user=self.request.user, Isordered=False).first()
        if cartObj:
            cartObj = self.serializer_class(cartObj)
            return Response(cartObj.data)
        else:
            return Response([], status=404)


# Cart Items
class CartItemListView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get(self, request):

        print(self.request.user)
        cartObj = Cart.objects.filter(
            user=request.user, Isordered=False).first()
        print("Cart : ", cartObj.Isordered)
        if cartObj is not None:
            cartItemObj = CartItem.objects.filter(
                user=self.request.user, cart=cartObj.id)
        else:
            cartItemObj = CartItem.objects.filter(user=self.request.user)

        print(cartItemObj)
        if cartItemObj:
            cartItemObj = self.serializer_class(cartItemObj, many=True)

            return Response(cartItemObj.data)
        else:
            return Response([])

    def post(self, request):
        cartObj = Cart.objects.filter(
            user=request.user.id, Isordered=False).first()
        print(cartObj)
        productObj = Product.objects.filter(id=request.data['product']).first()
        cartItemObj = CartItem(user=request.user, cart=cartObj, price=productObj.price,
                               quantity=request.data['quantity'], product=productObj)
        cartItemObj.save()
        cartItemObj = self.serializer_class(cartItemObj)
        return Response(cartItemObj.data)


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def patch(self, request, pk):
        cartItemObj = CartItem.objects.filter(pk=pk).first()
        if cartItemObj.user.id == request.user.id:
            cartItemObj.quantity = request.data['quantity']
            cartItemObj.save()
            return Response({'message': "Updated Cart Item", "status": 200})
        else:
            return Response({'error': "Updated Cart Failed", "status": 400})

    def delete(self, request, pk):
        cartItemObj = CartItem.objects.filter(pk=pk).first()
        if cartItemObj.user.id == request.user.id:
            cartItemObj.delete()
            return Response({'message': "Deleted Cart Item", "status": 200})
        else:
            return Response({'error': "Deleted Cart Failed", "status": 400})


# Signals Implementation


@receiver(pre_save, sender=CartItem)
def my_handler(sender, **kwargs):
    print('You Got Me ')

    # Get CardItem Model
    cartItemObj = kwargs['instance']
    priceofProduct = (Product.objects.get(id=cartItemObj.product.id)).price
    print(priceofProduct)
    cartItemObj.price = float(cartItemObj.quantity) * \
        float(priceofProduct)  # Calculate Total Price

    totalcartItems = CartItem.objects.filter(
        user=cartItemObj.user)  # Get All Items in Cart

    # Update User Cart
    cart = Cart.objects.get(id=cartItemObj.cart.id)
    cart.total += cartItemObj.price
    cart.save()


# Create CartItem

@receiver(post_save, sender=User)
def createCart(sender, **kwargs):
    print('User Created')
    user = kwargs['instance']
    print(user, type(user))

    obj = Cart.objects.filter(user=user, Isordered=False).reverse()
    print('Got cart')
    if len(obj) == 0:
        obj = Cart.objects.create(user=user)
        print('Created Cart')


# Order API

class OrderView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer

    def get(self, request):
        query = Order.objects.filter(user=request.user)
        serializer = self.serializer_class(query, many=True)
        return Response(serializer.data)

    def post(self, request):
        cartObj = Cart.objects.filter(
            user=request.user, Isordered=False).first()
        print(request.user, cartObj)
        orderId = str(uuid.uuid4())
        orderObj = Order(user=request.user, cart=cartObj, isPaid=request.data.get(
            'isPaid'), orderId=orderId, amount=cartObj.total)
        orderObj.save()
        orderObj = self.serializer_class(orderObj)

        # Cart Status True
        cartObj.Isordered = True
        cartObj.save()

        # Create New Cart For Current User
        cartObj = Cart.objects.create(user=request.user)
        print('Cart Created')
        return Response(orderObj.data)

    # def get(self, request, *args, **kwargs):
    #     print()

    #     # Decode Token
    #     token = request.META.get('HTTP_AUTHORIZATION')
    #     valid_data = TokenBackend(algorithm='HS256').decode(token,verify=False)
    #     print(valid_data)
    #     user = valid_data['user_id']
    #     user = User.objects.filter(id=user).first()
    #     print("User",user)
    #     cart = Cart.objects.filter(user=user).first()
    #     cart = CartSerializer(cart)
    #     return Response(cart.data)
# AKIAXLSZRNQVJTVCMCOX fnaciq71Dad6ThxxXrIYuXgXkBCoR3rPU8cHbMlz

        