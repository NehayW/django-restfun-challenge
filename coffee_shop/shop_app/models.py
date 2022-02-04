""" shop_app/models.py """
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class UserAccountManager(BaseUserManager):
    def create_user(self,  email, name, password=None):
        if not email:
            raise ValueError('user must have an email')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.role = UserAccount.SUPER_ADMIN
        user.set_password(password)
        user.save()
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    SUPER_ADMIN = 0
    MANAGER = 1
    SHOP = 2
    CUSTOMER = 3

    INACTIVE = 'INACTIVE'
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'

    USER_STATUSES = (
        (INACTIVE, 'Inactive'),
        (ACTIVE, 'Active'),
        (DELETED, 'Deleted')
    )

    ROLE_TYPES = (
        (SUPER_ADMIN, 'SUPER_ADMIN'),
        (MANAGER, 'MANAGER'),
        (SHOP, 'SHOP'),
        (CUSTOMER, 'CUSTOMER')
    )

    role = models.IntegerField(choices=ROLE_TYPES, default=3)
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=USER_STATUSES, default=ACTIVE)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)


class ShopOptionValue(models.Model):
    value_name = models.CharField(max_length=255, null=True, blank=True)


class ShopOptionType(models.Model):
    option_value = models.ManyToManyField(ShopOptionValue)
    type_name = models.CharField(max_length=255, null=True, blank=True)


class ShopItem(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    option = models.ManyToManyField(ShopOptionType)
    description = models.TextField(null=True, blank=True)


class OrderItem(models.Model):
    shop_item = models.ForeignKey(ShopItem, null=True, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=255, null=True, blank=True)
    option = models.CharField(max_length=255, null=True, blank=True)


class Order(models.Model):
    ORDER_CHOICE = (
        ('WAITING', 'WAITING'),
        ('PREPARATION', 'PREPARATION'),
        ('READY', 'READY'),
        ('DELIVERED', 'DELIVERED'),
        ('CANCEL', 'CANCEL'),
    )
    customer = models.ForeignKey(UserAccount, null=True, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    status = models.CharField(max_length=255, null=True, blank=True, choices=ORDER_CHOICE)
    total_bill = models.CharField(max_length=255, null=True, blank=True)
