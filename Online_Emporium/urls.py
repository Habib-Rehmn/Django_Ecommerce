from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from Online_Emporium.views import customer_signup_view, customer_login_view
from django.contrib import admin
from djstripe import webhooks






urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_view, name='search'),
    path('sort/', views.search_view, name='search_view'),
    path('filter/', views.search_view, name='search_view'),
    
    
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('accounts/customer/', customer_signup_view.as_view(), name='customer_signup'),
    path('accounts/customer/login/', customer_login_view.as_view(), name='customer_login'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin-logout-choice/', views.handle_admin_logout_choice, name='admin_logout_choice'),
    path('accounts/customer/update/', views.customer_update, name='customer_update'),
    path('accounts/customer/delete/', views.customer_delete, name='customer_delete'),
    
    
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('customer/orders/', views.customer_orders, name='customer_orders'),

    path('payment/', views.payment_view, name='payment'),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

