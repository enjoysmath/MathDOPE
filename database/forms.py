from django.forms import Form, TextInput

class CreateDiagramForm(Form):
    def __init__(self, *args, **kwargs):
        super(Form, self).__init__(*args, **kwargs)
        
    diagram_name = TextInput()
    