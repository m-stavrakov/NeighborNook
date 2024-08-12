from django import forms
from django.forms import modelformset_factory
from .models import Event, EventImage
from .widgets import MultipleFileInput

INPUT_CLASS = 'auth_inputs'

class NewEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'name',
            'overview',
            'description', 
            'location', 
            'date', 
            'time', 
            'category', 
            'age_limit', 
            'weather', 
            'what_to_bring')
        
        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'overview': forms.Textarea(attrs={'class': INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASS}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': INPUT_CLASS, 'type': 'time'}),
            'category': forms.Select(attrs={'class': INPUT_CLASS}),
            'age_limit': forms.Select(attrs={'class': 'form-control'}),
            'weather': forms.Select(attrs={'class': 'form-control'}),
            'what_to_bring': forms.Textarea(attrs={'class': INPUT_CLASS}),
        }

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class EventImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ('image',)
        widgets = {
            'image': MultipleFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

EventImageFormSet = modelformset_factory(EventImage, form=EventImageForm, extra=0, can_delete=True)

class EditImageForm(forms.ModelForm):
    class Meta:
        model = EventImage
        fields = ('image',)
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False

ImageEditFormSet = modelformset_factory(EventImage, form=EditImageForm, extra=0, can_delete=True)

class EditEventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = (
            'name', 
            'overview',
            'description', 
            'location', 
            'date', 
            'time', 
            'category', 
            'age_limit', 
            'weather', 
            'what_to_bring')

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'overview': forms.Textarea(attrs={'class': INPUT_CLASS}),
            'description': forms.Textarea(attrs={'class': INPUT_CLASS}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'date': forms.DateInput(attrs={'class': INPUT_CLASS, 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': INPUT_CLASS, 'type': 'time'}),
            'category': forms.Select(attrs={'class': INPUT_CLASS}),
            'age_limit': forms.Select(attrs={'class': 'form-control'}),
            'weather': forms.Select(attrs={'class': 'form-control'}),
            'what_to_bring': forms.Textarea(attrs={'class': INPUT_CLASS}),
        }