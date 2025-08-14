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

    $(document).on('submit', '#contactform', function(event) {
        event.preventDefault();
        
        const form = $(this);
        const submitButton = $('#sendmessagebutton');

        submitButton.html('<i class="fas fa-spinner fa-spin"></i> Sending...');
        submitButton.prop('disabled', true);

        $.ajax({
            url: '/macrotech/contact-us/',
            type: 'POST',
            data: form.serialize(),
            headers: { 'X-CSRFToken': csrftoken },
            success: function(data) {
                toastr.success(data['success'], 'Success');
                // form.trigger('reset');
            },
            error: function(xhr) {
                if (xhr.responseJSON && xhr.responseJSON.error) {
                    toastr.error(xhr.responseJSON.error, 'Error');
                } else {
                    toastr.error('There was an issue sending your message.', 'Error');
                }
            },
            complete: function() {
                submitButton.html('Send Message');
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
    "showDuration": "600",
    "hideDuration": "2000",
    "timeOut": "10000",
    "extendedTimeOut": "2000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};
