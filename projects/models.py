from django.db import models
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, help_text="Short description (1 line)")
    scope_statement = models.TextField(blank=True, null=True, help_text="Scope statement (2-3 lines)")
    icon = models.ImageField(upload_to="category_icons/", blank=True, null=True)
    
    # System Mapping
    system_node = models.ForeignKey('core.SystemNode', on_delete=models.SET_NULL, blank=True, null=True, related_name="categories", help_text="Link to System Universe Node")
    
    # Ordering & Status
    order = models.IntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class TechnologyCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Technology Categories"
        ordering = ['display_order', 'name']

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super(TechnologyCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Technology(models.Model):
    category = models.ForeignKey(TechnologyCategory, on_delete=models.CASCADE, related_name='technologies')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to="tech_icons/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    
    # Optional styling
    color = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color code (e.g. #FF0000)")
    
    class Meta:
        verbose_name_plural = "Technologies"
        ordering = ['category__display_order', 'display_order', 'name']

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.name)
        super(Technology, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
class Project(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_description = models.TextField()
    full_description = RichTextField(blank=True, null=True)
    
    # Tech Stack
    technologies = models.ManyToManyField(Technology, blank=True, related_name="projects")
    tech_stack = models.JSONField(help_text="List of technologies used (Legacy)", default=list, blank=True)
    
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    docs_link = models.URLField(blank=True, null=True)
    cover_image = models.ImageField(upload_to="projects/")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured = models.BooleanField(default=False)
    
    # Detailed fields
    architecture_image = models.ImageField(upload_to="architecture/", blank=True, null=True)
    problem_statement = RichTextField(blank=True, null=True)
    solution_overview = RichTextField(blank=True, null=True, help_text="High-level system explanation")
    system_architecture = RichTextField(blank=True, null=True, help_text="Layer breakdown and data flow")
    
    # Tech & Capabilities (JSON preferred)
    domain_tags = models.JSONField(default=list, blank=True)
    capabilities = models.JSONField(default=list, blank=True)

    implementation_details = RichTextField(blank=True, null=True)
    results = RichTextField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    # Trust Signals
    trust_real_world = models.BooleanField(default=False)
    trust_live_data = models.BooleanField(default=False)
    trust_production_ready = models.BooleanField(default=False)
    trust_hardware_integrated = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        from django.utils.text import slugify
        if not self.slug:
            self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="project_gallery/")

    def __str__(self):
        return f"Image for {self.project.title}"
