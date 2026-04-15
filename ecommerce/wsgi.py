import os
import django
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command # This imports the 'migrate' tool

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

# 1. Start Django
django.setup()

# 2. Create the application for Vercel
application = get_wsgi_application()
app = application

# 3. The "Builder": This creates your Neon tables automatically
try:
    print("Connecting to Neon and building tables...")
    call_command('migrate', interactive=False)
    print("Neon database is ready!")
except Exception as e:
    print(f"Database setup failed: {e}")