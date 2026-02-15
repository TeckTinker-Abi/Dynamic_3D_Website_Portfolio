from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from django.urls import reverse
from django.contrib import messages
from .forms import (
    SystemNodeForm, SystemConnectionForm, ProjectForm, CategoryForm,
    ImpactMetricForm, CapabilitySignalForm, CurrentFocusForm, GlobalSettingForm, IdentityCoreForm, LiveSystemForm,
    GlobalConfigurationForm, TechnologyCategoryForm, TechnologyForm
)
from core.models import GlobalConfiguration, Profile
from core.system_models import SystemNode, SystemConnection
from core.dashboard_models import ImpactMetric, CapabilitySignal, CurrentFocus, GlobalSetting, IdentityCore, LiveSystem
from projects.models import Project, Category, Technology, TechnologyCategory

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    # 1. Portfolio Status Summary
    stats = {
        'total_projects': Project.objects.count(),
        'total_categories': Category.objects.count(),
        'active_nodes': SystemNode.objects.filter(is_active=True).count(),
        'total_connections': SystemConnection.objects.count(),
        'active_connections': SystemConnection.objects.filter(from_node__is_active=True, to_node__is_active=True).count(),
    }
    
    # 2. System Universe Status
    core_node = SystemNode.objects.filter(is_core=True).first()
    system_status = {
        'core_node': core_node,
        'domain_nodes': SystemNode.objects.filter(is_core=False).count(),
        'warnings': []
    }
    if not core_node:
        system_status['warnings'].append("No Core Node Defined!")
    if stats['total_connections'] == 0:
        system_status['warnings'].append("No Connections Defined!")

    # 3. Project Overview
    project_overview = {
        'by_category': Category.objects.annotate(project_count=Count('project')).filter(project_count__gt=0),
        'recent': Project.objects.order_by('-created_at').first(),
        'missing_data': Project.objects.filter(Q(github_link__isnull=True) | Q(live_link__isnull=True)).count()
    }

    # 4. Category Overview
    category_overview = {
        'all': Category.objects.annotate(project_count=Count('project')),
        'empty': Category.objects.annotate(project_count=Count('project')).filter(project_count=0)
    }

    # 5. Dashboard Content Status
    content_status = {
        'metrics': ImpactMetric.objects.filter(is_active=True).count(),
        'capabilities': CapabilitySignal.objects.filter(is_active=True).count(),
        'focus_areas': CurrentFocus.objects.filter(is_active=True).count(),
        'settings': 1 if GlobalConfiguration.objects.exists() else 0
    }

    # 6. Global Config
    config = GlobalConfiguration.objects.first()

    context = {
        'stats': stats,
        'system_status': system_status,
        'project_overview': project_overview,
        'category_overview': category_overview,
        'content_status': content_status,
        'global_config': config,
        'identity_core': IdentityCore.objects.first(),
        'live_system': LiveSystem.objects.first(),
    }
    return render(request, 'admin_custom/dashboard.html', context)

# --- GENERIC DELETE VIEW ---
def generic_delete(request, model_class, pk, redirect_url_name, content_label):
    obj = get_object_or_404(model_class, pk=pk)
    if request.method == 'POST':
        obj.delete()
        admin_url = redirect_url_name if ':' in redirect_url_name else f'custom_admin:{redirect_url_name}'
        return redirect(admin_url)
    
    cancel_url = reverse(redirect_url_name if ':' in redirect_url_name else f'custom_admin:{redirect_url_name}')
    return render(request, 'admin_custom/delete_confirmation.html', {
        'object': obj,
        'content_label': content_label,
        'cancel_url': cancel_url
    })

# --- GENERIC EDIT VIEW ---
def generic_edit(request, model_class, form_class, pk=None, redirect_url='custom_admin:dashboard', title="Edit Item", desc="Update details", delete_url_name=None):
    item = get_object_or_404(model_class, pk=pk) if pk else None
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = form_class(instance=item)
    
    context = {
        'form': form,
        'page_title': title,
        'page_description': desc,
        'delete_url': reverse(delete_url_name, args=[pk]) if pk and delete_url_name else None
    }
    
    return render(request, 'admin_custom/form.html', context)

