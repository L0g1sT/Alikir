import json
import uuid

from django.views.generic import DetailView
from yookassa import Configuration, Payment
from http import HTTPStatus

from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from django import template
from datetime import datetime
import pdb;

from products.models import Basket


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Алькир - Спасибо за заказ!'


class CanceledTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/canceled.html'


class OrderCreateView(TitleMixin, CreateView):
    title = 'Алькир - Оформление заказа'
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)

            Configuration.account_id = settings.ACCOUNT_ID
            Configuration.secret_key = settings.SECRET_KEY

            # Подготовка данных платежа
            order_total = self.order.get_total_cost()  # Предположим, что у заказа есть метод для расчета общей стоимости
            payment = Payment.create({
                'amount': {
                    'value': str(order_total),  # общая стоимость заказа
                    'currency': 'RUB'
                },
                'confirmation': {
                    'type': 'redirect',
                    'return_url': '{}{}'.format(settings.DOMAIN_NAME, reverse("orders:order_success"))
                },
                'capture': True,
                'description': f'Заказ номер {self.order.id} от {datetime.now().strftime('%d/%m/%Y')}'
                # Используем ID заказа
            }, uuid.uuid4())
            self.order.status = Order.PAID
            self.order.save()
            return HttpResponseRedirect(payment.confirmation.confirmation_url, status=HTTPStatus.SEE_OTHER)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        basket_history = self.request.POST.getlist('basket_history')

        # Ожидаем один элемент в basket_history, который является строкой JSON-массива
        if len(basket_history) != 1:
            raise ValueError("basket_history must contain exactly one JSON array string")

        try:
            baskets = json.loads(basket_history[0])  # Десериализация JSON массива
            if not isinstance(baskets, list):
                raise ValueError("basket_history does not contain a JSON array")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON in basket_history")

        # Проверка, что каждый элемент массива является словарем
        for item in baskets:
            if not isinstance(item, dict):
                raise ValueError("Each item in basket_history must be a dictionary")


        form.instance.baskets = json.dumps(baskets)  # Сериализация обратно в JSON строку
        response = super(OrderCreateView, self).form_valid(form)
        Basket.objects.filter(user=self.request.user).delete()
        self.order = form.instance  # Сохраняем объект заказа
        return response


class OrdersShowView(TitleMixin, ListView):
    model = Order
    title = "Алькир - заказы"
    template_name = 'orders/orders.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:orders')

    def get_queryset(self):
        user_id = self.request.user.id
        return Order.objects.filter(initiator_id=user_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrdersShowView, self).get_context_data()
        return context


class OrderShowView(TitleMixin, DetailView):
    title = "Алькир - заказ"
    template_name = 'orders/order.html'
    model = Order
    context_object_name = 'order'
    success_url = reverse_lazy('orders:order_detail')
