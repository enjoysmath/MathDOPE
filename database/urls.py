from django.urls import path
from .views import save_diagram, create_diagram, load_diagram, diagram_search


urlpatterns = [
    #path('set-category', set_diagram_category, name='set_diagram_category'),    
    #path('set-model-string/<str:Model>/<str:field>', set_model_string, name='set_model_string'),
    path('save-diagram/<str:diagram_id>', save_diagram, name='save_diagram'),
    path('load-diagram/<str:diagram_id>', load_diagram, name='load_diagram'),
    path('create-diagram', create_diagram, name='create_diagram'),
    path('diagram-search/<str:diagram_id>', diagram_search, name='diagram_search'), 
    #path('load-cd/<str:diagram_id>', load_diagram_from_database, name='load_diagram'),
    #path('open-cds', list_open_diagrams, name='open_diagrams'),
    #path('all-cds', list_all_diagrams, name='all_diagrams'),
]

