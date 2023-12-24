from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dope.http_tools import render_error

@login_required
def diagram_editor(request, slug:str):
    try:        
        context = {
            'slug': slug,
        }
        return render(request, 'diagram_editor.html', context)
    
    except Exception as e:
        return render_error(request, excep=e)


#@login_required
#def create_new_diagram(request):
    #diagram = Diagram.our_create(name='', author=request.user.username)
    #session = request.session
    
    #if 'diagram ids' not in session:
        #session['diagram ids'] = [diagram.uid]
    #else:
        #if diagram.uid not in session['diagram ids']:
            #session['diagram ids'].append(diagram.uid)
            #session.save()

    #diagrams = []
    
    ##for diagram_id in session['diagram ids']:
        ##diagram = get_model_by_uid(Diagram, uid=diagram_id)
        ##diagrams.append(diagram)
        
    #context={
        #'diagram_id': diagram.uid,
        #'diagrams' : diagrams,
    #} 
                
    #return render(request, 'create_diagram.html', context)