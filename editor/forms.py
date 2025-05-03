from django import forms
from .models import Path, Background

class BackgroundChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name  # Optional: cleaner name if needed

class PathForm(forms.ModelForm):
    background = BackgroundChoiceField(
        queryset=Background.objects.all(),
        widget=forms.RadioSelect
    )

    class Meta:
        model = Path
        fields = ['name', 'background']