from django.shortcuts import render
from projects.models import Project, Category
from skills.models import Skill
from .models import Profile, GlobalConfiguration
from .system_models import SystemNode, SystemConnection
from .dashboard_models import IdentityCore, LiveSystem, ImpactMetric, CapabilitySignal, CurrentFocus

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
    categories = Category.objects.all()

    # System Universe Data
    system_nodes = SystemNode.objects.filter(is_active=True).order_by('-is_core', 'order_index')
    connections = SystemConnection.objects.all()

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
    }

    return render(request, "core/dashboard.html", context)
