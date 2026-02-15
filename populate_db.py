import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Profile
from skills.models import Skill
from projects.models import Category
from django.utils.text import slugify

# Create Superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("Superuser 'admin' created with password 'admin'")
else:
    print("Superuser 'admin' already exists")

# Create Profile
if not Profile.objects.exists():
    Profile.objects.create(
        full_name="M. Abishek",
        title="AI Engineer | ML Architect | Full Stack Developer",
        bio="B.E Computer Science Engineering (AI & ML). Passionate about intelligent systems and scalable architecture.",
        detailed_bio="High-performance engineer specializing in IoT, Backend Systems, and AI Integration.",
        email="abishek@example.com"
    )
    print("Profile created")
else:
    print("Profile already exists")

# Create Categories
categories = [
    "IoT Projects",
    "Web Applications",
    "Desktop Applications",
    "AI / ML / GenAI Projects",
    "API / Backend / Microservices"
]

for cat_name in categories:
    slug = slugify(cat_name)
    Category.objects.get_or_create(name=cat_name, slug=slug, defaults={'description': f"Projects related to {cat_name}"})

print(f"{len(categories)} categories processed")

# Create Skills
skills_data = [
    ("System Architecture", 95, "Backend & Platforms"),
    ("Hardware-Software Integration", 95, "IoT & Embedded Systems"),
    ("API & Microservices Design", 95, "Backend & Platforms"),
    ("AI / LLM Integration", 70, "AI / ML / GenAI"),
    ("UI / Experience Design", 70, "Applications"),
]

for name, proficiency, category in skills_data:
    Skill.objects.get_or_create(name=name, proficiency=proficiency, category=category)

print(f"{len(skills_data)} skills processed")
