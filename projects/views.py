from django.shortcuts import render, get_object_or_404
from .models import Category, Project

def category_projects(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    projects = Project.objects.filter(category=category)

    # Basic filtering logic (can be expanded later)
    tech_filter = request.GET.get('tech')
    if tech_filter:
        projects = projects.filter(tech_stack__icontains=tech_filter)

    context = {
        "category": category,
        "projects": projects,
        "active_filter": tech_filter
    }

    return render(request, "projects/category.html", context)
