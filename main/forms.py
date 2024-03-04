from django import forms
from .models import *

class urlToGdrive_form(forms.ModelForm):
    filename = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,)
    fileid = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,)
    folderid = forms.CharField(max_length=50,
                               widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,)
    shared = forms.BooleanField(required=False)
    local_path = forms.CharField(max_length=500,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}),required=False,
                                 error_messages={'required': 'Please enter URL'},)

    class Meta:
        model = UrlToGdrive
        fields = ['filename']  