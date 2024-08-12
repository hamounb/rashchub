from store.models import CategoryModel, ProductPriceModel
from store.views import Cart

def menu(request):
    categories = CategoryModel.objects.all()
    return {"categories":categories}

def cart(request):
    cart = Cart(request)
    products = ProductPriceModel.objects.filter(id__in=[int(id) for id in cart.cart.keys()])
    total_price = 0
    for i in products:
        if i.on_sale != "0":
            total_price += int(i.on_sale)
        else:
            total_price += int(i.price)
    return {"cart_products":products, "total_price":total_price}