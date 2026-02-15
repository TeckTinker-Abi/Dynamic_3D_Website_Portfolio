import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')
django.setup()

from core.system_models import SystemNode, SystemConnection
from projects.models import Category

# Initial Cleanup
SystemNode.objects.all().delete()
SystemConnection.objects.all().delete()

# 1. Create Core Node
core_node = SystemNode.objects.create(
    title="INTELLIGENCE CORE",
    slug="core-ai",
    description="Central AI Orchestration Layer",
    color="#7B61FF",
    is_core=True,
    active=True
)

# 2. Create Domain Nodes
domains = [
    {"title": "IoT & Embedded", "slug": "iot", "color": "#00F5FF", "order": 1},
    {"title": "Backend APIs", "slug": "backend", "color": "#00F5FF", "order": 2},
    {"title": "GenAI Models", "slug": "genai", "color": "#7B61FF", "order": 3},
    {"title": "Applications", "slug": "apps", "color": "#10B981", "order": 4},
]

created_nodes = {}
for d in domains:
    # Try to link to category if exists (fuzzy match)
    cat = Category.objects.filter(name__icontains=d['title'].split(' ')[0]).first()
    
    node = SystemNode.objects.create(
        title=d['title'],
        slug=d['slug'],
        color=d['color'],
        order_index=d['order'],
        active=True,
        category=cat
    )
    created_nodes[d['slug']] = node

# 3. Create Connections (Data Flows)
connections = [
    ("iot", core_node, "data"),
    (core_node, "backend", "inference"),
    ("backend", "apps", "data"),
    ("apps", "genai", "feedback"),
    ("genai", core_node, "inference"),
]

for src, dst, flow in connections:
    # Resolve src
    s_node = created_nodes[src] if isinstance(src, str) else src
    d_node = created_nodes[dst] if isinstance(dst, str) else dst
    
    SystemConnection.objects.create(
        from_node=s_node,
        to_node=d_node,
        flow_type=flow,
        strength=1.5
    )

print("System Universe populated with Core + 4 Domains + Connections")
