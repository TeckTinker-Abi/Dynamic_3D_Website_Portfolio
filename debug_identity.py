
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_project.settings")
django.setup()

from core.dashboard_models import IdentityCore

try:
    identity = IdentityCore.objects.first()
    if identity:
        print(f"Full Name: '{identity.full_name}'")
        print(f"Profile Title: '{identity.profile_title}'")
        print(f"Slogan: '{identity.slogan}'")
    else:
        print("No IdentityCore record found.")
except Exception as e:
    print(f"Error: {e}")
