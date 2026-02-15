from django.db import models
from django.core.exceptions import ValidationError
from projects.models import Category

class SystemNode(models.Model):
    title = models.CharField(max_length=100, help_text="Display name of the node")
    slug = models.SlugField(unique=True, help_text="Unique identifier for routing")
    description = models.TextField(blank=True, help_text="Tooltip content")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, help_text="Links to Project Category")
    
    # Visuals
    color = models.CharField(max_length=7, default="#00F5FF", help_text="Hex Color e.g. #00F5FF")
    is_core = models.BooleanField(default=False, help_text="Is this the Central Intelligence Node? Only one allowed.")
    order_index = models.IntegerField(default=0, help_text="Orbit position order (0-12)")
    is_active = models.BooleanField(default=True, help_text="Toggle visibility in frontend")
    
    # Optional Advanced
    importance_weight = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)], help_text="Controls node size/prominence (1-5)")
    icon = models.ImageField(upload_to='system_icons/', blank=True, null=True, help_text="Optional visual icon")
    pulse_enabled = models.BooleanField(default=True, help_text="Controls glow pulse animation")

    class Meta:
        ordering = ['-is_core', 'order_index']
        verbose_name = "System Node"
        verbose_name_plural = "System Nodes"

    def clean(self):
        # Validate Color Hex
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValidationError({'color': 'Color must be a valid 6-char hex code (e.g. #00F5FF)'})
        
        # Ensure only one core node exists
        if self.is_core:
            # Check if another core exists and it's not self
            existing_core = SystemNode.objects.filter(is_core=True).exclude(pk=self.pk)
            if existing_core.exists():
                raise ValidationError({'is_core': 'Only one Core Node is allowed. Please unset the existing core first.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({'CORE' if self.is_core else 'NODE'})"

class SystemConnection(models.Model):
    from_node = models.ForeignKey(SystemNode, related_name='connections_out', on_delete=models.CASCADE)
    to_node = models.ForeignKey(SystemNode, related_name='connections_in', on_delete=models.CASCADE)
    flow_type = models.CharField(max_length=50, choices=[
        ('data', 'Data Flow'),
        ('inference', 'AI Inference'),
        ('feedback', 'Feedback Loop')
    ], default='data')
    strength = models.IntegerField(default=1, choices=[(i, i) for i in range(1, 6)], help_text="Flow intensity (1-5)")
    is_bidirectional = models.BooleanField(default=False, help_text="Two-way flow")

    class Meta:
        unique_together = ('from_node', 'to_node')
        verbose_name = "System Connection"
        verbose_name_plural = "System Connections"

    def clean(self):
        # Prevent self-connection
        if self.from_node == self.to_node:
            raise ValidationError("A node cannot connect to itself.")
        
        # Ensure both nodes are active
        if not self.from_node.is_active or not self.to_node.is_active:
            raise ValidationError("Both nodes must be active to create a connection.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.from_node} -> {self.to_node} [{'BI' if self.is_bidirectional else 'UNI'}]"
