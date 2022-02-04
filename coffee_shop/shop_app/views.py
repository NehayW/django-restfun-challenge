from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.db import transaction
from django.contrib.auth.hashers import make_password
from coffee_shop.settings import EMAIL_HOST_USER
from . models import *
from . serializers import UserSerializerView, UserSerializer, ShopItemSerializer, \
                         OrderSerializer
from . utils import Messages
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from cerberus import Validator
from django.shortcuts import render, redirect
from django.http import JsonResponse
# Create your views here.


def change_order_status(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_object = Order.objects.filter(pk=data.get("order_id"))
        order_object.update(status=data.get("status"))
        email = EmailMultiAlternatives('Order status', 'Order Status',
                                        EMAIL_HOST_USER,
                                        [order_object.first().customer.email])
        email.attach_alternative(html_content, 'text/html')
        email.send()
        return JsonResponse()


def manager_login(request):
    """login for user"""
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            order_object = Order.objects.all()
            return render(request, 'home.html', {"order": order_object})
            return render(request, 'home.html')
        else:
            messages.info(request, 'Invalid Email and password')
    else:
        if request.user.is_authenticated:
            order_object = Order.objects.all()
            return render(request, 'home.html', {"order": order_object})
        else:
            return render(request, 'admin_login.html')
    return render(request, 'admin_login.html')

def signup(request):
    """Manager can register it self"""
    if request.method == 'POST':
        email = request.POST['username']
        password = make_password(request.POST['password'])
        name = request.POST['name']
        user = UserAccount.objects.filter(email=email)
        if not user.exists():
            UserAccount.objects.create(email=email,
                                   password=password,
                                   name=name,
                                   role=1)
            return render(request, 'admin_login.html')
        messages.info(request, 'Email already exists!')
    return render(request, 'signup.html')


class LogoutView(APIView):
    def post(self, request):
        """Logout api for all users"""
        tokens = request.headers['Authorization']
        s = tokens.split()
        token = Token.objects.get(key=s[1])
        # user_object = UserAccount.objects.filter(pk=request.user.pk).update(device_id="")
        user_object = UserAccount.objects.filter(pk=request.user.pk)
        token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)


@permission_classes((AllowAny, ))
class LoginView(APIView):
    def post(self, request):
        """Login api for all users"""
        data = request.data
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        user_object = UserAccount.objects.filter(email=email)
        if user_object.exists():
            if user_object.first().status == "DELETED":
                return Response({"error": Messages.ACCOUNT_DELETED}, status=status.HTTP_400_BAD_REQUEST)
            if user_object.first().status == "INACTIVE":
                return Response({"error": Messages.ACCOUNT_NOT_ACTIVE}, status=status.HTTP_400_BAD_REQUEST)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if request.data.get('device_id'):
                user_object.update(device_id=request.data.get('device_id'))
            return Response({'token': token.key, "role": request.user.role}, status=status.HTTP_200_OK)
        return Response({"error": Messages.WRONG_CREDENTIALS}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((AllowAny, ))
class CustomerRegistration(APIView):
    def post(self, request):
        """Customer can register"""
        try:
            # Validate the request
            schema = {
                "name": {'type': 'string', 'required': True, 'empty': False},
                "email": {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                          'required': True, 'empty': False},
                "password": {'type': 'string', 'required': False, 'empty': False},
            }
            v = Validator()
            if not v.validate(request.data, schema):
                return Response(
                    {'error': v.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user_object = UserAccount.objects.filter(email=request.data.get('email'))
            if user_object.exists():
                return Response({"error": "This email already exists!"}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                user_data = UserAccount.objects.create(
                    name=request.data.get('name'),
                    email=request.data.get('email'),
                    password=make_password(request.data.get('password')),
                    role=3
                )
            return Response({"message": "Your Account created successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ViewMenu(APIView):
    def get(self, request):
        product_object = ShopItem.objects.all()
        serializer = ShopItemSerializer(product_object, many=True).data
        return Response(serializer, status=status.HTTP_200_OK)

 
class OrderItems(APIView):
    def get(self, request):
        order_object = Order.objects.filter(customer=request.user)
        order_serializer = OrderSerializer(order_object, many=True).data
        return Response(order_serializer, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            # Validate the request
            schema = {
                "items": {
                    'type': 'list', 'schema': {
                        'type': 'dict', 'schema': {
                            'id': {'type': 'string', 'required': True, 'empty': False},
                            'quantity': {'type': 'integer', 'required': True, 'empty': False},
                            'option': {'type': 'string', 'required': True, 'empty': False},
                        }
                    }, 'required': True, 'empty': False
                },
            }
            v = Validator()
            if not v.validate(request.data, schema):
                return Response(
                    {'error': v.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            total_price = 0
            for data in request.data['items']:
                item_data = ShopItem.objects.filter(pk=data['id'])
                if not item_data.exists():
                    return Response({"error": "Product not found"})
                total_price = total_price + int(item_data.first().price)*data['quantity']
            
            with transaction.atomic():
                order_object = Order.objects.create(
                    customer=request.user,
                    status='WAITING'
                )
                for data in request.data['items']:
                    item_object = OrderItem.objects.create(
                        shop_item_id=data['id'],
                        quantity=data['quantity'],
                        option=data['option']
                    )
                    item_id = OrderItem.objects.latest('pk')
                    order_object.items.add(item_id)
            order_object.total_bill = total_price
            order_object.save()
            return Response({"message": "Order successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CancelOrder(APIView):
    def post(self, request, pk):
        try:
            order_object = Order.objects.filter(pk=pk)
            if not order_object.exists():
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            if order_object.first().status != "WAITING":
                return Response({"error": "You can not change order status"}, status=status.HTTP_400_BAD_REQUEST)
            order_object.update(status="CANCEL")
            return Response({"message": "Order cancel successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangeOrder(APIView):
    def post(self, request, pk):
        try:
            # Validate the request
            schema = {
                "items": {
                    'type': 'list', 'schema': {
                        'type': 'dict', 'schema': {
                            'replaced_id': {'type': 'string', 'required': True, 'empty': False},
                            'id': {'type': 'string', 'required': True, 'empty': False},
                            'quantity': {'type': 'integer', 'required': True, 'empty': False},
                            'option': {'type': 'string', 'required': True, 'empty': False},
                        }
                    }, 'required': True, 'empty': False
                },
            }
            v = Validator()
            if not v.validate(request.data, schema):
                return Response(
                    {'error': v.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )
            order_object = Order.objects.filter(pk=pk)
            if not order_object.exists():
                return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
            if order_object.first().status != "WAITING":
                return Response({"error": "You can not change order"}, status=status.HTTP_400_BAD_REQUEST)
            total_bill = 0
            for data in request.data['items']:
                item_data1 = ShopItem.objects.filter(pk=data['id'])
                if not item_data1.exists():
                    return Response({"error": "Product not found"})
            with transaction.atomic():
                for data in request.data['items']:
                    item_data = OrderItem.objects.filter(shop_item_id=data['replaced_id'])
                    order_object.update(total_bill=int(order_object.first().total_bill)-(int(item_data.first().shop_item.price)*int(item_data.first().quantity)))
                    item_data1 = ShopItem.objects.get(pk=data['id'])
                    item_data.update(
                        shop_item_id=data['id'],
                        quantity=data['quantity'],
                        option=data['option']
                    )
                    order_object.update(total_bill=int(order_object.first().total_bill)+(int(item_data1.price)*data['quantity']))
            return Response({"message": "Order changed successfully!"}, status=status.HTTP_201_CREATED)
        except Exception as exception:
            return Response({"error": str(exception)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
