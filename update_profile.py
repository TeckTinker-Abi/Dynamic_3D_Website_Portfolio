import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from core.models import Profile

if not Profile.objects.exists():
    # ... previous create Logic ...
    pass
else:
    profile = Profile.objects.first()
    profile.full_name = "M. Abishek"
    profile.title = "Intelligent Systems & GenAI Engineer"
    profile.philosophy = "Designing systems where intelligence meets the physical world."
    profile.current_building = "LLM-driven intelligent automation system"
    profile.focus_areas = "GenAI architectures\nLLM orchestration\nIntelligent automation systems\nScalable AI-driven platforms"
    profile.save()
    print("Profile Updated with Command Center Details")
