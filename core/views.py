from django.shortcuts import render
from django.db.models import Count
from projects.models import Project, Category, Technology, TechnologyCategory
from skills.models import Skill
from .models import Profile, GlobalConfiguration
from .system_models import SystemNode, SystemConnection
from .dashboard_models import IdentityCore, LiveSystem, ImpactMetric, CapabilitySignal, CurrentFocus
from django.db.models import Prefetch

def dashboard(request):
    featured_projects = Project.objects.filter(featured=True)[:4]
    
    # Sort skills by proficiency (Keep for backward compatibility if needed, but we have CapabilitySignal now)
    skills = Skill.objects.order_by('-proficiency')
    
    # New Dashboard Models
    identity_core = IdentityCore.objects.first()
    live_system = LiveSystem.objects.filter(is_active=True).first()
    impact_metrics = ImpactMetric.objects.filter(is_active=True).order_by('display_order')
    capabilities = CapabilitySignal.objects.filter(is_active=True).order_by('display_order')
    focus_items = CurrentFocus.objects.filter(is_active=True).order_by('display_order')
    
    global_config = GlobalConfiguration.objects.first()

    # Get Categories with counts
    categories = Category.objects.annotate(project_count=Count('project'))

    # System Universe Data
    system_nodes = SystemNode.objects.filter(is_active=True).order_by('-is_core', 'order_index')
    connections = SystemConnection.objects.all()

    # Tech Stack - Efficient Prefetch
    tech_categories = TechnologyCategory.objects.filter(is_active=True).order_by('display_order').prefetch_related(
        Prefetch('technologies', queryset=Technology.objects.filter(is_active=True).order_by('display_order'))
    )

    context = {
        "featured_projects": featured_projects,
        "skills": skills, # Keep for now
        "identity_core": identity_core,
        "live_system": live_system,
        "impact_metrics": impact_metrics,
        "capabilities": capabilities,
        "focus_items": focus_items,
        "global_config": global_config,
        "categories": categories,
        "system_nodes": system_nodes,
        "connections": connections,
        "tech_categories": tech_categories,
    }

    return render(request, "core/dashboard.html", context)
