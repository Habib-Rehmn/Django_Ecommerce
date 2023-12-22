import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.shortcuts import redirect
from django.core.mail import send_mail
from .models import CustomUser, OrderItem  
import requests
from django.core.files import File
import mimetypes
from .models import Order, CustomUser
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import messages


@receiver(post_save, sender=SocialAccount)
def update_custom_user_with_social_info(sender, instance, created, **kwargs):
    if created:
        # Check if the social account is newly created
        user = instance.user
        custom_user = CustomUser.objects.get(id=user.id)  # Get your custom user instance
        
        # Update custom user model with social information
        custom_user.email = instance.extra_data.get('email', custom_user.email)
        custom_user.full_name = instance.extra_data.get('name', custom_user.full_name)
        
         # Download and save the profile picture
        picture_url = instance.extra_data.get('picture')
        if picture_url:
            response = requests.get(picture_url, stream=True)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type')
                if content_type:
                    extension = mimetypes.guess_extension(content_type)
                    if extension:
                        file_name = f"{user.id}{extension}"
                        custom_user.profile_image.save(file_name, File(response.raw))
        
        custom_user.save()




from django.db.models.signals import Signal

payment_succeeded = Signal()





@receiver(payment_succeeded)
def handle_payment_succeeded(sender, user_id, total_price, address, phone_number, city, full_name, zip_code, email, payment_method, **kwargs):
    # Get the user object based on the user_id
    user = CustomUser.objects.get(pk=user_id)
    from .views import get_cart_for_user
    cart = get_cart_for_user(user)

    order = Order.objects.create(
                user=user,
                total_price=total_price,
                address=address,
                phone_number=phone_number,
                city=city,
                full_name=full_name,
                zip_code=zip_code,
                email=email,
                payment_method = payment_method,
                status = 'paid',
                )
                

                
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
    payment_method = "online_payment"
    order.payment_method = payment_method
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
        [user.email],
        fail_silently=False,
    )
    
 


