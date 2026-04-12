from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from django.views import View
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.views.generic import TemplateView
import stripe
import json

from store.models import Product, Category, Brand, Cart, Order, Customer, Wishlist

stripe.api_key = settings.STRIPE_SECRET_KEY

# ─── STATIC & INFO VIEWS ────────────────────────────────────
class AboutUsView(TemplateView):
    template_name = 'about_us.html'

class DeliveryInfoView(TemplateView):
    template_name = 'delivery_info.html'

class ReturnsPolicyView(TemplateView):
    template_name = 'returns_policy.html'

class FAQsView(TemplateView):
    template_name = 'faqs.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'privacy_policy.html'

class CookiePolicyView(TemplateView):
    template_name = 'cookie_policy.html'

class TermsView(TemplateView):
    template_name = 'terms.html'

class SitemapView(TemplateView):
    template_name = 'sitemap.html'

# ─── CONTACT VIEW ──────────────────────────────────────────
class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

    def post(self, request):
        return render(request, 'contact.html', {'contact_success': True})

# ─── MAIN STORE VIEWS ───────────────────────────────────────
class Index(View):
    def get(self, request):
        categories = Category.objects.all()[:4]
        products = Product.objects.all().order_by('-id')[:8]
        random_product = Product.objects.order_by('?').first()

        return render(request, 'index.html', {
            'products': products,
            'categories': categories,
            'random_product': random_product,
        })

class GalleryView(View):
    def get(self, request):
        products = Product.objects.select_related('category', 'brand').all()

        category_slug = request.GET.get('category')
        category = None
        related_categories = None

        if category_slug:
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                products = products.filter(category=category)
                parent = category.parent
                if parent:
                    related_categories = Category.objects.filter(parent=parent)
                else:
                    related_categories = Category.objects.filter(parent__isnull=True)

        q = request.GET.get('q')
        if q:
            products = products.filter(
                models.Q(name__icontains=q) |
                models.Q(short_description__icontains=q) |
                models.Q(description__icontains=q) |
                models.Q(category__name__icontains=q) |
                models.Q(brand__name__icontains=q)
            )

        selected_brands = request.GET.getlist('brand')
        if selected_brands:
            products = products.filter(brand__slug__in=selected_brands)

        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price:
            products = products.filter(price__gte=min_price)
        if max_price:
            products = products.filter(price__lte=max_price)

        sort = request.GET.get('sort')
        if sort == 'price-asc':
            products = products.order_by('price', 'id')
        elif sort == 'price-desc':
            products = products.order_by('-price', '-id')
        elif sort == 'name':
            products = products.order_by('name', 'id')
        elif sort == 'newest':
            products = products.order_by('-id')

        paginator = Paginator(products, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'product_gallery.html', {
            'products': page_obj.object_list,
            'page_obj': page_obj,
            'paginator': paginator,
            'category': category,
            'categories': Category.objects.filter(parent__isnull=True),
            'brands': Brand.objects.all().order_by('name'),
            'related_categories': related_categories,
            'selected_brands': selected_brands,
            'selected_category_slug': category_slug,
            'min_price': min_price,
            'max_price': max_price,
            'sort': sort,
            'q': q,
        })

class ProductDetail(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        is_in_stock = product.stock_count > 0
        return render(request, 'product_detail.html', {
            'product': product,
            'is_in_stock': is_in_stock
        })

# ─── AUTHENTICATION ──────────────────────────────────────────
class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        d = request.POST
        if Customer.objects.filter(email=d.get('email')).exists():
            return render(request, 'signup.html', {'error': "Email exists", 'values': d})
        user = Customer.objects.create_user(
            username=d.get('email'),
            email=d.get('email'),
            password=d.get('password'),
            phone=d.get('phone'),
            first_name=d.get('firstname'),
            last_name=d.get('lastname')
        )
        login(request, user)
        return redirect('homepage')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'homepage'))
        return render(request, 'login.html', {'error': 'Invalid credentials'})

def logout_view(request):
    logout(request)
    return redirect('login')

