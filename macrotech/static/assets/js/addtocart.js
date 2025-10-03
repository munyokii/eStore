$(document).ready(function() {
  $('.add-to-cart').click(function(e) {
    e.preventDefault();

    let productId = $(this).data('product');

    $.ajax({
      url: "/cart/add/",
      method: "POST",
      data: {
        product_id: productId,
        csrfmiddlewaretoken: "{{ csrf_token }}"
      },
      success: function(response) {
        if (response.success) {
          toastr.success(response.message);
          $("#cart-count").text(response.cart_count);
        } else {
          toastr.error(response.message);
        }
      },
      error: function() {
        toastr.error('Something went wrong. Try again!');
      }
    });
  });
});

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": true,
    "positionClass": "toast-bottom-right",
    "preventDuplicates": true,
    "onclick": null,
    "showDuration": "1200",
    "hideDuration": "4000",
    "timeOut": "20000",
    "extendedTimeOut": "4000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};