# AJAX endpoints handle cart / wishlist / checkout dynamically
from django.urls import path
from . import views

urlpatterns = [
    # ── INDEX & STATIC PAGES ─────────────────────────────────────────
    path('', views.Index.as_view(), name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('returns-policy/', views.returns_policy, name='returns_policy'),
    path('cookie-policy/', views.cookie_policy, name='cookie_policy'),
    path('about-us/', views.about_us, name='about_us'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('terms/', views.terms, name='terms'),
    path('orders/', views.orders, name='orders'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),

    # ── AUTHENTICATION ───────────────────────────────────────────────
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── CART AJAX ENDPOINTS ──────────────────────────────────────────
    path('ajax/add-to-cart/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('ajax/remove-from-cart/', views.ajax_remove_from_cart, name='ajax_remove_from_cart'),
    path('ajax/cart-data/', views.ajax_cart_data, name='ajax_cart_data'),

    # ── WISHLIST AJAX ENDPOINTS ──────────────────────────────────────
    path('ajax/add-to-wishlist/', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist'),
    path('ajax/remove-from-wishlist/', views.ajax_remove_from_wishlist, name='ajax_remove_from_wishlist'),
    path('ajax/wishlist-data/', views.ajax_wishlist_data, name='ajax_wishlist_data'),
    path('ajax/wishlist-to-cart/', views.ajax_wishlist_to_cart, name='ajax_wishlist_to_cart'),

    # ── ORDERS AJAX ENDPOINT ─────────────────────────────────────────
    path('ajax/orders/', views.ajax_orders, name='ajax_orders'),

    # ── STRIPE PAYMENT ENDPOINTS ─────────────────────────────────────
    path('checkout/', views.CreateCheckoutSession.as_view(), name='checkout'),
    path('success/', views.PaymentSuccess.as_view(), name='success'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),

    # ── REVIEWS ──────────────────────────────────────────────────────
    path('review/', views.review_page, name='review'),
]