# ─── CART & CHECKOUT ────────────────────────────────────────
class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            cart_items = Cart.objects.filter(customer=request.user).select_related('product')
            total = sum(item.product.price * item.quantity for item in cart_items)
        else:
            cart_items = []
            total = 0
        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

    def post(self, request):
        """
        Handles update-quantity and remove actions submitted from cart.html forms.
        Both forms POST to /cart/ with hidden fields: product_id and action.
        """
        if not request.user.is_authenticated:
            return redirect('login')

        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product = get_object_or_404(Product, id=product_id)

        if action == 'remove':
            Cart.objects.filter(customer=request.user, product=product).delete()

        elif action == 'update':
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
            item, _ = Cart.objects.get_or_create(customer=request.user, product=product)
            item.quantity = quantity
            item.save()

        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class CheckOutView(View):
    def get(self, request):
        cart_items = Cart.objects.filter(customer=request.user).select_related('product')
        if not cart_items.exists():
            return redirect('cart')
        total = sum(i.product.price * i.quantity for i in cart_items)
        return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

    def post(self, request):
        request.session['checkout_info'] = {
            'address': request.POST.get('address'),
            'phone': request.POST.get('phone')
        }
        return redirect('create_checkout_session')


@method_decorator(login_required, name='dispatch')
class CreateCheckoutSession(View):
    def get(self, request):
        cart_items = Cart.objects.filter(customer=request.user).select_related('product')
        if not cart_items.exists():
            return redirect('cart')

        line_items = [{
            'price_data': {
                'currency': 'gbp',
                'product_data': {'name': i.product.name},
                'unit_amount': int(round(i.product.price * 100))
            },
            'quantity': i.quantity
        } for i in cart_items]

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri('/success/') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri('/cart/'),
            metadata={'user_id': str(request.user.id)}
        )
        request.session['stripe_session_id'] = session.id
        return redirect(session.url, code=303)


@method_decorator(login_required, name='dispatch')
class PaymentSuccess(View):
    def get(self, request):
        session_id = request.GET.get('session_id')
        if session_id and session_id == request.session.get('stripe_session_id'):
            stripe_session = stripe.checkout.Session.retrieve(session_id)
            if stripe_session.payment_status == 'paid':
                cart_items = Cart.objects.filter(customer=request.user).select_related('product')
                info = request.session.get('checkout_info', {})
                for item in cart_items:
                    Order.objects.create(
                        customer=request.user,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price,
                        address=info.get('address', ''),
                        phone=info.get('phone', ''),
                        paid=True
                    )
                cart_items.delete()
                return render(request, 'payment_success.html')
        return redirect('cart')


@method_decorator(login_required, name='dispatch')
class OrderView(View):
    def get(self, request):
        orders = Order.objects.filter(customer=request.user).order_by('-created_at')
        return render(request, 'orders.html', {'orders': orders})


# ─── WISHLIST ────────────────────────────────────────────────
class WishlistView(View):
    def get(self, request):
        if request.user.is_authenticated:
            wishlist_items = Wishlist.objects.filter(customer=request.user).select_related('product')
        else:
            wishlist_items = []
        return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


# ─── AJAX ENDPOINTS ──────────────────────────────────────────

def ajax_add_to_cart(request):
    """
    Accepts JSON POST: { "product_id": "123", "quantity": 1 }
    Called from product_detail.html, index.html, and wishlist.html via fetch().
    Requires login — returns JSON so the page can show a toast without redirecting.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'login_required'}, status=401)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return JsonResponse({'success': False, 'error': 'Missing product_id'}, status=400)

    product = get_object_or_404(Product, id=product_id)

    if product.stock_count < 1:
        return JsonResponse({'success': False, 'error': 'Out of stock'})

    item, created = Cart.objects.get_or_create(
        customer=request.user,
        product=product
    )
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    cart_count = Cart.objects.filter(customer=request.user).count()
    return JsonResponse({'success': True, 'cart_count': cart_count})


def ajax_add_to_wishlist(request):
    """
    Accepts JSON POST: { "product_id": "123" }
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'login_required'}, status=401)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    _, created = Wishlist.objects.get_or_create(customer=request.user, product=product)
    return JsonResponse({'success': True, 'created': created})


def ajax_remove_from_wishlist(request):
    """
    Accepts JSON POST: { "product_id": "123" }
    Removes the product from the current user's wishlist.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'login_required'}, status=401)

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    Wishlist.objects.filter(customer=request.user, product_id=product_id).delete()
    return JsonResponse({'success': True})