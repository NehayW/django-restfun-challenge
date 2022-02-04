from django.contrib import admin
from .models import *


admin.site.register(UserAccount)

admin.site.register(Shop)

admin.site.register(ShopOptionValue)

admin.site.register(ShopOptionType)

admin.site.register(ShopItem)

admin.site.register(OrderItem)

admin.site.register(Order)
