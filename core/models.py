from django.db import models
from django.core.exceptions import ValidationError

class Profile(models.Model):
    # 1. Identity Core
    full_name = models.CharField(max_length=100, default="Abishek M")
    title = models.CharField(max_length=200, help_text="e.g., Intelligent Systems & GenAI Engineer")
    philosophy = models.CharField(max_length=300, default="Designing systems where intelligence meets the physical world.", help_text="Engineering Philosophy Line")
    
    # Bio (Keep for other pages)
    bio = models.TextField(help_text="Short bio", blank=True)
    detailed_bio = models.TextField(help_text="Longer bio", blank=True)
    
    # 5. Live System
    current_building = models.CharField(max_length=200, help_text="e.g. LLM-driven intelligent automation system", blank=True)
    
    # 7. Current Focus (Store as new-line separated text)
    focus_areas = models.TextField(help_text="GenAI architectures, LLM orchestration... (one per line)", blank=True)
    
    # Visuals
    profile_picture = models.ImageField(upload_to="profile/", blank=True, null=True)
    logo = models.ImageField(upload_to="profile/", blank=True, null=True)
    
    # Resume
    resume = models.FileField(upload_to="resume/", help_text="Upload updated PDF resume")
    
    # Social Links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValidationError('There is already an existing Profile instance')
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Command Center Profile"
        verbose_name_plural = "Command Center Profile"

class GlobalConfiguration(models.Model):
    # 3D Settings
    enable_3d = models.BooleanField(default=True, help_text="Toggle System Universe 3D visualization")
    animation_speed = models.FloatField(default=1.0, help_text="Speed multiplier (0.5 - 2.0)")
    max_nodes_limit = models.IntegerField(default=8, help_text="Max nodes to display in 3D view")

    # Theme Settings
    primary_color = models.CharField(max_length=7, default="#00E5FF", help_text="Main accent color (Hex)")
    accent_color = models.CharField(max_length=7, default="#7C3AED", help_text="Secondary accent color (Hex)")
    background_style = models.CharField(max_length=50, default="dark", choices=[('dark', 'Dark'), ('gradient', 'Gradient'), ('minimal', 'Minimal')])

    # Contact Settings
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    # Resume
    resume_file = models.FileField(upload_to="resume/", blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Global Configuration"
        verbose_name_plural = "Global Configuration (Singleton)"

    def clean(self):
        # Validate node limit
        if self.max_nodes_limit > 10:
            raise ValidationError({'max_nodes_limit': 'Max nodes limit cannot exceed 10.'})
        
        # Validate animation speed
        if not (0.5 <= self.animation_speed <= 2.0):
            raise ValidationError({'animation_speed': 'Animation speed must be between 0.5 and 2.0.'})

    def save(self, *args, **kwargs):
        if not self.pk and GlobalConfiguration.objects.exists():
            raise ValidationError("Only one Global Configuration allowed.")
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return "Global System Configuration"
