# utils.py

from .models import Product  # Import your Product model

def get_filtered_brands(request, product_type):
    # Assuming 'product_type' is a field in your Product model
    filtered_brands = Product.objects.filter(product_type=product_type).values('brand').distinct()
    brands = [entry['brand'] for entry in filtered_brands]
    return brands