# --- SYSTEM UNIVERSE ---
@user_passes_test(is_admin)
def system_universe(request):
    # Nodes Filtering
    nodes = SystemNode.objects.all().order_by('-is_core', 'order_index')
    node_search = request.GET.get('node_search')
    node_filter = request.GET.get('node_filter')
    
    if node_search:
        nodes = nodes.filter(Q(title__icontains=node_search) | Q(slug__icontains=node_search))
    
    if node_filter == 'active':
        nodes = nodes.filter(is_active=True)
    elif node_filter == 'inactive':
        nodes = nodes.filter(is_active=False)
    elif node_filter == 'core':
        nodes = nodes.filter(is_core=True)

    # Connections Filtering
    connections = SystemConnection.objects.all()
    conn_search = request.GET.get('conn_search')
    conn_filter = request.GET.get('conn_filter')

    if conn_search:
        connections = connections.filter(
            Q(from_node__title__icontains=conn_search) | 
            Q(to_node__title__icontains=conn_search)
        )
    
    if conn_filter == 'active':
        connections = connections.filter(from_node__is_active=True, to_node__is_active=True)
    elif conn_filter in ['data', 'inference', 'feedback']:
        connections = connections.filter(flow_type=conn_filter)

    return render(request, 'admin_custom/system_universe.html', {
        'nodes': nodes, 
        'connections': connections,
        'node_search': node_search or '',
        'node_filter': node_filter or 'all',
        'conn_search': conn_search or '',
        'conn_filter': conn_filter or 'all'
    })

@user_passes_test(is_admin)
def node_edit(request, pk=None):
    return generic_edit(request, SystemNode, SystemNodeForm, pk, 'custom_admin:system_universe', 
                       "Manage System Node", "Define a component of your system architecture.",
                       delete_url_name='custom_admin:node_delete')

@user_passes_test(is_admin)
def node_delete(request, pk):
    return generic_delete(request, SystemNode, pk, 'custom_admin:system_universe', "System Node")

@user_passes_test(is_admin)
def connection_edit(request, pk=None):
    return generic_edit(request, SystemConnection, SystemConnectionForm, pk, 'custom_admin:system_universe',
                        "Manage Connection", "Define data flow between nodes.")

# --- PROJECTS & CATEGORIES ---
@user_passes_test(is_admin)
def projects_list(request):
    projects = Project.objects.all().order_by('-updated_at')
    
    # Filters
    status_filter = request.GET.get('status')
    featured_filter = request.GET.get('featured')
    search_query = request.GET.get('q')

    if status_filter == 'active':
        projects = projects.filter(is_active=True)
    elif status_filter == 'draft':
        projects = projects.filter(is_active=False)
    
    if featured_filter == 'true':
        projects = projects.filter(featured=True)

    if search_query:
        projects = projects.filter(Q(title__icontains=search_query) | Q(slug__icontains=search_query))

    return render(request, 'admin_custom/projects.html', {
        'projects': projects,
        'current_status': status_filter,
        'current_featured': featured_filter,
        'search_query': search_query
    })

