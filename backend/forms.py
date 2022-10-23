from django import forms
from backend.models import Upload


class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['image', 'action']
