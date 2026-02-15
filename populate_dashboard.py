import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from core.dashboard_models import ImpactMetric, CapabilitySignal, FocusArea, GlobalSetting

# Clear existing
ImpactMetric.objects.all().delete()
CapabilitySignal.objects.all().delete()
FocusArea.objects.all().delete()

# 1. Impact Metrics
metrics = [
    ("5+", "Intelligent Systems", 1),
    ("3", "Domains Integrated", 2),
    ("Multi", "Platform Support", 3),
    ("100%", "System Uptime", 4),
]
for t, l, o in metrics:
    ImpactMetric.objects.create(title=t, label=l, order=o)

# 2. Capability Signals
caps = [
    ("System Architecture", 95, 1),
    ("Generative AI / LLMs", 90, 2),
    ("Backend Engineering", 85, 3),
    ("Frontend / 3D Web", 80, 4),
]
for n, s, o in caps:
    CapabilitySignal.objects.create(name=n, strength=s, order=o)

# 3. Focus Areas
focus = [
    ("Architecting Autonomous Agents", 1),
    ("Optimizing Large Language Models (LLMs)", 2),
    ("Designing Scalable Microservices", 3),
    ("Exploring Quantum Computing Interfaces", 4),
]
for t, o in focus:
    FocusArea.objects.create(title=t, order=o)

# 4. Global Settings
GlobalSetting.objects.get_or_create(key="theme_color", value="#00F5FF", description="Main accent color")
GlobalSetting.objects.get_or_create(key="enable_3d", value="true", description="Toggle 3D visualization")

print("Dashboard Content Populated Successfully")
