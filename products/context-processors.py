from products.models import Basket


def baskets(request):
    user = request.user
    
    if user.is_authenticated:
        result = {
                'baskets':Basket.objects.filter(user=user)
                }
        return result
    else:
        return list()
