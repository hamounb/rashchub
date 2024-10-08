from django.urls import path, re_path
from .views import *

app_name = 'store'

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("cart/add/<int:id>/", CartAddView.as_view(), name="cart-add"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/remove/<int:id>/", CartRemoveView.as_view(), name="cart-remove"),
    path("products/", AllProductsView.as_view(), name="all-products"),
    re_path(r'category/(?P<slug>[^/]+)/?/$', CategoryView.as_view(), name="category"),
    re_path(r'product/(?P<slug>[^/]+)/?/$', ProductDetailsView.as_view(), name="product-details"),
    path("comment/<int:id>/", ProductCommentView.as_view(), name="comment"),
    path("about-us/", AboutUsView.as_view(), name="about-us"),
    path("contact-us/", ContactUsView.as_view(), name="contact-us"),
    path("help/<str:key>/", HelpView.as_view(), name="help"),
    path("cart/submit/", CartSubmitView.as_view(), name="cart-submit"),
    path("invoice/add/", InvoiceAddView.as_view(), name="invoice-add"),
    path("invoice/<int:id>/", InvoiceView.as_view(), name="invoice-view"),
    path("verify/<int:id>/", VerifyView.as_view(), name="verify"),
]