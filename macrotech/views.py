"""Application views for the app."""
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.db.models import Count

from macrotech.forms import ContactMessageForm

from .utils import custom_login_required
from .models import Category, Product
from .email import EmailContactNotification

User = get_user_model()

class HomeView(View):
    """Class-based view to display the home.html template."""

    def get(self, request):
        """Handle GET requests and render the home template."""
        products = Product.objects.all().order_by("-uploaded_at")
        categories = Category.objects.annotate(product_count=Count('products'))

        context = {
            "products": products,
            "categories": categories
        }
        return render(request, "home.html", context)


class ProductDetailView(View):
    """Class-based view to display the product_detail.html template."""

    def get(self, request, product_id):
        """Handle GET requests and render the product detail template."""
        product = Product.objects.get(id=product_id)
        context = {
            "product": product
        }
        return render(request, "product-details.html", context)


class CartView(View):
    """Class-based view to display the cart.html template."""

    def get(self, request):
        """Handle GET requests and render the cart template."""
        return render(request, "cart.html")


class CheckoutView(View):
    """Class-based view to display the checkout.html template."""

    def get(self, request):
        """Handle GET requests and render the checkout template."""
        return render(request, "user/checkout.html")


class BlogView(View):
    """Class-based view to display the blog.html template."""

    def get(self, request):
        """Handle GET requests and render the blog template."""
        return render(request, "blog.html")


class BlogDetailView(View):
    """Class-based view to display the blog-details.html template."""

    def get(self, request):
        """Handle GET requests and render the blog-details template."""
        return render(request, "blog-details.html")


class AboutView(View):
    """Class-based view to display the about.html template."""

    def get(self, request):
        """Handle GET requests and render the about template."""
        return render(request, "about.html")


class CategoryView(View):
    """Class-based view to display the category.html template."""

    def get(self, request):
        """Handle GET requests and render the category template."""
        return render(request, "category.html")


class ContactView(View):
    """Class-based view to handle contact form rendering and submission."""

    def get(self, request):
        """Render the contact form template."""
        form = ContactMessageForm()
        return render(request, "contact.html", {'form': form})

    def post(self, request):
        """Handle POST request to submit contact form data."""
        form = ContactMessageForm(request.POST)

        if form.is_valid():
            try:
                contact = form.save()

                context = {
                    'name': contact.name,
                    'email': contact.email,
                    'subject': contact.subject,
                    'message': contact.message,
                }

                notification = EmailContactNotification(context)
                email_sent = notification.send()

                if email_sent:
                    return JsonResponse({
                        'success': 'We have received your message 🤝. We will contact you soon. 🤖'
                    })
                else:
                    return JsonResponse({
                        'warning': 'We have received your message 🤝. But there was an issue sending confirmation email 🤖'
                    })

            except ValueError as e:
                print(f'Error: {e}')
                return JsonResponse({
                    'error': 'Sorry, there was an issue sending your message. Please try again!'
                }, status=500)

        else:
            return JsonResponse({'error': form.errors}, status=400)


class SupportView(View):
    """Class-based view to display the support.html template."""

    def get(self, request):
        """Handle GET requests and render the support template."""
        return render(request, "support.html")


class ShippingInfoView(View):
    """Class-based view to display the shipping-info.html template."""

    def get(self, request):
        """Handle GET requests and render the shipping-info template."""
        return render(request, "shipping-info.html")


class ReturnPolicyView(View):
    """Class-based view to display the return-policy.html template."""

    def get(self, request):
        """Handle GET requests and render the return-policy template."""
        return render(request, "return-policy.html")


class TermsOfServiceView(View):
    """Class-based view to display the terms-of-service.html template."""

    def get(self, request):
        """Handle GET requests and render the terms-of-service template."""
        return render(request, "tos.html")


class PrivacyView(View):
    """Class-based view to display the privacy.html template."""

    def get(self, request):
        """Handle GET requests and render the privacy template."""
        return render(request, "privacy.html")

@method_decorator(custom_login_required(), name='dispatch')
class AccountView(View):
    """Class-based view to display the account.html template."""

    def get(self, request):
        """Handle GET requests and render the account template."""
        user_detail = User.objects.get(id=request.user.id)

        context = {
            "user_detail": user_detail
        }

        return render(request, "user/account.html", context)
