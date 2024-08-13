from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django import views
from .models import *
from .forms import *
from django.contrib import messages
from random import randint
from django.utils.encoding import uri_to_iri
from django.core.paginator import Paginator
from accounts.melipayamak import send_sms

# Create your views here.

class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get('cart', {})

    def add_product(self, id, quantity=1):
        product_id = str(id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity
        self.save()

    def remove_product(self, id):
        product_id = str(id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True


class CartAddView(views.View):

    def get(self, request, id):
        product = get_object_or_404(ProductPriceModel, pk=id)
        cart = Cart(request)
        cart.add_product(id=product.pk)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

class CartView(views.View):

    def get(self, request):
        cart = Cart(request)
        products = ProductPriceModel.objects.filter(id__in=[int(id) for id in cart.cart.keys()])
        total_price = 0
        total_on_sale = 0
        sale = 0
        for i in products:
            total_price += int(i.price)
            if i.on_sale != "0":
                total_on_sale += int(i.on_sale)
            else:
                total_on_sale += int(i.price)
        sale = total_price - total_on_sale    
        context = {
            "products":products,
            "total_price":total_price,
            "total_on_sale":total_on_sale,
            "sale":sale,
        }
        return render(request, 'store/cart.html', context)
    

class CartRemoveView(views.View):

    def get(self, request, id):
        product = get_object_or_404(ProductPriceModel, pk=id)
        cart = Cart(request)
        cart.remove_product(id=product.pk)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

class IndexView(views.View):

    def get(self, request):
        categories = CategoryModel.objects.all()
        products_on_sale = ProductPriceModel.objects.exclude(on_sale__iexact="0")
        products_new = ProductModel.objects.all().order_by("-created_date")[:2]
        products_sale = ProductModel.objects.all().order_by("-sale")[:5]
        context = {
            "categories":categories,
            "products_on_sale":products_on_sale,
            "products_new":products_new,
            "products_sale":products_sale,
        }
        return render(request, "store/index.html", context)
    

class CategoryView(views.View):

    def get(self, request, slug):
        products = ProductModel.objects.filter(category__slug=uri_to_iri(slug)).order_by("-created_date")
        paginator = Paginator(products, 12)
        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        prices = ProductPriceModel.objects.filter(product__category__slug=uri_to_iri(slug))
        categories = CategoryModel.objects.all()
        context = {
            "products":products,
            "categories":categories,
            "slug":slug,
            "prices":prices,
            "page_obj": page_obj,
        }
        return render(request, "store/category.html", context)
    

class ProductDetailsView(views.View):

    def get(self, request, slug):
        product = get_object_or_404(ProductModel, slug=uri_to_iri(slug))
        view = int(product.view)
        view += 1
        product.view = view
        product.save()
        products = ProductModel.objects.filter(category__slug=product.category.slug)[:6]
        products_new = ProductModel.objects.all().order_by("-created_date")[:2]
        images = ProductImageModel.objects.filter(product=product)
        form = CartSubmitForm()
        context = {
            "product":product,
            "images":images,
            "products":products,
            "products_new":products_new,
        }
        return render(request, "store/product-details.html", context)
    

class AboutUsView(views.View):

    def get(self, request):
        return render(request, "store/about-us.html")
    

class ContactUsView(views.View):

    def get(self, request):
        form = ContactUsForm()
        return render(request, "store/contact-us.html", {"form":form})

    def post(self, request):
        form = ContactUsForm(self.request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            mobile = form.cleaned_data.get("mobile")
            message = form.cleaned_data.get("message")
            code = randint(100000000, 999999999)
            contact = ContactUsModel(
                first_name = first_name,
                last_name = last_name,
                email = email,
                mobile = mobile,
                message = message,
                code = str(code),
            )
            contact.save()
            send_sms(str(mobile), 239745, [str(code)])
            print(send_sms)
            messages.success(request, "پیام شما با موفقیت ارسال شد، لطفا منتظر باشید تا همکاران ما با شما تماس بگیرند.")
            return render(request, "store/messages.html")
        return render(request, "store/contact-us.html", {"form":form})
    

class HelpView(views.View):

    def get(self, request, key):
        return render(request, "store/help.html", {"help":key})
    

class CartSubmitView(views.View):

    def post(self, request):
        form = CartSubmitForm(request.POST)
        if form.is_valid():
            price = form.cleaned_data.get("price")
            cart = Cart(request)
            cart.add_product(price)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        