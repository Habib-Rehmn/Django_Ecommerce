from datetime import timedelta
from django.utils import timezone
from http.client import responses
import json
from urllib import response
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.decorators import login_required
from .models import Product, ProductAttribute
from django.contrib.auth import login, logout
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import render
from .utils import get_filtered_brands
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import CustomUser, Cart, CartItem, Coupon, Order, OrderItem
from allauth.account.views import SignupView, LoginView
from .forms import  CustomSignupForm1
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.oauth2.client import OAuth2Error
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from .decorators import admin_logout_required
from urllib.parse import unquote
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerUpdateForm 
from django.core.mail import send_mail




def index(request):
    return render(request, 'index.html')


    
@login_required
def user_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'profile.html', context)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})


def home(request):
    # Retrieve query parameters from the URL
    query = request.GET.get('q')

    # Create a base queryset without any filtering
    queryset = Product.objects.all()

    # Apply filters based on query parameters
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query) |
            Q(product_type__icontains=query)
        ).distinct()

    context = {
        'results': queryset,
        'query': query,
    }

    return render(request, 'products/home.html', context)




def search_view(request):
    # Retrieve query parameters from the URL
    query = request.GET.get('q')
    min_price = request.GET.get('minPrice')
    max_price = request.GET.get('maxPrice')
    sort_by = request.GET.get('sort_by')
    selected_brand = request.GET.getlist('brand')
    selected_shipping = request.GET.getlist('shipping')
    selected_rating = request.GET.getlist('rating')
 
    # Create a base queryset without any filtering
    queryset = Product.objects.all()
    
    
    
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__icontains=query) |
            Q(product_type__icontains=query)
        ).distinct()
    
    # Initialize an empty Q object to build the dynamic filters
    dynamic_filters = Q()

    # Iterate through the query parameters and add filters for attribute names and values
    for param_name, param_value in request.GET.items():
        if param_name not in ['q', 'minPrice', 'maxPrice', 'sort_by', 'brand', 'shipping', 'rating', 'page']:
            # This is an attribute name and value
            attr_filter = Q(productattribute__attribute_name=param_name, productattribute__attribute_value=param_value)
            dynamic_filters |= attr_filter

    # Apply dynamic filters to the base queryset
    queryset = queryset.filter(dynamic_filters)
    

    if min_price:
        queryset = queryset.filter(price__gte=min_price)

    if max_price:
        queryset = queryset.filter(price__lte=max_price)
        
    if selected_rating:
        queryset = queryset.filter(ratings__in=selected_rating)
        
    if selected_brand:
        queryset = queryset.filter(brand__in=selected_brand)
        
    if selected_shipping:
        if 'free' in selected_shipping:
            queryset = queryset.filter(free_shipping=True)
    
        if 'fee' in selected_shipping:
            queryset = queryset.filter(free_shipping=False)



     # Apply sorting based on 'sort_by' parameter
    if sort_by == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort_by == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort_by == 'ratings_desc':
        queryset = queryset.order_by('-ratings')
    elif sort_by == 'latest':
        queryset = queryset.order_by('-id')  # Assuming 'id' is the primary key

    # Fetch brands for all the product types in the filtered queryset
    product_types = set(queryset.values_list('product_type', flat=True))
    brands = []
    for product_type in product_types:
        filtered_brands = get_filtered_brands(request, product_type)  # Call the function
        brands.extend(filtered_brands)
        
    # Fetch product types
    product_types = queryset.values_list('product_type', flat=True).distinct()
    
    # Fetch all products and their attributes
    product_attributes = {}
    attribute_names = set()
    
    for product in queryset:
        attributes = ProductAttribute.objects.filter(product=product)
        product_attributes[product.id] = [(attr.attribute_name, attr.attribute_value) for attr in attributes]
        attribute_names.update(attr.attribute_name for attr in attributes)

    # Fetch all attribute values whose names match those in the queryset
    all_attribute_values = ProductAttribute.objects.filter(attribute_name__in=attribute_names)

    # Organize the attribute values by attribute name
    attribute_values_dict = {}
    for attribute_value in all_attribute_values:
        attribute_name = attribute_value.attribute_name
        attribute_value = attribute_value.attribute_value

        # Check if the attribute value is not already in the list for the current attribute name
        if attribute_value not in attribute_values_dict.get(attribute_name, []):
            if attribute_name not in attribute_values_dict:
                attribute_values_dict[attribute_name] = []
            attribute_values_dict[attribute_name].append(attribute_value)
            
    
    queryset = queryset.order_by('id')   
       
            
    # Define the number of items to display per page
    items_per_page = 3  # You can adjust this value based on your preference

    # Create a Paginator instance
    paginator = Paginator(queryset, items_per_page)
    print('Paginator:', paginator)

    # Get the current page number from the request's GET parameters
    page = request.GET.get('page', 1)
    print('Page:', page)

    try:
        # Get the Page object for the current page
        results = paginator.get_page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, display the first page
        results = paginator.page(1)
        
    print('Results:', results)  # Debug statement

    context = {
        'results': results,
        'query': query,
        'brands': brands,
        'min_price': min_price,
        'max_price': max_price,
        'product_types': product_types,
        'product_attributes': product_attributes,
        'attribute_values_dict': attribute_values_dict,  
    }

    return render(request, 'search.html', context)




    
