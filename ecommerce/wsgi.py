import os
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
application = get_wsgi_application()
app = application

# Create Admin automatically on startup
try:
    User = get_user_model()
    if not User.objects.filter(username='admin_user').exists():
        User.objects.create_superuser('admin_user', 'admin@example.com', 'YourSecurePassword123')
        print("Superuser created successfully!")
except Exception as e:
    print(f"Startup task failed: {e}")