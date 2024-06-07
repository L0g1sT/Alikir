from django.db import models
from users.models import User
import json  

class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
            (CREATED, 'Создан'),
            (PAID, 'Оплачен'),
            (ON_WAY, 'В пути'),
            (DELIVERED, 'Доставлен'))

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(max_length=256)
    address = models.CharField(max_length=256)
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def get_total_cost(self):
        try:
            basket_items = json.loads(self.baskets)
            if not isinstance(basket_items, list):
                raise ValueError("basket_items is not a list")
        except json.JSONDecodeError:
            raise ValueError("baskets contains invalid JSON")

        total_cost = 0
        for item in basket_items:
            if not isinstance(item, dict):
                raise ValueError("Each item in basket_items should be a dictionary")
            total_cost += float(item['fields']['price']) * item['fields']['quantity']  # Преобразование цены в float
        return total_cost

    def __str__(self):
        return f'Order #{self.id}. {self.first_name} {self.last_name}'
    
