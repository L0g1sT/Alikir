from django.urls import path
from orders.views import OrderCreateView, SuccessTemplateView, CanceledTemplateView, OrdersShowView, OrderShowView

app_name = 'orders'

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('orders/', OrdersShowView.as_view(), name='orders'),
    path('order-success/', SuccessTemplateView.as_view(), name='order_success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('order/<int:pk>/', OrderShowView.as_view(), name='order_detail'),]
