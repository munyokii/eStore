$(document).ready(function() {
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
    
    
    $(document).off('submit', '#newsletter-subscription').on('submit', '#newsletter-subscription', function(event) {
        console.log('Newsletter form submitted');
        event.preventDefault();
        
        const form = $(this);
        const submitButton = $('#newsletter-button');
        

        if (submitButton.prop('disabled')) {
            console.log('Form already being processed, ignoring submission');
            return false;
        }
        
        submitButton.html('<i class="fas fa-spinner fa-spin"></i>');
        submitButton.prop('disabled', true);
        
        $.ajax({
            url: '/newsletter/signup/',
            type: 'POST',
            data: form.serialize(),
            headers: { 'X-CSRFToken': csrftoken },
            dataType: 'json',
            success: function(data) {
                console.log('AJAX response received:', data);
                
                if (data.success) {
                    console.log('Showing success message');
                    toastr.success(data.success, 'Success');
                    form.trigger('reset');
                } else if (data.error) {
                    console.log('Showing error message');
                    toastr.error(data.error, 'Error');
                } else {
                    console.log('Unexpected response format:', data);
                    toastr.error('Unexpected response from server', 'Error');
                }
            },
            error: function(xhr, errmsg, err) {
                console.log('AJAX error:', xhr.status, xhr.responseText);
                

                try {
                    const errorData = JSON.parse(xhr.responseText);
                    if (errorData.error) {
                        toastr.error(errorData.error, 'Error');
                    } else {
                        toastr.error('There was an issue with your subscription.', 'Error');
                    }
                } catch (e) {
                    toastr.error('There was an issue with your subscription.', 'Error');
                }
            },
            complete: function() {
                console.log('AJAX request completed');
                submitButton.html('Subscribe');
                submitButton.prop('disabled', false);
            }
        });
        
        return false;
    });
});