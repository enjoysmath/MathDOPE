from .settings import MAX_TEXT_LENGTH
from django.shortcuts import render, HttpResponse
from django.contrib import messages
from dope.python_tools import full_qualname
import json


def render_error(request, error_msg=None, excep=None):
    if error_msg is None:
        error_msg = ''
    
    if excep is not None:
        if __debug__:
            raise excep 
        
        error_msg += '\n'
        error_msg += f'{full_qualname(e)}: {str(e)}'
    
    messages.error(request, error_msg)
    
    return render(request, 'error_page.html', {'error_msg': error_msg})


def get_posted_text(request, key=None, max_len=None): # TODO:  max_len=MAX_TEXT_LENGTH):
    if request.method != 'POST':
        raise Exception('This setting requires you to use the POST method.')
    
    if key is None:
        key = 'value'
        
    if not key in request.POST:
        raise KeyError('Error, missing POST parameter(s).')
    
    text = request.POST[key]
    text = text.strip()
    
    if len(text) > max_len:
        raise ValueError(f'The text exceeded max length {max_len}')
    
    return text


def get_url_text(request, text, max_len=MAX_TEXT_LENGTH):
    if request.method != 'GET':
        raise Exception('This page requires you to use the GET method.')
    
    if len(text) > max_len:
        raise ValueError(f'The text exceeded max length {max_len}')
    
    return text    
        
        
def get_model_id(request, edit_mode):   
    if edit_mode not in request.session:
        raise Exception(f'You are not currently in {edit_mode} edit mode.')
    
    # The edit item's id is kept in the session which is private.
    # The client doesn't see the id.  This all works as long as
    # only one editor is allowed open at any one time.
    edit_id = request.session[edit_mode]
    
    return edit_id


# `data` is a python dictionary
def render_to_json(request, data):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False),
        mimetype=request.is_ajax() and "application/json" or "text/html")