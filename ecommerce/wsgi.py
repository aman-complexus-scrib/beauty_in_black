import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# Initialize Django
django.setup()

# Create the application object for Vercel
application = get_wsgi_application()
app = application

# Run migrations automatically
try:
    print("Running migrations...")
    call_command('migrate', interactive=False)
    print("Migrations completed successfully.")
except Exception as e:
    print(f"Migration failed: {e}")