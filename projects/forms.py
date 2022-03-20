from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }
    # format form fields
    def __init__(self, *args, **kwargs):
        # override super
        super(ProjectForm, self).__init__(*args, **kwargs)
        # apply class 'input' to each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # OR SET EACH FIELD INDIVIDUALLY LIKE BELOW:
        # self.fields['title'].widget.attrs.update({'class': 'input'})
        # self.fields['description'].widget.attrs.update({'class': 'input'})