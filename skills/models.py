from django.db import models

class Skill(models.Model):
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField()  # 1-100
    category = models.CharField(max_length=100, help_text="e.g. Frontend, Backend, AI")
    icon = models.ImageField(upload_to="skills/", blank=True, null=True)

    def __str__(self):
        return self.name
