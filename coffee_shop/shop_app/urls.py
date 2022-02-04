from django.urls import path
from . import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('customer-registration', views.CustomerRegistration.as_view(), name='customer-registration'),
    path('view-menu', views.ViewMenu.as_view(), name='view-menu'),
    path('order-item', views.OrderItems.as_view(), name='order-item'),
    path('cancel-order/<pk>', views.CancelOrder.as_view(), name='cancel-order'),
    path('change-order/<pk>', views.ChangeOrder.as_view(), name='change-order'),
    path('', views.manager_login, name='manager_login'),
    path('signup', views.signup, name='signup'),
    path('change-order-status', views.change_order_status, name='signup'),

]
