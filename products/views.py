from django.shortcuts import render, HttpResponseRedirect
from products.models import ProductCategory, Product, Basket
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.views import TitleMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
class IndexView(TemplateView):
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Алькир'
        context['request'] = self.request
        return context




class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Алькир - Каталог'

    def get_queryset(self):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')

        if category_id:
            return queryset.filter(category_id=category_id)
        else:
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Алькир - Каталог'
        context['request'] = self.request  # Добавляем переменную request в контекст
        context['categories'] = ProductCategory.objects.all()
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def update_quantity(request, basket_id):
    quantity = request.POST.get('quantity')

    if basket_id and quantity:
        try:
            basket = Basket.objects.get(id=basket_id, user=request.user)
            basket.quantity = quantity
            basket.save()

            # Обновляем сумму и общее количество товаров в корзине
            baskets = Basket.objects.filter(user=request.user)
            total_sum = sum(basket.quantity * basket.product.price for basket in baskets)
            total_quantity = sum(basket.quantity for basket in baskets)
            basket_sum = "{:.2f}".format(float(basket.product.price) * float(basket.quantity))

            # Возвращаем обновленные значения суммы и количества товаров в корзине
            return JsonResponse({'total_sum': total_sum, 'total_quantity': total_quantity, 'basket_sum': basket_sum})
        except Basket.DoesNotExist:
            pass

    # Если в запросе нет баскет_id или quantity, возвращаем ошибку
    return JsonResponse({'error': 'Invalid request'})

