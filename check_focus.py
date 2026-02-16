import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from core.dashboard_models import CurrentFocus, ImpactMetric, CapabilitySignal

print("--- CurrentFocus ---")
count = CurrentFocus.objects.count()
print(f"CurrentFocus count: {count}")
if count > 0:
    for item in CurrentFocus.objects.all():
        print(f"- {item.title} (Active: {item.is_active})")

print("\n--- ImpactMetric ---")
count = ImpactMetric.objects.count()
print(f"ImpactMetric count: {count}")
if count > 0:
    for item in ImpactMetric.objects.all():
        print(f"- {item.title} (Active: {item.is_active})")

print("\n--- CapabilitySignal ---")
count = CapabilitySignal.objects.count()
print(f"CapabilitySignal count: {count}")
