from django.shortcuts import render, get_object_or_404
from .models import Category, Project

def category_projects(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    projects = Project.objects.filter(category=category, is_active=True).order_by('?') # Random order for now or use specific ordering

    # Stats
    production_count = projects.filter(deployment_status='Production').count()
    research_count = projects.filter(complexity='Research').count()

    # Basic filtering logic (can be expanded later)
    tech_filter = request.GET.get('tech')
    if tech_filter:
        projects = projects.filter(tech_stack__icontains=tech_filter)

    context = {
        "category": category,
        "projects": projects,
        "active_filter": tech_filter,
        "production_count": production_count,
        "research_count": research_count,
    }

    return render(request, "projects/category.html", context)

def project_detail(request, category_slug, project_slug):
    project = get_object_or_404(Project, category__slug=category_slug, slug=project_slug)
    
    context = {
        "project": project,
    }
    return render(request, "projects/detail.html", context)
