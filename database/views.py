from django.shortcuts import render, redirect, HttpResponse
from .models import get_model_by_name, get_unique, Diagram
from django.contrib.auth.decorators import login_required, user_passes_test
#from accounts.permissions import is_editor
from dope.http_tools import get_posted_text, render_error
from django.http import JsonResponse
from dope.python_tools import full_qualname, call_with_retry
import json
from django.db import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from neomodel.properties import StringProperty
from dope.settings import MAX_ATOMIC_LATEX_LENGTH
from django.contrib import messages


@login_required
def create_diagram(request):
    try:
        if request.method == 'POST':
            #namespace = request.user.username
            diagram_name = request.POST.get('diagram-name-input')
        
            #diagram_name = DrawnDiagram.validate_name(diagram_name)
        
            if 0 < len(diagram_name) <= MAX_ATOMIC_LATEX_LENGTH:               
                diagram = call_with_retry(Diagram.nodes.get_or_none, name=diagram_name)
                
                if diagram is None:
                    diagram = Diagram.our_create(
                        name=diagram_name, checked_out_by=request.user.username)
                    
                    return redirect('diagram_editor', diagram_name)
                else:
                    error_msg = 'A diagram by that name already exists.'                
            else:
                if len(diagram_name) == 0:
                    error_msg = 'A diagram name must be non-empty.'
                elif len(diagram_name) > MAX_ATOMIC_LATEX_LENGTH:
                    error_msg = f'A diagram name can be no longer than {MAX_ATOMIC_LATEX_LENGTH} characters.'                
        else:
            error_msg = None
            
    except Exception as e:
        if __debug__:
            raise e
        
    if error_msg:
        messages.error(request, error_msg)
        
    return render(request, 'create_diagram.html')                
            

#def get_model_by_uid(Model, uid:str):
    #if len(uid) > 36:
        #raise ValueError('That id is longer than a UUID4 is supposed to be.')
    
    #if isinstance(Model, str):
        #Model = get_model_class(Model)
        
    #model = Model.nodes.get_or_none(uid=uid)    
    
    #if model is None:
        #raise ObjectDoesNotExist(f'An instance of the model {Model} with uid "{uid}" does not exist.')
    
    #return model
                        

@login_required   
#@user_passes_test(is_editor)
def set_model_string(request, Model:str, field:str):
    try:                        
        old_id = request.POST['pk']
        
        ModelClass = get_model_class(Model)         
        model = get_model_by_uid(ModelClass, uid=old_id)
        
        if model.checked_out_by != request.user.username:
            raise OperationalError(f'The {Model} is not checked out by you.')
        
        if not hasattr(model, field):
            raise ValueError(f'A {Model} has no field "{field}" implemented.')
        
        string = get_posted_text(request)        
        string = string.strip()
        
        if string == '':
            raise Exception(f'Name cannot be empty.')       
    
        current_val = getattr(model, field)
        
        if current_val != string:
            setattr(model, field, string)
            model.save()
            
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({'success': False, 'error_msg': f'{full_qualname(e)}: {e}'}) 



#@login_required   
##@user_passes_test(is_editor)
#def set_diagram_category(request):
    #try:                        
        #diagram = get_model_by_uid(Diagram, uid=request.POST['pk'])
        
        #if diagram.checked_out_by != request.user.username:
            #raise OperationalError(f'The {Model} is not checked out by you.')
               
        #category_name = get_posted_text(request).strip()
        
        #if category_name == '':
            #raise Exception(f'Category name cannot be empty.')       
    
        #category = diagram.category.single()
    
        #if category_name != category.name:
            #new_category = get_unique(Category, name=category_name)
            #diagram.category.reconnect(category, new_category)
            #diagram.save()
            
        #return JsonResponse({'success': True})
        
    #except Exception as e:
        #return JsonResponse({'success': False, 'error_msg': f'{full_qualname(e)}: {e}'})
    
    
    
@login_required
def list_open_diagrams(request):
    
    try:          
        diagrams = []
        diagram_ids = request.session.get('diagram ids', [])
        
        for diagram_id in diagram_ids:
            diagram = get_model_by_uid(Diagram, uid=diagram_id)
            diagrams.append(diagram)
            
        context = {
            'diagrams' : diagrams
        }
            
        return render(request, 'diagram_list_page.html', context)
    except Exception as e:
        return redirect('error', full_qualname(e) + ': ' + str(e))
    
    
def list_all_diagrams(request):
    try:
        context = {
            'diagrams' : Diagram.nodes.order_by('name')
        }        
         
        return render(request, 'diagram_list_page.html', context) 
            
    except Exception as e:
        return redirect('error', f'{full_qualname(e)}: {str(e)}')
        
        
@login_required
def load_diagram(request, diagram_name:str):
    try:
        if request.method == 'GET':
            user = request.user.username
            
            diagram = get_model_by_name(Diagram, diagram_name)
            
            if diagram.checked_out_by != user:
                raise OperationalError(
                    f'The diagram with name "{diagram_name}" is already checked out by {diagram.checked_out_by}')                
                        
            data = diagram.quiver_format()
            
            messages.success(request, "Loaded diagram from the database! ✨")
            return JsonResponse(data, safe=False)            
            
            #return render(request, 'diagram_editor.html', context)
        else:
            raise OperationalError('You can only use the GET method to load from the database.') 
                
    except Exception as e:
        if __debug__:
            raise e
        error_msg = f'{full_qualname(e)}: {str(e)}'
        messages.error(request, error_msg)
        return JsonResponse({'error_msg' : error_msg})


@login_required   
def save_diagram(request, diagram_name):
    try:
        if request.method != 'POST': #or not request.headers.get("contentType", "application/json; charset=utf-8"):
            raise OperationalError('You can only use the POST method to save to the database.')            
        user = request.user.username
        
        diagram = get_model_by_name(Diagram, diagram_name)

        if diagram.checked_out_by != user:
            raise OperationalError(
                f'The diagram with name "{diagram_name}" is already checked out by {diagram.checked_out_by}')                
                       
        body = request.body.decode('utf-8')
        
        if body:
            try:
                data = json.loads(body)                
            except json.decoder.JSONDecodeError:
                # For some reason, empty diagrams are resulting in the body as a URL str (not JSON)
                data = [0, 0]               
        else:
            data = [0, 0]
        
        diagram.delete_objects()
        diagram.load_from_editor(data)        

        messages.success(request, "Saved diagram to the database! 🤩")
        
        return JsonResponse(
            'Wrote the following data to the database:\n' + str(data), safe=False)

    except Exception as e:
        if __debug__:
            raise e
        error_msg = f'{full_qualname(e)}: {str(e)}'
        messages.error(request, error_msg)
        return JsonResponse({'error_msg' : error_msg})
    
    #except Exception as e:
        #return JsonResponse({'success': False, 'error_msg': f'{full_qualname(e)}: {e}'}) 

