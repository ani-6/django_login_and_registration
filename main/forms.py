from django import forms
from .models import *

class urlToGdrive_form(forms.ModelForm):
    file_name = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,)
    file_id = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,)
    folder_id = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,)
    shared = forms.BooleanField(required=False)
    source_path = forms.CharField(max_length=500,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,
                                 error_messages={'required': 'Please enter URL'},)

    class Meta:
        model = UrlToGdrive
        fields = ['file_name']  