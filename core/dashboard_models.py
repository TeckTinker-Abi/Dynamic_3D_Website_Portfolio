from django.db import models
from django.core.exceptions import ValidationError

class GlobalSetting(models.Model):
    key = models.CharField(max_length=50, unique=True, help_text="Unique key for the setting (e.g., 'theme_color')")
    value = models.TextField(help_text="Value of the setting")
    description = models.CharField(max_length=255, blank=True, help_text="Description of what this setting controls")
    is_public = models.BooleanField(default=True, help_text="If false, this setting is for internal/admin use only")

    def __str__(self):
        return f"{self.key}: {self.value}"

class IdentityCore(models.Model):
    """Singleton model for the top-left dashboard section."""
    full_name = models.CharField(max_length=120)
    degree = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. B.Tech in Computer Science")
    profile_title = models.CharField(max_length=150)
    slogan = models.CharField(max_length=250)
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    enable_avatar_mode = models.BooleanField(default=False)
    explore_cta_text = models.CharField(max_length=50, blank=True, null=True, help_text="Text for the main CTA button")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Identity Core (Singleton)"

    def clean(self):
        if not self.pk and IdentityCore.objects.exists():
            raise ValidationError("Only one Identity Core record allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Identity: {self.full_name}"

class LiveSystem(models.Model):
    """Singleton model for the currently active system build."""
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    highlight_tag = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 'v2.0 Beta'")

    class Meta:
        verbose_name_plural = "Live System (Singleton)"

    def clean(self):
        if not self.pk and LiveSystem.objects.exists():
            raise ValidationError("Only one Live System record allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CapabilitySignal(models.Model):
    STRENGTH_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    title = models.CharField(max_length=100)
    strength_level = models.CharField(max_length=10, choices=STRENGTH_CHOICES, default='Medium')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.title} ({self.strength_level})"

class ImpactMetric(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

class CurrentFocus(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Current Focus Items"
        ordering = ['display_order']

    def __str__(self):
        return self.title
