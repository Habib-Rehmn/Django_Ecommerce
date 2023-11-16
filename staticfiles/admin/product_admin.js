(function ($) {
    $(document).ready(function () {
                $('.field-ram').hide();
                $('.field-storage_type').hide();
                $('.field-generation').hide();
                $('.field-processor').hide();
                $('.field-gpu').hide();
                $('.field-condition').hide();
                $('.field-storage').hide();
                $('.field-battery').hide();
                $('.field-warranty').hide();
                $('.field-color').hide();
                $('.field-apparel_type').hide();
                $('.field-size').hide();
                $('.field-material').hide();
                $('.field-pant_type').hide();
                $('.field-pant_size').hide();
                $('.field-shoes_size').hide();

        // Function to show/hide fields based on product type
        function toggleFields() {
            console.log('Dropdown changed!'); // Debugging
            var productType = $('#id_product_type').val();
            console.log(productType)
            
            if (productType === 'laptop') {
                $('.field-ram').hide();
                $('.field-storage_type').hide();
                $('.field-generation').hide();
                $('.field-processor').hide();
                $('.field-gpu').hide();
                $('.field-condition').hide();
                $('.field-storage').hide();
                $('.field-battery').hide();
                $('.field-warranty').hide();
                $('.field-color').hide();
                $('.field-apparel_type').hide();
                $('.field-size').hide();
                $('.field-material').hide();
                $('.field-pant_type').hide();
                $('.field-pant_size').hide();
                $('.field-shoes_size').hide();
                $('.field-ram').show();
                $('.field-storage_type').show();
                $('.field-generation').show();
                $('.field-processor').show();
                $('.field-gpu').show();
                $('.field-condition').show();
            } else if (productType === 'mobile_phone') {
                $('.field-ram').hide();
                $('.field-storage_type').hide();
                $('.field-generation').hide();
                $('.field-processor').hide();
                $('.field-gpu').hide();
                $('.field-condition').hide();
                $('.field-storage').hide();
                $('.field-battery').hide();
                $('.field-warranty').hide();
                $('.field-color').hide();
                $('.field-apparel_type').hide();
                $('.field-size').hide();
                $('.field-material').hide();
                $('.field-pant_type').hide();
                $('.field-pant_size').hide();
                $('.field-shoes_size').hide();
                $('.field-ram').show();
                $('.field-storage').show();
                $('.field-battery').show();
                $('.field-condition').show();
                $('.field-warranty').show();
            } else if (productType === 'shirt') {
                $('.field-ram').hide();
                $('.field-storage_type').hide();
                $('.field-generation').hide();
                $('.field-processor').hide();
                $('.field-gpu').hide();
                $('.field-condition').hide();
                $('.field-storage').hide();
                $('.field-battery').hide();
                $('.field-warranty').hide();
                $('.field-color').hide();
                $('.field-apparel_type').hide();
                $('.field-size').hide();
                $('.field-material').hide();
                $('.field-pant_type').hide();
                $('.field-pant_size').hide();
                $('.field-shoes_size').hide();
                $('.field-color').show();
                $('.field-apparel_type').show();
                $('.field-size').show();
                $('.field-material').show();
            } else if (productType === 'pant') {
                $('.field-ram').hide();
                $('.field-storage_type').hide();
                $('.field-generation').hide();
                $('.field-processor').hide();
                $('.field-gpu').hide();
                $('.field-condition').hide();
                $('.field-storage').hide();
                $('.field-battery').hide();
                $('.field-warranty').hide();
                $('.field-color').hide();
                $('.field-apparel_type').hide();
                $('.field-size').hide();
                $('.field-material').hide();
                $('.field-pant_type').hide();
                $('.field-pant_size').hide();
                $('.field-shoes_size').hide();
                $('.field-color').show();
                $('.field-size').show();
                $('.field-material').show();
                $('.field-pant_type').show();
                $('.field-pant_size').show();
            } else if (productType === 'shoes') {
                $('.field-ram').hide();
                $('.field-storage_type').hide();
                $('.field-generation').hide();
                $('.field-processor').hide();
                $('.field-gpu').hide();
                $('.field-condition').hide();
                $('.field-storage').hide();
                $('.field-battery').hide();
                $('.field-warranty').hide();
                $('.field-color').hide();
                $('.field-apparel_type').hide();
                $('.field-size').hide();
                $('.field-material').hide();
                $('.field-pant_type').hide();
                $('.field-pant_size').hide();
                $('.field-shoes_size').hide();
                $('.field-color').show();
                $('.field-size').show();
                $('.field-apparel_type').show();
                $('.field-shoes_size').hide();
            }
        }
        
        // Initial toggle when the page loads
        toggleFields();
        
        // Toggle fields whenever the product type changes
        $('#id_product_type').on('change', toggleFields);
    });
})(django.jQuery);
