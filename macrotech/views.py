"""Application views for the app."""
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.decorators import method_decorator
from django.db.models import Avg, Count

from macrotech.forms import ContactMessageForm, ReviewForm

from .utils import custom_login_required
from .models import BlogPost, Category, NewsletterSubscriber, Product, Review
from .email import EmailContactNotification, NewsletterEmailSender

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
        product = get_object_or_404(Product, id=product_id)

        reviews = product.reviews.all()
        review_count = reviews.count()

        average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        rating_distribution = (
            reviews.values('rating')
                   .annotate(count=Count('rating'))
                   .order_by('-rating')
        )

        rating_counts = {r['rating']: r['count'] for r in rating_distribution}

        full_rating_counts = {i: rating_counts.get(i, 0) for i in range(1, 6)}

        rating_percentages = {
            i: round((count / review_count * 100)) if review_count > 0 else 0
            for i, count in full_rating_counts.items()
        }

        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'reviewer_name': request.user.get_full_name() or request.user.username,
                'reviewer_email': request.user.email
            }

        context = {
            "product": product,
            "reviews": reviews.order_by('-created_at'),
            "form": ReviewForm(initial=initial_data),
            "review_count": review_count,
            "average_rating": average_rating,
            "rating_counts": full_rating_counts,
            "rating_percentages": rating_percentages
        }
        return render(request, "product-details.html", context)

    def post(self, request, product_id):
        """Handle POST request to submit review form data."""
        if not request.user.is_authenticated:
            return JsonResponse({
                'error': 'You must be logged in to post a review.'
            }, status=401)

        product = get_object_or_404(Product, id=product_id)
        form = ReviewForm(request.POST)

        if form.is_valid():
            try:
                if Review.objects.filter(product=product, user=request.user).exists():
                    return JsonResponse({
                        'error': 'You have already reviewed this product.'
                    }, status=400)

                review = form.save(commit=False)
                review.product = product
                review.user = request.user
                review.reviewer_name = request.user.get_full_name() or request.user.username
                review.reviewer_email = request.user.email
                review.save()

                return JsonResponse({
                    'success': 'Your review was posted successfully🤝.',
                    'review': {
                        'rating': review.rating,
                        'title': review.review_title,
                        'description': review.review_description,
                        'reviewer_name': review.reviewer_name,
                        'created_at': review.created_at.strftime('%B %d, %Y')
                    }
                })

            except (ValueError, AttributeError) as e:
                print(f'Error: {e}')
                return JsonResponse({
                    'error': 'Sorry, there was an issue posting your review. Please try again!'
                }, status=500)
        else:
            errors = {field: error_list[0] for field, error_list in form.errors.items()}
            return JsonResponse({'error': errors}, status=400)


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
        business_category = BlogPost.objects.filter(
            post_category="Business"
            ).order_by(
                "-posted_at").first()

        tech_category = BlogPost.objects.filter(
            post_category="Technology"
            ).order_by(
                "-posted_at").first()

        ent_category = BlogPost.objects.filter(
            post_category="Entertainment"
            ).order_by(
                "-posted_at").first()

        life_category = BlogPost.objects.filter(
            post_category="Lifestyle"
            ).order_by(
                "-posted_at").first()

        pol_category = BlogPost.objects.filter(
            post_category="Politics"
            ).order_by(
                "-posted_at").first()

        recent_blogs = BlogPost.objects.all().order_by("-posted_at")[:6]


        context = {
            "recent_blogs": recent_blogs,
            "business_category": business_category,
            "tech_category": tech_category,
            "ent_category": ent_category,
            "life_category": life_category,
            "pol_category": pol_category
        }
        return render(request, "blog.html", context)


class BlogDetailView(View):
    """Class-based view to display the blog-details.html template."""

    def get(self, request, post_id):
        """Handle GET requests and render the blog-details template."""
        blog_post = get_object_or_404(BlogPost, id=post_id)

        categories = BlogPost.objects.values('post_category').annotate(
            count=Count('post_category')).order_by('post_category')

        recent_posts = BlogPost.objects.exclude(
                id=post_id).order_by("-posted_at")[:5]

        tags = [tag.strip() for tag in blog_post.post_tags.split(' ')]

        context = {
            "blog_post": blog_post,
            "categories": categories,
            "recent_posts": recent_posts,
            "tags": tags
        }
        return render(request, "blog-details.html", context)


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

class NewsletterView(View):
    """Handle Newsletter Subscription"""

    def post(self, request, *args, **kwargs):
        """Handle POST request to subscribe to the newsletter."""
        email = request.POST.get('email', '').strip().lower()

        try:
            validate_email(email)

            if NewsletterSubscriber.objects.filter(email=email).exists():
                return JsonResponse(
                    {'error': 'This email is already subscribed to the mailing list'}
                )
            recipient = NewsletterSubscriber(email=email)

            email_sender = NewsletterEmailSender(email)
            if email_sender.send():
                recipient.save()
                return JsonResponse({
                    'success': 'Welcome aboard! 🚀 Thank you for subscribing to our newsletter! 🎉'
                })
            else:
                return JsonResponse({'error': 'Email Notification Error. Please Try Again!'})

        except ValidationError:
            return JsonResponse({'error': 'Invalid email address'})

        except Exception as e:
            print(f"Unhandled error: {e}")
            return JsonResponse({
                'error': 'An error occurred while processing your request. Please try again later.'
            })

    def get(self, request, *args, **kwargs):
        """Handle GET request for the newsletter subscription."""
        return JsonResponse({'error': 'Invalid request method'}, status=405)


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
