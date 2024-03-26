from django.shortcuts import render, redirect, HttpResponse
from .models import get_model_by_slug, get_unique, Diagram, Object
from django.contrib.auth.decorators import login_required, user_passes_test
#from accounts.permissions import is_editor
from dope.http_tools import get_posted_text, render_error
from django.http import JsonResponse
from dope.python_tools import full_qualname, call_with_retry
import json
from django.db import OperationalError
from django.core.exceptions import ObjectDoesNotExist
from neomodel.properties import StringProperty
from dope.settings import MAX_ATOMIC_LATEX_LENGTH, MAX_slug_LEN
from django.contrib import messages
from .forms import CreateDiagramForm
from django.utils.text import slugify
from neo4j.exceptions import ServiceUnavailable
from neomodel import db


@login_required
def create_diagram(request):
    try:
        if request.method == 'POST':
            form = CreateDiagramForm(data=request.POST)
            
            if form.is_valid():
                diagram_name = form.cleaned_data.get('diagram_name')                   
                slug = slugify(diagram_name)
                
                if 0 < len(slug) <= MAX_slug_LEN:
                    
                    diagram = Diagram.nodes.get_or_none(slug=slug, author_id=request.user.id)
                    
                    if diagram is None:
                        diagram = Diagram.our_create(slug=slug, author_id=request.user.id, name=diagram_name)
                        
                        return redirect('diagram_editor', slug)
                    else:
                        error_msg = 'A diagram by that name already exists.'                
                else:
                    if len(diagram_name) == 0:
                        error_msg = 'A diagram name must be non-empty.'
                    elif len() > MAX_slug_LEN:
                        error_msg = f'A diagram name can be no longer than {MAX_slug_LEN} characters.'
            else:
                # Form is not valid
                error_msg = 'The form submitted is not valid.'
        else:
            form = CreateDiagramForm()
            error_msg = None
            
    except ServiceUnavailable as e:
        error_msg = f'Create Diagram Erruption 🌋: The neo4j graph database is down or has connectivity issues.'
        
    except Exception as e:
        error_msg = f'{full_qualname(e)}: {e}'
        if __debug__:
            raise e
        
    if error_msg:
        messages.error(request, error_msg)
        
    return render(request, 'create_diagram.html', {'form': form})                
            

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
        
        if model.author != request.user.username:
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
        
        #if diagram.author != request.user.username:
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
def load_diagram(request, slug:str):
    try:
        if request.method == 'GET':
            username = request.user.username
            
            diagram = get_model_by_slug(Diagram, slug)
            
            if diagram.author_id != request.user.id:
                raise OperationalError(f'The diagram with name "{diagram_name}" is only editable by its original author, {username}')                
                        
            data = {
                'quiver': diagram.quiver_format(),
                'diagram_name' : diagram.name,
            }
            
            messages.success(request, "Loaded diagram from the database! ✨")
            return JsonResponse(data, safe=False)            
            
            #return render(request, 'diagram_editor.html', context)
        else:
            raise OperationalError('You can only use the GET method to load from the database.') 
                
    except Exception as e:
        #if __debug__:
            #raise e
        error_msg = f'{full_qualname(e)}: {str(e)}'
        messages.error(request, error_msg)
        
        return JsonResponse({'error_msg' : error_msg})


@login_required   
def save_diagram(request, slug):
    try:
        if request.method != 'POST': #or not request.headers.get("contentType", "application/json; charset=utf-8"):
            raise OperationalError('You can only use the POST method to save to the database.')            
        username = request.user.username
        
        diagram = get_model_by_slug(Diagram, slug)

        if diagram.author_id != request.user.id:
            raise OperationalError(f'The diagram with name "{slug}" is only editable by its original author, {username}')                
                       
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


rule_search_orders = [
    ('creator', 'Creator Name'),
    ('created', 'Date Created'),
    ('edited', 'Date Edited'),
    ('usages', 'Number of Usages'),
    ('views', 'Number of Views'),
    ('votes', 'Sum of Votes'),
    ('name', 'Rule Name'),
]

rule_search_order_map = { param: text for param,text in rule_search_orders }

@login_required
def rule_search(request, diagram_id:str):
    try:  
        ascending = request.GET.get('asc', 'true')
        order_param = request.GET.get('ord', 'name')
        one_to_one = request.GET.get('onetoone', '1')
        
        if ascending not in ('true', 'false'):
            raise ValueError(f'Invalid order direction parameter (asc) value: {ascending}')
        
        if one_to_one not in ('0', '1'):
            raise ValueError(f'Invalid one-to-one parameter (onetoone) value: {one_to_one}')
        
        if order_param not in rule_search_order_map:
            raise ValueError(order_param + " is not a valid value to order by.")        
        
        # Starting from longest paths first should shorten the final search query (not this one)        
        paths_by_length = Diagram.get_paths_by_length(diagram_id)          
        nodes, rels, search_query = Diagram.build_query_from_paths(paths_by_length)
                        
        rules = []
        
        if search_query:
            regexes, search_query = Diagram.build_match_query(search_query, nodes, rels)
            search_query += "RETURN n0"  # We only need n0 to get a diagram id at this stage of the app UX
            
            results, meta = db.cypher_query(search_query)
            
            rule_memo = {
                # To weed out duplicated results, keyed by rule.uid
            }
            
            for result in results:
                n0 = Object.inflate(result[0])
                
                diagram_results, meta = db.cypher_query(
                    f"MATCH (D:Diagram)-[:CONTAINS]->(X:Object) WHERE X.uid = '{n0.uid}' RETURN D.uid")
                
                if diagram_results and diagram_results[0]:
                    result_diagram_id = diagram_results[0][0]
                    rules_query = \
                        f"MATCH (R:DiagramRule)-[:KEY_DIAGRAM]->(D:Diagram) " + \
                        f"WHERE D.uid = '{result_diagram_id}' RETURN R" 
                    
                    #HERE'S WHERE WE INSERT ORDERING CODE also key / result search^^
                    
                    results, meta = db.cypher_query(rules_query)                
                    
                    for rule in results:
                        rule = DiagramRule.inflate(rule[0])
                        
                        key_diagram = rule.key_diagram.single()
                        if rule.uid not in rule_memo:
                            if one_to_one == '1':
                                if len(key_diagram.objects) != len(nodes) or key_diagram.morphism_count() != len(rels):
                                    continue                        

                            rule_memo[rule.uid] = rule
                            rules.append(rule)                           
        
        order_text = rule_search_order_map[order_param]
        
        context = {
            'diagram_id' : diagram_id,
            'order_param' : order_param,
            'order_text' : order_text,
            'orders' : rule_search_orders,
            'rules' : rules,
            'ascending' : ascending,
            'one_to_one' : one_to_one,
        }
        
        return render(request, 'rule_search.html', context)
        
    except Exception as e:
        if DEBUG:
            raise e
        return redirect('error', f'{full_qualname(e)}: {str(e)}')        