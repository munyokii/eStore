$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');
    const productId = $('#review-container').data('product-id');

    $(document).on('submit', '#reviewForm', function(event) {
        event.preventDefault();
        
        const form = $(this);
        const submitButton = $('#submitReviewButton');

        submitButton.html('<i class="fas fa-spinner fa-spin"></i> Posting...');
        submitButton.prop('disabled', true);

        $.ajax({
            url: `/product/details/${productId}/`,
            type: 'POST',
            data: form.serialize() + `&csrfmiddlewaretoken=${csrftoken}`,
            headers: { 'X-CSRFToken': csrftoken },
            success: function(data) {
                toastr.success(data['success'], 'Success');
                form.trigger('reset');
                // window.location.reload();
            },
            error: function(xhr) {
                if (xhr.responseJSON) {
                    if (xhr.responseJSON.error) {
                        if (typeof xhr.responseJSON.error === 'object') {
                            // Handle field-specific errors
                            let errorMsg = '';
                            for (const [field, message] of Object.entries(xhr.responseJSON.error)) {
                                errorMsg += `${field}: ${message}\n`;
                            }
                            toastr.error(errorMsg, 'Validation Error');
                        } else {
                            toastr.error(xhr.responseJSON.error, 'Error');
                        }
                    } else {
                        toastr.error(JSON.stringify(xhr.responseJSON), 'Error Details');
                    }
                } else {
                    toastr.error('There was an issue posting your review.', 'Error');
                }
            },
            complete: function() {
                submitButton.html('Submit Review');
                submitButton.prop('disabled', false);
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
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};
