from django.db import models

class SiteVisit(models.Model):
    path = models.CharField(max_length=200) # e.g., /projects/ai-ml/
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True, help_text="Browser/Device info")
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.path} - {self.ip_address}"
