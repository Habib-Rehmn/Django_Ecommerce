from django.contrib import admin
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Product, ProductAttribute, CustomUser
from django import forms
from django.contrib.auth.admin import UserAdmin
import random
import string
from .models import Coupon, Order
from django.utils.html import format_html
import json

class PriceFilter(admin.SimpleListFilter):
    title = 'By price'
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return [
            ('ascending', 'Increasing'),
            ('descending', 'Decreasing'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'ascending':
            return queryset.order_by('price')
        if self.value() == 'descending':
            return queryset.order_by('-price')

class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1  # Number of empty attribute fields to display

class CustomProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

   

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'price', 'ratings', 'image', 'free_shipping')
    list_filter = (PriceFilter, 'free_shipping')
    search_fields = ('name', 'price')

    # Custom action for editing selected products
    actions = ['edit_selected_products']

    def edit_selected_products(self, request, queryset):
        if queryset.count() == 1:  # Only allow editing a single product
            product_id = queryset.first().id
            edit_url = reverse('admin:Online_Emporium_product_change', args=[product_id])
            return HttpResponseRedirect(edit_url)
        else:
            self.message_user(request, "Please select a single product to edit.")

    edit_selected_products.short_description = "Edit selected product"

    inlines = [ProductAttributeInline]  # Include the inline form for attributes
    form = CustomProductForm  # Use the custom form for Product

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Save the variable attributes if provided
        attribute_name = form.cleaned_data.get('attribute_name')
        attribute_value = form.cleaned_data.get('attribute_value')
        if attribute_name and attribute_value:
            ProductAttribute.objects.create(product=obj, attribute_name=attribute_name, attribute_value=attribute_value)


class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ( 'address', 'phone_number', 'city', 'zip_code', 'full_name', 'profile_image'),
        }),
    )
    readonly_fields = ( 'address', 'phone_number', 'city', 'zip_code', 'full_name', 'profile_image')
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('username', 'email',  'address', 'phone_number', 'city', 'zip_code', 'full_name' , 'profile_image'),
        }),
    )
    
    readonly_fields = ('username', 'email',  'address', 'phone_number', 'city', 'zip_code', 'full_name' , 'profile_image', 'first_name', 'last_name')

    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email', 'address', 'phone_number')


admin.site.register(CustomUser, CustomUserAdmin)





def generate_coupon_code(modeladmin, request, queryset):
    for _ in range(10):  # Generate 10 coupons
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        percentage = random.randint(5, 50)  # Random discount percentage
        Coupon.objects.create(code=code, discount_percentage=percentage)

generate_coupon_code.short_description = "Generate Coupons"

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    actions = [generate_coupon_code]





class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_price', 'order_date', 'status')
    list_filter = ('status',)
    fieldsets = (
        ('Order Details', {
            'fields': ('order_id', 'user', 'status', 'display_ordered_products', 'payment_method','address', 'phone_number', 'city', 'full_name', 'zip_code', 'email'),
        }),
    )
    readonly_fields = ('order_id', 'user', 'total_price', 'display_ordered_products', 'payment_method','address', 'phone_number', 'city', 'full_name', 'zip_code', 'email')  



    def display_ordered_products(self, obj):
        # Check if there is product quantity data in the JSON field
        if obj.product_quantity:
            product_quantity = json.loads(obj.product_quantity)

            if product_quantity:
                table_html = '<table class="ordered-products-table">'
                table_html += '<tr>'  # Start a row for table headers
                table_html += '<th>Product Name</th>'
                table_html += '<th>Product Image</th>'
                table_html += '<th>Unit Price</th>'
                table_html += '<th>Quantity</th>'
                table_html += '<th>Subtotal</th>'
                table_html += '</tr>'  # Close the header row

                row_color = "even"  # Initialize row color
                total_order_price = 0  # Initialize total order price

                for product_id, quantity in product_quantity.items():
                    try:
                        product = Product.objects.get(id=product_id)
                        # Calculate subtotal
                        subtotal = product.price * quantity
                        total_order_price += subtotal

                        # Toggle row colors between "even" and "odd"
                        if row_color == "even":
                            row_color = "odd"
                        else:
                            row_color = "even"

                        # Define CSS classes for row colors and additional formatting
                        row_classes = f"product-row {row_color}"

                    # Generate a table row for each product with CSS classes
                        product_info = format_html(
                            '<tr class="{}"><td>{}</td><td><img src="{}" width="50" height="50" /></td><td>{}</td><td>{}</td><td>{}</td></tr>',
                            row_classes,
                            product.name,
                            product.image.url,
                            product.price,
                            quantity,
                            subtotal
                        )
                        table_html += product_info
                    except Product.DoesNotExist:
                        pass

                table_html += '</table>'

                # Display the total order price
                total_price_html = f'Total Order Price: Rs. {total_order_price:.2f}'
                return format_html(f'{table_html}<br/>{total_price_html}')
    
        return 'No items'



    display_ordered_products.short_description = 'Ordered Products'  # Display a user-friendly name for the field
    

admin.site.register(Order, OrderAdmin)




        
