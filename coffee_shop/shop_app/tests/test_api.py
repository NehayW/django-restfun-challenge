""" coffee_shop/test/test_api.py """
from rest_framework.test import APIClient, APITestCase
from shop_app.models import (
    UserAccount, ShopOptionValue, ShopOptionType, ShopItem,
    OrderItem, Order
)
from rest_framework.authtoken.models import Token
from django.urls import reverse
from shop_app.utils import Messages


class BaseTestCase(APITestCase):
    """
    This is BaseTestCase class
    """
    def create_user_object(self):
        self.email = "prakhardwi@gmail.com"
        self.name = "Prakhar Dwivedi"
        self.password = "Myadmin123"
        self.user_data = {
            'email': self.email,
            'name' : self.name,
            'password' : self.password
        }
        self.user = UserAccount.objects.create_user(**self.user_data)
        return self.user


    def login_user_func(self):
        login_url = reverse('login')
        self.login_data = {
            'password': self.password, 'email': self.email
        }
        response = self.client.post(login_url, self.login_data)
        self.token = response.json().get('token')

    def create_shop_option_value(self):
        self.shop_option_value = ShopOptionValue.objects.create(
                                    value_name="Coffee Shop")

    def create_shop_option_type(self):
        self.shop_option_type = ShopOptionType.objects.create(
                                    type_name="Coffee House")
        self.shop_option_type.option_value.add(self.shop_option_value)

    def create_shop_item_object(self):
        self.shop_item_object = ShopItem.objects.create(
                                    name="Coffee",
                                    price='20',
                                    description="Coffee description")
        self.shop_item_object.option.add(self.shop_option_type)

        self.shop_item_object1 = ShopItem.objects.create(
                                    name="Coffee",
                                    price='10',
                                    description="Coffee description2")
        self.shop_item_object1.option.add(self.shop_option_type)

    def create_order_item_object(self):
        self.order_item_object = OrderItem.objects.create(
                                            shop_item=self.shop_item_object,
                                            quantity='10',
                                            option='Coffee option')
        self.order_item_object2 = OrderItem.objects.create(
                                            shop_item=self.shop_item_object1,
                                            quantity='30',
                                            option='Coffee option')


class LoginAPITestCase(BaseTestCase):
    """
    This is Base Test Case Class
    """
    def setUp(self):
        self.create_user_object()
        self.client = APIClient()
        self.localhost = '127.0.0.1'
        self.login_url = reverse('login')
        self.login_data = {
            'password': self.password, 'email': self.email
        }

    def test_user_login_post_request_with_valid_data_status_code(self):
        """
        test user login post request.with valid data status_code
        """
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, 200)

    def test_user_login_post_request_with_valid_data_json_response(self):
        """
        test user login post request.with valid data
        """
        response = self.client.post(self.login_url, self.login_data)
        with self.subTest('Check token data'):
            self.assertTrue(response.json()['token'])
        with self.subTest('Check role data'):
            self.assertTrue(response.json()['role'])

    def test_user_login_post_request_with_invalid_url(self):
        """
        test user login post request.with invalid url
        """
        login_url = 'not_valid'
        response = self.client.post(login_url, self.login_data)
        self.assertEqual(response.status_code, 404)

    def test_user_login_post_request_with_invalid_login_data(self):
        """
        test user login post request.with invalid login data
        """
        login_data = {
            'email': 'testuser@gmail.com', 'password': 'testing321'
        }
        response = self.client.post(self.login_url, login_data)
        with self.subTest('Check status code'):
            self.assertEqual(response.status_code, 400)
        with self.subTest('Check response errors'):
            self.assertEqual(response.json()['error'], 'Wrong credentials are sent')

    def test_user_login_post_request_with_inactive_user_status_error_message(self):
        """
        test_user_login_post_request_with_invalid_user_status_error_message
        """
        self.user.status = UserAccount.INACTIVE
        self.user.save()
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.json()['error'], Messages.ACCOUNT_NOT_ACTIVE)

    def test_user_login_post_request_with_deleted_user_status_error_message(self):
        """
        test_user_login_post_request_with_invalid_user_status_error_message
        """
        self.user.status = UserAccount.DELETED
        self.user.save()
        response = self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.json()['error'], Messages.ACCOUNT_DELETED)


