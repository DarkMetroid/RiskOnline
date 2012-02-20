from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext

def homepage(request): 
	rc = RequestContext(request, {'STATIC_URL' : '/statics/',})
	return render_to_response('login.html', rc)