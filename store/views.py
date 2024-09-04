from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django import views
from .models import *
from accounts.models import AddressModel
from .forms import *
from django.contrib import messages
from random import randint
from django.utils.encoding import uri_to_iri
from django.core.paginator import Paginator
from accounts.melipayamak import send_sms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from rashchub import settings
import requests
import json
from django.db import IntegrityError

# Create your views here.


sandbox = 'www'

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"


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
        products_on_sale = ProductPriceModel.objects.exclude(on_sale__iexact="0").filter(product__is_active=True)
        products_new = ProductModel.objects.filter(is_active=True).order_by("-created_date")[:2]
        products_sale = ProductModel.objects.filter(is_active=True).order_by("-sale")[:5]
        context = {
            "categories":categories,
            "products_on_sale":products_on_sale,
            "products_new":products_new,
            "products_sale":products_sale,
        }
        return render(request, "store/index.html", context)
    

class CategoryView(views.View):

    def get(self, request, slug):
        products = ProductModel.objects.filter(Q(category__slug=uri_to_iri(slug)) & Q(is_active=True)).order_by("-created_date")
        paginator = Paginator(products, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        categories = CategoryModel.objects.all()
        context = {
            "products":products,
            "categories":categories,
            "slug":slug,
            "page_obj": page_obj,
        }
        return render(request, "store/category.html", context)
    

class AllProductsView(views.View):

    def get(self, request):
        products = ProductModel.objects.filter(Q(is_active=True)).order_by("-created_date")
        paginator = Paginator(products, 12)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        categories = CategoryModel.objects.all()
        context = {
            "products":products,
            "categories":categories,
            "page_obj": page_obj,
        }
        return render(request, "store/all-products.html", context)
    

class ProductDetailsView(views.View):

    def get(self, request, slug):
        product = get_object_or_404(ProductModel, slug=uri_to_iri(slug))
        comments = ProductCommentModel.objects.filter(Q(product=product) & Q(is_active=True)).order_by("created_date")
        total = ProductCommentModel.objects.filter(Q(product=product) & Q(is_active=True)).count()
        one  = ProductCommentModel.objects.filter(Q(product=product) & Q(is_active=True) & Q(rate=1)).count()
        one_p = int(float(one * 100 / total))
        two = ProductCommentModel.objects.filter(Q(product=product) & Q(is_active=True) & Q(rate=2)).count()
        two_p = int(float(two * 100 / total))
        three = ProductCommentModel.objects.filter(Q(product=product) & Q(is_active=True) & Q(rate=3)).count()
        three_p = int(float(three * 100 / total))
        four = ProductCommentModel.objects.filter(Q(product=product) & Q(is_active=True) & Q(rate=4)).count()
        four_p = int(float(four * 100 / total))
        five = ProductCommentModel.objects.filter(Q(product=product) & Q(is_active=True) & Q(rate=5)).count()
        five_p = int(float(five * 100 / total))
        rate = int(float(((one * 1) + (two * 2) + (three * 3) + (four * 4) + (five * 5)) / total))
        form = ProductCommentForm()
        view = int(product.view)
        view += 1
        product.view = view
        product.save()
        products = ProductModel.objects.filter(Q(category__slug=product.category.slug) & Q(is_active=True))[:6]
        products_new = ProductModel.objects.filter(is_active=True).order_by("-created_date")[:2]
        context = {
            "product":product,
            "comments":comments,
            "products":products,
            "products_new":products_new,
            "form":form,
            "rate":rate,
            "one":one,
            "two":two,
            "three":three,
            "four":four,
            "five":five,
            "one_p":one_p,
            "two_p":two_p,
            "three_p":three_p,
            "four_p":four_p,
            "five_p":five_p,
        }
        return render(request, "store/product-details.html", context)
    

class ProductCommentView(LoginRequiredMixin, views.View):
    login_url = "accounts:sign-in"

    def post(self, request, id):
        user = get_object_or_404(User, pk=request.user.id)
        product = get_object_or_404(ProductModel, pk=id)
        mobiles = ManagementNumbersModel.objects.all().order_by("-created_date")
        form = ProductCommentForm(request.POST)
        if form.is_valid():
            rate = form.cleaned_data.get("rate")
            comment = form.cleaned_data.get("comment")
            new_comment = ProductCommentModel()
            new_comment.user = user
            new_comment.is_active = False
            new_comment.product = product
            new_comment.rate = rate
            new_comment.comment = comment
            new_comment.user_created = user
            new_comment.user_modified = user
            try:
                new_comment.save()
            except IntegrityError as e:
                messages.error(request, "قبلا این دیدگاه خود را ذخیره کرده‌اید!")
                return render(request, "store/comment.html", {"product":product})
            else:
                messages.success(request, "کاربر گرامی نظر شما با موفقیت ثبت شد.")
                if mobiles:
                    for i in mobiles:
                        send_sms(number=i.mobile, bodyId=246562, args=[user.username])
                return render(request, "store/comment.html", {"product":product})
        return redirect("store:product-details", slug=product.slug)

    

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
        

class InvoiceAddView(LoginRequiredMixin, views.View):
    login_url = "accounts:sign-in"

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        cart = Cart(request)
        products = ProductPriceModel.objects.filter(id__in=[int(id) for id in cart.cart.keys()])
        total_on_sale = 0
        for i in products:
            if i.on_sale != "0":
                total_on_sale += int(i.on_sale)
            else:
                total_on_sale += int(i.price)
        if products:
            invoice = InvoiceModel()
            invoice.user = user
            invoice.total_price = total_on_sale
            invoice.save()
            send_sms(f"{user.username}", 241741, [invoice.pk])
        else:
            messages.error(request, "سبد خرید شما خالی است، لطفا ابتدا محصول مورد نظر خود را اضافه کنید.")
            return redirect("store:cart")
        for p in products:
            if p.price != "0" or p.on_sale != "0":
                item = InvoiceItemModel(
                    invoice=invoice,
                    product=p,
                    price=p.price,
                    on_sale=p.on_sale
                )
                item.save()
                cart.remove_product(id=p.pk)
        messages.success(request, f"سبد خرید شما خالی شد و یک فاکتور با شماره {invoice.pk} برای شما ایجاد شد.")
        return redirect("store:invoice-view", id=invoice.pk)
    

class InvoiceView(views.View):

    def get(self, request, id):
        user = get_object_or_404(User, pk=request.user.id)
        addresses = AddressModel.objects.filter(user=user)
        if addresses:
            invoice = get_object_or_404(InvoiceModel, Q(user=user) & Q(pk=id) & Q(is_active=True))
            form = AddressSelectForm()
            context = {
                "addresses":addresses,
                "invoice":invoice,
                "form":form,
            }
            return render(request, "store/invoice-view.html", context)
        return redirect("accounts:address-add")
    
    def post(self, request, id):
        user = get_object_or_404(User, pk=request.user.id)
        addresses = AddressModel.objects.filter(user=user)
        invoice = get_object_or_404(InvoiceModel, Q(user=user) & Q(pk=id) & Q(is_active=True))
        form = AddressSelectForm(request.POST)
        context = {
            "addresses":addresses,
            "invoice":invoice,
            "form":form,
        }
        if form.is_valid():
            address = form.cleaned_data.get("address")
            amount = form.cleaned_data.get("amount")
            ad = get_object_or_404(AddressModel, pk=int(address))
            invoice.address = f"{ad.province}-{ad.city}-{ad.address}-کد پستی:{ad.postal_code}"
            invoice.save()
            if amount == "paid":
                payment = PaymentModel(
                    state=PaymentModel.STATE_PAID,
                    invoice=invoice,
                    amount=int(invoice.total_price),
                    mobile=user.username,
                    email=user.email,
                    description=f"صورتحساب شماره {invoice.pk}"
                )
                payment.save()
                callback = "https://rashchub.com/verify"
                data = {
                        "MerchantID": settings.MERCHANT,
                        "Amount": int(invoice.total_price),
                        "Description": f"صورتحساب شماره {invoice.pk}",
                        "Phone": user.username,
                        "CallbackURL": f"{callback}/{payment.pk}",
                    }
                data = json.dumps(data)
                headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
                try:
                    response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
                    if response.status_code == 200:
                        response = response.json()
                        if response['Status'] == 100:
                            payment.authority = response["Authority"]
                            payment.save()
                            url = ZP_API_STARTPAY + str(response["Authority"])
                            return HttpResponseRedirect(url)
                        else:
                            messages.error(request, "در حال حاضر خطای سیستمی رخ داده است و ارتباط با درگاه بانک برقرار نشد، لطفا دوباره تلاش کنید!")
                            return render(request, "store/message.html")
                    return render(request, "store/invoice-view.html", context)

                except requests.exceptions.Timeout:
                    messages.warning(request, "زمان شما برای پرداخت به پایان رسیده است، لظفا دوباره تلاش کنید.")
                    return render(request, "store/invoice-view.html", context)
                except requests.exceptions.ConnectionError:
                    messages.warning(request, "ارتباط با درگاه برقرار نشد!")
                    return render(request, "store/invoice-view.html", context)
            elif amount == "deposit":
                payment = PaymentModel(
                    state=PaymentModel.STATE_DEPOSIT,
                    invoice=invoice,
                    amount=int(float((float(invoice.total_price) * 30) / 100 )),
                    mobile=user.username,
                    email=user.email,
                    description=f"صورتحساب شماره {invoice.pk}"
                )
                payment.save()
                callback = "https://rashchub.com/verify"
                data = {
                        "MerchantID": settings.MERCHANT,
                        "Amount": int(float((float(invoice.total_price) * 30) / 100 )),
                        "Description": f"صورتحساب شماره {invoice.pk}",
                        "Phone": user.username,
                        "CallbackURL": f"{callback}/{payment.pk}",
                    }
                data = json.dumps(data)
                headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
                try:
                    response = requests.post(ZP_API_REQUEST, data=data,headers=headers, timeout=10)
                    if response.status_code == 200:
                        response = response.json()
                        if response['Status'] == 100:
                            payment.authority = response["Authority"]
                            payment.save()
                            url = ZP_API_STARTPAY + str(response["Authority"])
                            return HttpResponseRedirect(url)
                        else:
                            messages.error(request, "در حال حاضر خطای سیستمی رخ داده است و ارتباط با درگاه بانک برقرار نشد، لطفا دوباره تلاش کنید!")
                            return render(request, "store/message.html")
                    return render(request, "store/invoice-view.html", context)

                except requests.exceptions.Timeout:
                    messages.warning(request, "زمان شما برای پرداخت به پایان رسیده است، لظفا دوباره تلاش کنید.")
                    return render(request, "store/invoice-view.html", context)
                except requests.exceptions.ConnectionError:
                    messages.warning(request, "ارتباط با درگاه برقرار نشد!")
                    return render(request, "store/invoice-view.html", context)
            else:
                return render(request, "store/invoice-view.html", context)
        return render(request, "store/invoice-view.html", context)


class VerifyView(views.View):

    def get(self, request, id):
        payment = get_object_or_404(PaymentModel, pk=id)
        invoice = get_object_or_404(InvoiceModel, pk=payment.invoice.pk)
        mobiles = ManagementNumbersModel.objects.all()
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": payment.amount,
            "Authority": payment.authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                payment.status = 100
                payment.refid = response["RefID"]
                payment.save()
                invoice.state = InvoiceModel.STATE_ACCEPT
                invoice.save()
                if mobiles:
                    for i in mobiles:
                        send_sms(i.mobile, 241819, [invoice.pk])
                context = {
                    "payment":payment
                }
                send_sms(invoice.user.username, 241818, [str(payment.refid)])
                messages.success(request, "پرداخت شما با موفقیت انجام شد.")
                return render(request, "store/verify.html", context)
            else:
                messages.error(request, "خطا رخ داده، پرداخت انجام نشده است!")
                return render(request, "store/verify.html", {'status': False, 'code': str(response['Status'])})
        return response