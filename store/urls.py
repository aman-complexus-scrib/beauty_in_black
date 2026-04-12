from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name='homepage'),
    path('shop/', views.GalleryView.as_view(), name='gallery'),
    path('product/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    
    # Auth
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Customer Actions
    path('cart/', views.CartView.as_view(), name='cart'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('checkout/', views.CheckOutView.as_view(), name='checkout'),
    path('orders/', views.OrderView.as_view(), name='orders'),
    
    # Stripe
    path('create-checkout-session/', views.CreateCheckoutSession.as_view(), name='create_checkout_session'),
    path('success/', views.PaymentSuccess.as_view(), name='payment_success'),
    
    # Static / Info Pages
    path('faqs/', views.FAQsView.as_view(), name='faqs'),
    path('about/', views.AboutUsView.as_view(), name='about_us'),
    path('delivery/', views.DeliveryInfoView.as_view(), name='delivery_info'),
    path('returns/', views.ReturnsPolicyView.as_view(), name='returns_policy'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'), # Kept this one
    path('cookies/', views.CookiePolicyView.as_view(), name='cookie_policy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('sitemap/', views.SitemapView.as_view(), name='sitemap'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    
    # AJAX
    path('add-to-cart/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('add-to-wishlist/', views.ajax_add_to_wishlist, name='ajax_add_to_wishlist'),
    path('remove-from-wishlist/', views.ajax_remove_from_wishlist, name='ajax_remove_from_wishlist'),  # NEW
]