@login_required
@admin_logout_required
def customer_dashboard(request):
    
    return render(request, 'customer_dashboard.html')
   


def handle_admin_logout_choice(request):
    if request.method == 'POST':
        if 'logout' in request.POST:
            # The admin chose to log out
            logout(request)  # Log out the admin
            next_url = request.POST.get('next')
            print(next_url)
            if next_url:
                return redirect(unquote(next_url))  # Redirect to the specified URL
            else:
                return redirect('admin:index')  # Redirect to admin home if next_url is not specified
        else:
            # The admin chose to cancel
            return redirect('admin:index')  # Redirect to admin home

    next_url = request.GET.get('next')
    return render(request, 'admin_logout_choice.html', {'next_url': next_url})


@login_required
def customer_update(request):
    if request.method == 'POST':
        form = CustomerUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')
    else:
        form = CustomerUpdateForm(instance=request.user)
    return render(request, 'customer_update.html', {'form': form})


@login_required
def customer_delete(request):
    if request.method == 'POST':
        # Perform account deletion logic
        request.user.delete()
        return redirect('home')  # Redirect to the home page or a suitable location after deletion
    return render(request, 'customer_delete.html')



def add_to_cart(request, product_id):
    if request.user.is_authenticated:
        # If the user is logged in, add the product to the cart
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = Product.objects.get(pk=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # If the user is not logged in, store the product ID and quantity in the session
        product_id = str(product_id)
        quantity = request.session.get('cart_product_' + product_id, 0) + 1
        request.session['cart_product_' + product_id] = quantity
        # Redirect to the login or sign up page
        messages.info(request, 'Please log in or sign up to continue.')
        return redirect('customer_login')  # Change to the appropriate login URL





def remove_from_cart(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
        cart_item.delete()
        messages.success(request, 'Item removed from the cart.')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in the cart.')

    return redirect('cart_view')


def get_or_create(self, request):
    if request.user.is_authenticated:
        # If the user is logged in, associate the cart with the authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)
        return cart, created

    # If the user is not logged in, return None for the cart
    return None, False




@login_required
def cart_view(request):
    if request.user.is_authenticated:
        # If the user is logged in, associate the cart with the authenticated user
        cart, created = Cart.objects.get_or_create(user=request.user)


    # Rest of the view remains the same
    cart_items = cart.cart_items.all()
    
    # Check inventory for each product in the cart
     
    out_of_stock_items = []
     
    for cart_item in cart.cart_items.all():
        if cart_item.quantity > cart_item.product.inventory:
            # Handle the case where the quantity in the cart exceeds the available inventory
            out_of_stock_items.append({
            'product': cart_item.product,
            'available_inventory': cart_item.product.inventory
        })
        
    total_price = cart.get_total_price()    
    
    # Check if the cart is empty
    is_empty = cart_items.count() == 0
        
    # Pass the list to the template
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price, 'out_of_stock_items': out_of_stock_items, 'is_empty': is_empty})
        

    



def get_cart_for_user(user):
    # This function retrieves the user's cart.
    # You should customize it based on your project's logic.
    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        # Create a new cart for the user if it doesn't exist.
        cart = Cart.objects.create(user=user)
    return cart



