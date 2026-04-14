"""
WSGI config for beauty_in_black project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

# IMPORTANT: Ensure 'beauty_in_black.settings' matches your folder name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beauty_in_black.settings')

application = get_wsgi_application()

# This alias is required for Vercel to find the gateway
app = application