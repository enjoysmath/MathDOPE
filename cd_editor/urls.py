from django.urls import path
from .views import diagram_editor
#from database.views import save_diagram

urlpatterns = [
    path('<str:diagram_id>', diagram_editor, name='diagram_editor'),
]