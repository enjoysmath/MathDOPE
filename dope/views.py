#from .http_tools import render_to_json
#from django.template.loader import render_to_string
#from django.template import RequestContext
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages

#def ajax_error_messages(request):
    #data = {
        #'msg': render_to_string('error_messages.html', {}, RequestContext(request)),
    #}
    #return render_to_json(request, data)
    
def messages_(request):
    return render(request, 'messages.html')

def clear_messages(request):
    list(messages.get_messages(request))
    return HttpResponse('')

    #return render(request, 'consume_messages.html')