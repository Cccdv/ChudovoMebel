import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from products.models import Product
from profiles.models import UserProfile


class Order(models.Model):
    order_number = models.CharField('Номер заказа', max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True, related_name='orders', verbose_name="Выберите профиль:")
    full_name = models.CharField('ФИО', max_length=50, null=False, blank=False)
    email = models.EmailField('Электронная почта', max_length=254, null=False, blank=False)
    phone_number = models.CharField('Номер телефона', max_length=20, null=False, blank=False)
    country = CountryField('Страна', blank_label='Выберите страну', null=False, blank=False)
    postcode = models.CharField('Индекс', max_length=20, null=True, blank=True)
    town_or_city = models.CharField('Город', max_length=40, null=False, blank=False)
    street_address1 = models.CharField('Улица', max_length=80, null=False, blank=False)
    street_address2 = models.CharField('Дом', max_length=80, null=True, blank=True)
    county = models.CharField('Область', max_length=80, null=True, blank=True)
    date = models.DateTimeField('Дата', auto_now_add=True)
    order_total = models.DecimalField('Сумма заказа',
        max_digits=10, decimal_places=0, null=False, default=0)
    grand_total = models.DecimalField('Итого',
        max_digits=10, decimal_places=0, null=False, default=0)
    original_bag = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField('Ключ оплаты Stripe',
        max_length=254, null=False, blank=False, default='')

    class Meta:
        verbose_name_plural = "Заказы товаров"
        verbose_name = "заказ"
    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added,
        accounting for delivery costs.
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))[
            'lineitem_total__sum'] or 0
        self.grand_total = self.order_total
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE, related_name='lineitems', verbose_name='Заказ')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField('Количество', null=False, blank=False, default=0)
    lineitem_total = models.DecimalField('Сумма заказа ₽',
        max_digits=6, decimal_places=0, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Артикул: {self.product.sku} , № Заказа: {self.order.order_number}'
