# 🛡️ ADMIN PANEL STRATEGY & MANAGEMENT
**Platform:** Django Admin (Customized)  
**Purpose:** Centralized Control Center for Portfolio Content, Personal Details, and Analytics.

---

## 1️⃣ OVERVIEW
Use Django Admin to completely manage the content of the portfolio. No hardcoding of text or personal details in templates.

**Core Upgrade:**
- Custom Admin Dashboard Styling (using `django-jazzmin` or custom CSS).
- Rich Text Editors for descriptions (CKEditor).

---

## 2️⃣ CONTENT MANAGEMENT (EXISTING MODELS)
Manage these standard models via Admin:
- **Categories:** Create/Edit project categories.
- **Projects:** Full CRUD for projects, including uploading architecture diagrams, choosing categories, and setting featured status.
- **Skills:** Add new skills, adjust proficiency scores (1-100), and assign categories.
- **Experience:** Update work history timelines.
- **Contact Messages:** View incoming messages from the contact form.

---

## 3️⃣ PERSONAL DETAILS MANAGEMENT
Instead of hardcoding the name, bio, and social links in HTML, we will create a `Profile` model (Singleton).

### 👤 Profile Model
```python
class Profile(models.Model):
    # Basic Info
    full_name = models.CharField(max_length=100, default="Abishek M")
    title = models.CharField(max_length=200, help_text="e.g., AI Engineer | ML Architect")
    bio = models.TextField(help_text="Short bio for hero section")
    detailed_bio = models.TextField(help_text="Longer bio for about section")
    
    # Visuals
    profile_picture = models.ImageField(upload_to="profile/", blank=True, null=True)
    logo = models.ImageField(upload_to="profile/", blank=True, null=True, help_text="Site logo")
    
    # Resume
    resume = models.FileField(upload_to="resume/", help_text="Upload updated PDF resume")
    
    # Social Links
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and Profile.objects.exists():
            raise ValidationError('There is already an existing Profile instance')
        return super(Profile, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Personal Profile"
        verbose_name_plural = "Personal Profile"
```
**Admin Usage:** You will see a "Personal Profile" section. You can edit your bio, upload a new resume, or change social links instantly without touching code.

---

## 4️⃣ VISITOR ANALYTICS
We need to track how many users visit the portfolio and show this data in the Admin Panel.

### 📊 Analytics Model
```python
class SiteVisit(models.Model):
    path = models.CharField(max_length=200) # e.g., /projects/ai-ml/
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True, help_text="Browser/Device info")
    
    class Meta:
        ordering = ['-timestamp']
```

### 📈 Middleware Implementation
Create a middleware `middleware.py` to automatically track visits:
1. Check if user is Admin (ignore admin visits).
2. Log IP, Path, and Timestamp to `SiteVisit` model.

### 🖥️ Admin Dashboard View
In the Admin Panel index, we can display:
- **Total Visits:** Count of all `SiteVisit` records.
- **Unique Visitors:** Count of unique IPs.
- **Top Pages:** Aggregation of most visited paths.

---

## 5️⃣ SUMMARY OF ADMIN FEATURES
| Feature | Type | Admin Control |
| :--- | :--- | :--- |
| **Projects** | Dynamic Content | ✅ Create / Edit / Delete |
| **Skills** | Dynamic Graphs | ✅ Update Proficiency / Icons |
| **Profile** | Personal Data | ✅ Update Bio / Regex / Links |
| **Resume** | File Upload | ✅ Upload new PDF instantly |
| **Analytics** | Data Tracking | ✅ View User Visit Counts |
