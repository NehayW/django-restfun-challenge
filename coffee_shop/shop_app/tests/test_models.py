""" chat/test/test_models.py """
from shop_app.models import (
	UserAccount, ShopOptionValue, Shop, ShopOptionType, ShopItem,
	OrderItem, Order
)
from django import test


class UserAccountTestCase(test.TestCase):

	def setUp(self):
		self.email = 'prakhardwi@gmai.com'
		self.name = 'John Doe'
		user_data = {
			'role'  : UserAccount.CUSTOMER,
			'email' : self.email,
			'name'  : self.name,
			'password' : 'Myadmin123',
			'is_staff' : True,
			'is_active' : True,
			'status'  : UserAccount.ACTIVE 
		}
		self.user = UserAccount.objects.create(**user_data)

	def test_user_account_model_object(self):
		"""
		test user account model object
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertIsInstance(test_user, UserAccount)

	def test_user_account_model_email_field(self):
		"""
		test user account model email field
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertEqual(test_user.email, self.email)

	def test_user_account_model_role_field(self):
		"""
		test user account model role field
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertEqual(test_user.role, UserAccount.CUSTOMER)

	def test_user_account_model_name_field(self):
		"""
		test user account model name field
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertEqual(test_user.name, self.name)

	def test_user_account_model_is_acitve_field(self):
		"""
		test user account model is active field
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertEqual(test_user.is_active, True)

	def test_user_account_model_is_staff_field(self):
		"""
		test user account model is staff field
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertEqual(test_user.is_staff, True)

	def test_user_account_model_status_field(self):
		"""
		test user account model status field
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertEqual(test_user.status, UserAccount.ACTIVE)

	def test_user_account_model_get_full_name_method(self):
		"""
		test user account model get_full_name method
		"""
		test_user = UserAccount.objects.get(email=self.email)
		self.assertEqual(test_user.get_full_name(), self.name)


class ShopModelTestCase(test.TestCase):
	"""
	This test case tests shop model
	"""
	def setUp(self):
		self.shop_name = "Paliwal Shop"
		self.address = "Near Ganeesh Mandir, Topkhana, Ratlam M.P."
		self.value_name = "Foreign Family"
		shop_data = {
			'name'  : self.shop_name,
			'address' : self.address
		}
		self.shop = Shop.objects.create(**shop_data)
		self.shop_option = ShopOptionValue.objects.create(value_name=self.value_name)

	def test_shop_model_object(self):
		"""
		test user account model object
		"""
		test_shop = Shop.objects.get(name=self.shop_name)
		self.assertIsInstance(test_shop, Shop)

	def test_shop_model_name_field(self):
		"""
		test shop model name field
		"""
		test_shop = Shop.objects.get(name=self.shop_name)
		self.assertEqual(test_shop.name, self.shop_name)

	def test_shop_model_adddress_field(self):
		"""
		test shop model address field
		"""
		test_shop = Shop.objects.get(name=self.shop_name)
		self.assertEqual(test_shop.address, self.address)

	def test_shopvalue_model_object(self):
		"""
		test shopvalue model object
		"""
		test_shop_value = ShopOptionValue.objects.all()[0]
		self.assertIsInstance(test_shop_value, ShopOptionValue)

	def test_shopvalue_model_value_name_field(self):
		"""
		test shopvalue model value name field
		"""
		test_shop_value = ShopOptionValue.objects.all()[0]
		self.assertEqual(test_shop_value.value_name, self.value_name)


class ShopItemTestCase(test.TestCase):
	"""
	This test case tests shop item class
	"""
	def create_shop_option_value(self):
		self.value_name1 = "Foreign Family"
		self.value_name2 = "Coffee Family"
		self.value_name3 = "Tea Family"
		self.shop_option1 = ShopOptionValue.objects.create(value_name=self.value_name1)
		self.shop_option2 = ShopOptionValue.objects.create(value_name=self.value_name2)
		self.shop_option3 = ShopOptionValue.objects.create(value_name=self.value_name3)

	def create_shop_option_type(self):
		self.type_name = "Coffee Shop"
		shop_option_list = [self.shop_option1, self.shop_option2, self.shop_option3]
		self.shop_option_type = ShopOptionType.objects.create(type_name=self.type_name)
		self.shop_option_type.option_value.set(shop_option_list)

	def setUp(self):
		self.create_shop_option_value()
		self.create_shop_option_type()
		self.shop_item_name = "Coffee"
		self.shop_item_price = 20
		self.shop_item_description = "Coffee makes us cool and healthy."

		shop_item_data = {
			'name' : self.shop_item_name,
			'price' : self.shop_item_price,
			'description' : self.shop_item_description
		}
		self.shop_item = ShopItem.objects.create(**shop_item_data)
		self.shop_item.option.add(self.shop_option_type)

	def test_shop_option_value_object(self):
		"""
		test shop option value object
		"""
		self.assertIsInstance(self.shop_option2, ShopOptionValue)

	def test_shop_option_type_object(self):
		"""
		test shop option type object
		"""
		self.assertIsInstance(self.shop_option_type, ShopOptionType)

	def test_shop_item_object_valid_or_not(self):
		"""
		test shop item object valid or not
		"""
		self.assertIsInstance(self.shop_item, ShopItem)

	def test_shop_item_object_name_field(self):
		"""
		test shop item object name field
		"""
		test_shop_item = ShopItem.objects.get(name=self.shop_item_name)
		self.assertEqual(test_shop_item.name, self.shop_item_name)

	def test_shop_item_object_price_field(self):
		"""
		test shop item object price field
		"""
		test_shop_item = ShopItem.objects.get(name=self.shop_item_name)
		self.assertEqual(test_shop_item.price, str(self.shop_item_price))

	def test_shop_item_object_description_field(self):
		"""
		test shop item object description field
		"""
		test_shop_item = ShopItem.objects.get(name=self.shop_item_name)
		self.assertEqual(test_shop_item.description, self.shop_item_description)

	def test_shop_item_object_option_field_count(self):
		"""
		test shop item object option field count
		"""
		test_shop_item = ShopItem.objects.get(name=self.shop_item_name)
		self.assertEqual(test_shop_item.option.all().count(), 1)

	def test_shop_option_type_object_option_value_field_count(self):
		"""
		test shop option type object option value field count
		"""
		self.assertEqual(self.shop_option_type.option_value.all().count(), 3)


class OrderModelTestCase(test.TestCase):
	"""
	This test case order item
	"""
	def create_user_account_object(self):
		"""
		This method creates user account object
		"""
		self.email = 'prakhardwi@gmai.com'
		self.name = 'John Doe'
		user_data = {
			'role'  : UserAccount.CUSTOMER,
			'email' : self.email,
			'name'  : self.name,
			'password' : 'Myadmin123',
			'is_staff' : True,
			'is_active' : True,
			'status'  : UserAccount.ACTIVE 
		}
		self.user = UserAccount.objects.create(**user_data)


	def create_shop_option_value(self):
		"""
		This methdo creates SopOptionValue class object
		"""
		self.value_name = "Coffee Family"
		self.shop_option = ShopOptionValue.objects.create(value_name=self.value_name)

	def create_shop_option_type(self):
		"""
		This method creates ShopOptionTupe class object
		"""
		self.type_name = "Coffee Shop"
		self.shop_option_type = ShopOptionType.objects.create(type_name=self.type_name)
		self.shop_option_type.option_value.add(self.shop_option)

	def create_shop_item_object(self):
		"""
		this emthod creates ShopItem class object
		"""
		self.shop_item_name = "Coffee"
		self.shop_item_price = 20
		self.shop_item_description = "Coffee makes us cool and healthy."

		shop_item_data = {
			'name' : self.shop_item_name,
			'price' : self.shop_item_price,
			'description' : self.shop_item_description
		}
		self.shop_item = ShopItem.objects.create(**shop_item_data)
		self.shop_item.option.add(self.shop_option_type)

	def create_order_item_object(self):
		"""
		this method creates OrderItem class object
		"""
		self.order_item_quantity = 5
		self.option = "Coffee"
		self.order_item = OrderItem.objects.create(
			shop_item=self.shop_item,
			quantity=self.order_item_quantity,
			option=self.option
		)

	def setUp(self):
		self.create_shop_option_value()
		self.create_shop_option_type()
		self.create_shop_item_object()
		self.create_order_item_object()
		self.create_user_account_object()
		self.order_choice = "WAITING"
		self.total_bill = 200
		self.order_object = Order.objects.create(
				customer=self.user, 
				status=self.order_choice,
				total_bill=self.total_bill
		)
		self.order_object.items.add(self.order_item)

	def test_order_object_valid_or_not(self):
		"""
		test order object valid or not
		"""
		self.assertIsInstance(self.order_object, Order)

	def test_order_item_object_valid_or_not(self):
		"""
		test order item object valid or not
		"""
		self.assertIsInstance(self.order_item, OrderItem)

	def test_shop_item_object_valid_or_not(self):
		"""
		test shop item object valid or not
		"""
		self.assertIsInstance(self.shop_item, ShopItem)

	def test_shop_option_type_object_valid_or_not(self):
		"""
		test shop option type object valid or not
		"""
		self.assertIsInstance(self.shop_option_type, ShopOptionType)

	def test_shop_option_Value_object_valid_or_not(self):
		"""
		test shop option value object valid or not
		"""
		self.assertIsInstance(self.shop_option, ShopOptionValue)

	def test_order_object_items_field_count(self):
		"""
		test order object items field count
		"""
		self.assertEqual(self.order_object.items.all().count(), 1)

	def test_order_object_status_field(self):
		"""
		test order object status field
		"""
		self.assertEqual(self.order_object.status, self.order_choice)

	def test_order_object_customer_field(self):
		"""
		test order object customer field
		"""
		self.assertEqual(self.order_object.customer, self.user)

	def test_order_object_total_bill_field(self):
		"""
		test order object total bill field
		"""
		self.assertEqual(self.order_object.total_bill, self.total_bill)
