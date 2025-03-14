import os
from Backend.saltnlight.wsgi import application  # Import Django's WSGI app

# Set the default settings module (Django needs this)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.saltnlight.settings")

# Vercel expects an `app` variable
app = application