@login_required
# In your checkout view
def checkout(request):
    cart = get_cart_for_user(request.user)
    total_price = cart.get_total_price()
    coupon_error = None  # Initialize coupon_error to None

    
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code)
                total_price -= (total_price * coupon.discount_percentage / 100)
            except Coupon.DoesNotExist:
                # Set an error message
                coupon_error = "Invalid coupon code. Please check and try again."

        if not coupon_error:  # If there is no coupon error, proceed to create the order
            order = Order.objects.create(user=request.user, total_price=total_price)
            # Calculate or retrieve the necessary context data here
            
          


            
                
            ordered_product_ids = []  # Initialize a list to store product IDs
            # Create a dictionary to store product quantity data
            product_quantity = {}
            for cart_item in cart.cart_items.all():
                OrderItem.objects.create(order=order, cart_item=cart_item)
                product_quan = cart_item.quantity
                product_quantity[cart_item.product.id] = product_quan
                ordered_product_ids.append(cart_item.product.id)  # Add the product ID to the list

            # Set the ordered_products field of the order to the list of product IDs
            order.ordered_products.set(ordered_product_ids)
            
            # Serialize the product quantity data to JSON and store it in the Order model
            order.product_quantity = json.dumps(product_quantity)
            order.save()

            # Clear the cart
            cart.cart_items.all().delete()

            # Update the inventory
            for cart_item in cart.cart_items.all():
                product = cart_item.product
                product.inventory -= cart_item.quantity
                product.save()
                
                
                 # Send an order confirmation email
            send_mail(
                'Order Confirmation',
                f'Your order with ID {order.order_id} has been placed successfully.',
                'your@email.com',
                [request.user.email],
                fail_silently=False,
            )

            # Redirect to the order confirmation page with a unique order ID.
            return redirect('order_confirmation', order_id=order.id)
        
       

    return render(request, 'checkout.html', {'cart': cart, 'total_price': total_price, 'coupon_error': coupon_error})



@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'order_confirmation.html', {'order': order})



def update_cart(request):
    if request.method == 'POST':
        # Get the cart item ID and quantity from the form
        cart_item_id = request.POST.get('cart_item_id')
        quantity = int(request.POST.get('quantity'))

        # Retrieve the cart item
        cart_item = CartItem.objects.get(pk=cart_item_id)

        # Update the quantity of the cart item
        cart_item.quantity = quantity
        cart_item.save()

    return redirect('cart_view')




# Custom view for signup
class customer_signup_view(SignupView):
    form_class = CustomSignupForm1  # Your custom signup form
    template_name = 'customer_signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Check if there are any stored products in the session
        keys_to_remove = []
        for key, value in self.request.session.items():
            if key.startswith('cart_product_'):
                product_id = int(key.replace('cart_product_', ''))
                quantity = value
                # Add the product to the cart
                cart, _ = Cart.objects.get_or_create(user=self.request.user)
                product = Product.objects.get(pk=product_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                # Add the key to the removal list
                keys_to_remove.append(key)
        # Remove the session data
        for key in keys_to_remove:
            del self.request.session[key]
        return response

# Custom view for login
class customer_login_view(LoginView):
    template_name = 'customer_login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        # Check if there are any stored products in the session
        keys_to_remove = []
        for key, value in self.request.session.items():
            if key.startswith('cart_product_'):
                product_id = int(key.replace('cart_product_', ''))
                quantity = value
                # Add the product to the cart
                cart, _ = Cart.objects.get_or_create(user=self.request.user)
                product = Product.objects.get(pk=product_id)
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                # Add the key to the removal list
                keys_to_remove.append(key)
        # Remove the session data
        for key in keys_to_remove:
            del self.request.session[key]
        return response



@login_required
def customer_orders(request):
    # Get orders for the logged-in customer
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    # Additional context to store product details for each order
    order_details = []

    for order in orders:
        if order.product_quantity:
            product_quantity = json.loads(order.product_quantity)
            order_items = []
            total_order_price = 0

            for product_id, quantity in product_quantity.items():
                try:
                    product = Product.objects.get(id=product_id)
                    subtotal = product.price * quantity
                    total_order_price += subtotal
                    order_items.append({
                        'name': product.name,
                        'image_url': product.image.url,
                        'price': product.price,
                        'quantity': quantity,
                        'subtotal': subtotal,
                    })
                except Product.DoesNotExist:
                    pass

            order_details.append({
                'order_id': order.order_id,
                'order_date': order.order_date,
                'total_price': total_order_price,
                'status': order.status,
                'order_items': order_items,
            })

    return render(request, 'customer_orders.html', {'order_details': order_details})