class LogoutAPITestCase(BaseTestCase):
    """
    This is logout api test case
    """

    def login_user_func(self):
        login_url = reverse('login')

        response = self.client.post(login_url, self.login_data)
        self.token = response.json().get('token')

    def setUp(self):
        self.create_user_object()
        self.client = APIClient()
        self.localhost = '127.0.0.1'
        # self.logout_url = f'{self.localhost}:5000/logout'
        self.logout_url = reverse('logout')
        self.login_data = {
            'password': self.password, 'email': self.email
        }

    def test_with_logged_in_user(self):
        self.login_user_func()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)

    def test_with_without_logged_in_user(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 401)

    def test_with_without_authorization(self):
        self.login_user_func()
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 401)


class CustomerRegistrationAPITestCase(BaseTestCase):
    """
    This is Base Test Case Class
    """
    def create_customer_object_data(self):
        self.email = 'johndoe@gmai.com'
        self.name = 'John Doe'
        self.user_data = {
            'email' : self.email,
            'name'  : self.name,
            'password' : 'Myadmin123',
        }

    def setUp(self):
        self.create_customer_object_data()
        self.client = APIClient()
        self.localhost = '127.0.0.1'
        self.register_url = reverse('customer-registration')

    def test_customer_register_post_request(self):
        """
        test customer register post request
        """
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, 201)


class ViewMenuAPITestCase(BaseTestCase):
    """
    view menu api test case
    """
    def login_user_func(self):
        login_url = reverse('login')
        self.login_data = {
            'password': self.password, 'email': self.email
        }
        response = self.client.post(login_url, self.login_data)
        self.token = response.json().get('token')

    def setUp(self):
        self.create_user_object()
        self.client = APIClient()
        self.localhost = '127.0.0.1'
        self.view_menu_url = reverse('view-menu')

    def test_customer_register_valid_get_request(self):
        """
        test customer register post request
        """
        self.login_user_func()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.view_menu_url)
        self.assertEqual(response.status_code, 200)

    def test_customer_register_invalid_get_request(self):
        """
        test customer register post request
        """
        response = self.client.get(self.view_menu_url)
        self.assertEqual(response.status_code, 401)

    def test_customer_register_unauthorised_get_request(self):
        """
        test customer register post request
        """
        self.login_user_func()
        response = self.client.get(self.view_menu_url)
        self.assertEqual(response.status_code, 401)


class OrderItemsAPITestCase(BaseTestCase):
    """
    Order Item api test cases
    """
    def create_order_item_object_data(self):
        self.order_item_object_data = {
                'items': [
                   {
                        'id' : str(self.shop_item_object.id),
                        # 'shop_item' : self.shop_item_object,
                        'quantity' : 5,
                        'option' : "Milky Way Coffee"
                   },
               ]
        }

    def setUp(self):
        self.create_user_object()
        self.create_shop_option_value()
        self.create_shop_option_type()
        self.create_shop_item_object()
        self.create_order_item_object_data()
        # self.create_order_object_data()

        self.client = APIClient()
        self.localhost = '127.0.0.1'
        self.order_item_url = reverse('order-item')

    def test_order_item_valid_get_request(self):
        """
        test customer register post request
        """
        self.login_user_func()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(self.order_item_url)
        self.assertEqual(response.status_code, 200)

    def test_order_item_invalid_get_request(self):
        """
        test customer register post request
        """
        response = self.client.get(self.order_item_url)
        self.assertEqual(response.status_code, 401)

    def test_order_item_unauthorised_get_request(self):
        """
        test customer register post request
        """
        self.login_user_func()
        response = self.client.get(self.order_item_url)
        self.assertEqual(response.status_code, 401)

    def test_order_item_authorised_post_request(self):
        """
        test order item authorised post request
        """
        self.login_user_func()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.order_item_url, self.order_item_object_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_order_item_unauthorised_post_request(self):
        """
        test order item authorised post request
        """
        self.login_user_func()
        response = self.client.post(self.order_item_url, self.order_item_object_data, format='json')
        self.assertEqual(response.status_code, 401)

    def test_order_item_authorised_post_request_error(self):
        """
        test order item authorised post request error
        """
        self.login_user_func()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.order_item_url, self.order_item_object_data)
        self.assertEqual(response.status_code, 400)

    def test_order_item_unauthorised_post_request_error(self):
        """
        test order item unauthorised post request error
        """
        response = self.client.post(self.order_item_url, self.order_item_object_data)
        self.assertEqual(response.status_code, 401)


