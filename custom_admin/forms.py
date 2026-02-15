from django import forms
from core.models import GlobalConfiguration, Profile
from core.system_models import SystemNode, SystemConnection
from projects.models import Project, Category, Technology, TechnologyCategory

class TechnologyCategoryForm(forms.ModelForm):
    class Meta:
        model = TechnologyCategory
        fields = '__all__'
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'w-5 h-5'}),
        }

class TechnologyForm(forms.ModelForm):
    class Meta:
        model = Technology
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'w-full h-10 p-1 bg-transparent border border-white/20 rounded'}),
            'proficiency_level': forms.Select(attrs={'class': 'bg-black/20 border border-white/10 text-white rounded px-3 py-2 w-full'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'w-5 h-5'}),
        }
from core.dashboard_models import ImpactMetric, CapabilitySignal, CurrentFocus, GlobalSetting, IdentityCore, LiveSystem

class GlobalConfigurationForm(forms.ModelForm):
    class Meta:
        model = GlobalConfiguration
        fields = '__all__'
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-full h-10 p-1 bg-transparent border border-white/20 rounded'}),
            'accent_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-full h-10 p-1 bg-transparent border border-white/20 rounded'}),
            'animation_speed': forms.NumberInput(attrs={'step': 0.1, 'min': 0.5, 'max': 2.0, 'class': 'bg-black/20 border border-white/10 text-white rounded px-3 py-2 w-full'}),
            'max_nodes_limit': forms.NumberInput(attrs={'min': 1, 'max': 10, 'class': 'bg-black/20 border border-white/10 text-white rounded px-3 py-2 w-full'}),
            'background_style': forms.Select(attrs={'class': 'bg-black/20 border border-white/10 text-white rounded px-3 py-2 w-full'}),
            'github_url': forms.URLInput(attrs={'class': 'bg-black/20 border border-white/10 text-white rounded px-3 py-2 w-full', 'placeholder': 'https://github.com/...'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'bg-black/20 border border-white/10 text-white rounded px-3 py-2 w-full', 'placeholder': 'https://linkedin.com/...'}),
            'email': forms.EmailInput(attrs={'class': 'bg-black/20 border border-white/10 text-white rounded px-3 py-2 w-full', 'placeholder': 'me@example.com'}),
        }

class GlobalSettingForm(forms.ModelForm):
    class Meta:
        model = GlobalSetting
        fields = '__all__'
        widgets = {
            'value': forms.Textarea(attrs={'rows': 3}),
        }

class IdentityCoreForm(forms.ModelForm):
    class Meta:
        model = IdentityCore
        fields = '__all__'
        widgets = {
            'slogan': forms.Textarea(attrs={'rows': 2}),
        }

class LiveSystemForm(forms.ModelForm):
    class Meta:
        model = LiveSystem
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SystemNodeForm(forms.ModelForm):
    class Meta:
        model = SystemNode
        fields = '__all__'
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SystemConnectionForm(forms.ModelForm):
    class Meta:
        model = SystemConnection
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
            'scope_statement': forms.Textarea(attrs={'rows': 3}),
        }

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'short_description': forms.Textarea(attrs={'rows': 2}),
            'tech_stack': forms.Textarea(attrs={'rows': 2, 'placeholder': '["Python", "Django", "React"]'}),
            'github_link': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'live_link': forms.URLInput(attrs={'placeholder': 'https://...'}),
        }

class ImpactMetricForm(forms.ModelForm):
    class Meta:
        model = ImpactMetric
        fields = '__all__'

class CapabilitySignalForm(forms.ModelForm):
    class Meta:
        model = CapabilitySignal
        fields = '__all__'

class CurrentFocusForm(forms.ModelForm):
    class Meta:
        model = CurrentFocus
        fields = '__all__'