@user_passes_test(is_admin)
def project_edit(request, pk=None):
    # Custom edit view for specialized template
    project = get_object_or_404(Project, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('custom_admin:projects')
    else:
        form = ProjectForm(instance=project)
    
    page_title = "Edit Project" if pk else "Add New Project"
    
    context = {
        'form': form,
        'page_title': page_title,
        'page_description': "Manage all aspects of your project portfolio.",
    }
    if pk:
        context['delete_url'] = reverse('custom_admin:project_delete', args=[pk])
    
    return render(request, 'admin_custom/project_edit.html', context)

@user_passes_test(is_admin)
def project_delete(request, pk):
    return generic_delete(request, Project, pk, 'custom_admin:projects', "Project")

@user_passes_test(is_admin)
def categories_list(request):
    categories = Category.objects.annotate(project_count=Count('project')).order_by('order', 'name')
    
    # Filters
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')

    if status_filter == 'active':
        categories = categories.filter(is_active=True)
    elif status_filter == 'inactive':
        categories = categories.filter(is_active=False)
    elif status_filter == 'empty':
        categories = categories.filter(project_count=0)

    if search_query:
        categories = categories.filter(Q(name__icontains=search_query) | Q(slug__icontains=search_query))

    return render(request, 'admin_custom/categories.html', {
        'categories': categories,
        'current_status': status_filter,
        'search_query': search_query
    })

@user_passes_test(is_admin)
def category_edit(request, pk=None):
    item = get_object_or_404(Category, pk=pk) if pk else None
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('custom_admin:categories')
    else:
        form = CategoryForm(instance=item)
    
    context = {
        'form': form,
        'page_title': "Edit Category" if pk else "Add New Category",
        'delete_url': reverse('custom_admin:category_delete', args=[pk]) if pk else None
    }
    return render(request, 'admin_custom/category_edit.html', context)

@user_passes_test(is_admin)
def category_delete(request, pk):
    return generic_delete(request, Category, pk, 'custom_admin:categories', "Category")

# --- DASHBOARD CONTENT ---
@user_passes_test(is_admin)
def dashboard_content(request):
    metrics = ImpactMetric.objects.all()
    capabilities = CapabilitySignal.objects.all()
    current_focus = CurrentFocus.objects.all()
    return render(request, 'admin_custom/dashboard_content.html', {
        'metrics': metrics,
        'capabilities': capabilities,
        'current_focus': current_focus
    })

@user_passes_test(is_admin)
def metric_edit(request, pk=None):
    return generic_edit(request, ImpactMetric, ImpactMetricForm, pk, 'custom_admin:dashboard_content', 
                       "Impact Metric", "Key statistics displayed on the dashboard.")

@user_passes_test(is_admin)
def capability_edit(request, pk=None):
    return generic_edit(request, CapabilitySignal, CapabilitySignalForm, pk, 'custom_admin:dashboard_content', 
                       "Capability Signal", "Skill or technology proficiency level.")

@user_passes_test(is_admin)
def current_focus_edit(request, pk=None):
    return generic_edit(request, CurrentFocus, CurrentFocusForm, pk, 'custom_admin:dashboard_content', 
                       "Current Focus", "Current area of research or interest.")

# --- SETTINGS ---
@user_passes_test(is_admin)
def global_settings(request):
    # Singleton pattern: Get the first one or create it if none exists (checking strict singleton compliance)
    config = GlobalConfiguration.objects.first()
    if not config:
        config = GlobalConfiguration() # Prepare new instance (not saved yet)
    
    if request.method == 'POST':
        form = GlobalConfigurationForm(request.POST, request.FILES, instance=config)
        if form.is_valid():
            form.save()
            messages.success(request, "Global configuration updated successfully.")
            return redirect('custom_admin:global_settings')
    else:
        form = GlobalConfigurationForm(instance=config)

    return render(request, 'admin_custom/settings.html', {
        'form': form,
        'page_title': "Global Configuration",
        'page_description': "Manage platform behavior, 3D settings, and themes.",
    })

@user_passes_test(is_admin)
def identity_core_view(request):
    item = IdentityCore.objects.first()
    
    if request.method == 'POST':
        form = IdentityCoreForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Identity Core updated successfully.")
            return redirect('custom_admin:identity_core')
    else:
        form = IdentityCoreForm(instance=item)
        
    return render(request, 'admin_custom/identity_core.html', {
        'form': form,
        'page_title': "Identity Core",
        'item': item
    })

@user_passes_test(is_admin)
def live_system_view(request):
    item = LiveSystem.objects.first()
    
    if request.method == 'POST':
        form = LiveSystemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Live System Status updated successfully.")
            return redirect('custom_admin:live_system')
    else:
        form = LiveSystemForm(instance=item)
        
    return render(request, 'admin_custom/live_system.html', {
        'form': form,
        'page_title': "Live System Status",
        'item': item
    })

# --- TECHNICAL STACK MANAGEMENT ---
@user_passes_test(is_admin)
def tech_stack_view(request):
    categories = TechnologyCategory.objects.prefetch_related('technologies').order_by('display_order', 'name')
    
    return render(request, 'admin_custom/tech_stack.html', {
        'categories': categories,
    })

@user_passes_test(is_admin)
def tech_category_edit(request, pk=None):
    return generic_edit(request, TechnologyCategory, TechnologyCategoryForm, pk, 'custom_admin:tech_stack', 
                       "Technology Category", "Group technologies by domain (e.g., Languages, Frameworks).",
                       delete_url_name='custom_admin:tech_category_delete')

@user_passes_test(is_admin)
def tech_category_delete(request, pk):
    return generic_delete(request, TechnologyCategory, pk, 'custom_admin:tech_stack', "Technology Category")

@user_passes_test(is_admin)
def technology_edit(request, pk=None):
    return generic_edit(request, Technology, TechnologyForm, pk, 'custom_admin:tech_stack', 
                       "Technology / Tool", "Manage individual technologies, languages, or tools.",
                       delete_url_name='custom_admin:technology_delete')

@user_passes_test(is_admin)
def technology_delete(request, pk):
    return generic_delete(request, Technology, pk, 'custom_admin:tech_stack', "Technology")


