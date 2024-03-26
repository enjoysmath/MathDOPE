from django import forms
from dope.settings import MAX_DIAGRAM_NAME_LEN

class CreateDiagramForm(forms.Form):       
    diagram_name = forms.CharField(max_length=MAX_DIAGRAM_NAME_LEN, min_length=1, strip=True)
    
    
class DiagramSearchForm(forms.Form):
    pass
    