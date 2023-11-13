document.addEventListener("DOMContentLoaded", function () {
    // Add event listeners to your filter elements
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const minPriceInput = document.getElementById("minPrice");
    const maxPriceInput = document.getElementById("maxPrice");
  
    checkboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", updateFilters);
    });
  
    minPriceInput.addEventListener("input", updateFilters);
    maxPriceInput.addEventListener("input", updateFilters);
  
    // Function to update filters and trigger a request to your Django view
    function updateFilters() {
      // Collect selected filter values
      const selectedFilters = {
        // Example: Ratings
        ratings: Array.from(document.querySelectorAll('input[name="rating"]:checked')).map((checkbox) => checkbox.value),
        // Example: Shipping
        shipping: Array.from(document.querySelectorAll('input[name="shipping"]:checked')).map((checkbox) => checkbox.value),
        // Example: Price Range
        minPrice: minPriceInput.value,
        maxPrice: maxPriceInput.value,
        // ... Add more filters as needed
      };
  
      // Send the selected filters to your Django view
      // You can use JavaScript's fetch API or a library like Axios for this
  
      // Example using fetch:
      fetch("/your-django-view-url", {
        method: "POST",
        body: JSON.stringify(selectedFilters),
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle the response and update the product list on your page
          // You might need to use Django templates to render the updated products
          console.log(data); // Replace with your handling logic
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  });
  