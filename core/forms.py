from core.models import Recipe
from django import forms

class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    
    class Meta:
        model = Recipe
        fields = ('__all__')