class CancelOrderAPITestCase(BaseTestCase):
    """
    cancel order api test case
    """
    def create_order_object(self):
        self.order_object = Order.objects.create(customer=self.user,
                                                status="WAITING",
                                                total_bill='200')
        self.order_object.items.add(self.order_item_object)

    def setUp(self):
        self.create_user_object()
        self.create_shop_option_value()
        self.create_shop_option_type()
        self.create_shop_item_object()
        self.create_order_item_object()
        self.create_order_object()
        # self.create_order_object_data()

        self.client = APIClient()
        self.localhost = '127.0.0.1'
        self.order_item_url = reverse('cancel-order', kwargs = {"pk": self.order_object.id})

    def test_cancel_order_post_request(self):
        """
        test cancel order post request
        """
        self.login_user_func()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.order_item_url)
        self.assertEqual(response.status_code, 201)

    def test_cancel_order_post_request_unauthorised(self):
        """
        test cancel order post request unauthorised
        """
        self.login_user_func()
        response = self.client.post(self.order_item_url)
        self.assertEqual(response.status_code, 401)

    def test_cancel_order_post_request_unlogged(self):
        """
        test cancel order post request unlogged
        """
        response = self.client.post(self.order_item_url)
        self.assertEqual(response.status_code, 401)


class ChangeOrderAPITestCase(BaseTestCase):
    """
    Order Item api test cases
    """
    def create_order_object(self):
        self.order_object = Order.objects.create(customer=self.user,
                                                status="WAITING",
                                                total_bill='200')
        self.order_object.items.add(self.order_item_object)

    
    def create_order_item_object_data(self):
        self.order_item_object_data = {
                'items': [
                   {
                        'replaced_id' : str(self.shop_item_object1.id),
                        'id' : str(self.shop_item_object.id),
                        'quantity' : 5,
                        'option' : "Milky Way Coffee"
                   },
               ]
        }

    def setUp(self):
        self.create_user_object()
        self.create_shop_option_value()
        self.create_shop_option_type()
        self.create_shop_item_object()
        self.create_order_item_object()
        self.create_order_object()
        self.create_order_item_object_data()

        self.client = APIClient()
        self.localhost = '127.0.0.1'
        self.change_order_url = reverse('change-order', kwargs={'pk': self.order_object.id})

    def test_change_order_post_request(self):
        """
        test change order post request
        """
        self.login_user_func()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.change_order_url, self.order_item_object_data, 
                                    format='json')
        self.assertEqual(response.status_code, 201)

    def test_change_order_post_request_unauthorised(self):
        """
        test change order post request unauthorised
        """
        self.login_user_func()
        response = self.client.post(self.change_order_url, self.order_item_object_data, 
                                    format='json')
        self.assertEqual(response.status_code, 401)

    def test_change_order_post_request_unlogged(self):
        """
        test change order post request unlogged
        """
        response = self.client.post(self.change_order_url, self.order_item_object_data, 
                                    format='json')
        self.assertEqual(response.status_code, 401)
