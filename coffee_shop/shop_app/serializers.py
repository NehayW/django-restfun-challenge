from rest_framework import serializers
from . models import *


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAccount
		fields = ('email', 'name', 'role', 'password', )


class UserSerializerView(serializers.ModelSerializer):
	class Meta:
		model = UserAccount
		fields = ('email', 'name', 'role',)


class OptionValueSerializer(serializers.ModelSerializer):
	class Meta:
		model = ShopOptionValue
		fields = ('value_name',)


class OptionTypeSerializer(serializers.ModelSerializer):
	option_value = OptionValueSerializer(many=True)
	class Meta:
		model = ShopOptionType
		fields = ('type_name', 'option_value')


class ShopItemSerializer(serializers.ModelSerializer):
	option = OptionTypeSerializer(many=True)
	class Meta:
		model = ShopItem
		fields = ('name', 'price', 'option', 'description',)


class OrderItemSerializer(serializers.ModelSerializer):
	shop_item = ShopItemSerializer()
	class Meta:
		model = OrderItem
		fields = ('shop_item', 'quantity',)


class OrderSerializer(serializers.ModelSerializer):
	customer = UserSerializerView()
	items = OrderItemSerializer(many=True)
	class Meta:
		model = Order
		fields = ('customer', 'items', 'status', 'total_bill',)