from django import forms
from dope.settings import MAX_DIAGRAM_SLUG_LEN

class CreateDiagramForm(forms.Form):
    #def __init__(self, *args, **kwargs):
        #super(forms.Form, self).__init__(*args, **kwargs)
        
    diagram_name = forms.SlugField(max_length=MAX_DIAGRAM_SLUG_LEN)
    