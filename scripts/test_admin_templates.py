import os
import sys
import django

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')

django.setup()

# Check settings configuration
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from projects.models import Project, Category
from custom_admin.forms import ProjectForm
from django.test import RequestFactory

def run_test():
    print("--- Starting Admin Template Verification ---")

    # 1. Setup Data
    try:
        user = User.objects.filter(is_superuser=True).first()
        if not user:
            print("WARNING: No superuser found. Skipping view tests.")
            return

        cat, _ = Category.objects.get_or_create(name="Test Category", slug="test-cat")
        proj, _ = Project.objects.get_or_create(title="Test Render Title", slug="test-render-slug", category=cat)
        print("Data setup complete.")
    except Exception as e:
        print(f"CRITICAL: Database setup failed: {e}")
        return

    # 2. Test Project List Template
    try:
        # Request factory needed for url/static tags in base template
        factory = RequestFactory()
        request = factory.get('/admin/projects/')
        request.user = user
        
        # We manually render to avoid middleware complexity, but we need 'request' in context for likely usage
        context = {'projects': [proj], 'request': request}

        content = render_to_string('admin_custom/projects.html', context)
        
        if "{{ project.title }}" in content or "{{project.title}}" in content:
            print("❌ FAIL: Project List template contains literal curly braces for title.")
        elif "Test Render Title" in content:
            print("✅ PASS: Project List template successfully rendered the title.")
        else:
            print("⚠️ WARNING: content generated but title not found. Check logic.")
            
    except Exception as e:
        print(f"❌ ERROR rendering Project List: {e}")

    # 3. Test Project Edit Template
    try:
        if not settings.INSTALLED_APPS:
             print("Apps not installed?")

        form = ProjectForm(instance=proj)
        context = {
            'form': form,
            'page_title': 'Test Edit Project',
            'page_description': 'Testing...',
            'request': request
        }
        content = render_to_string('admin_custom/project_edit.html', context)
        
        if "Basic Information" in content and "Trust Signals" in content:
             print("✅ PASS: Project Edit template rendered key sections.")
        else:
             print("❌ FAIL: Project Edit template missing sections.")

    except Exception as e:
        print(f"❌ ERROR rendering Project Edit: {e}")

if __name__ == "__main__":
    run_test()
