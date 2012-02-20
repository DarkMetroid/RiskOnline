from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.template import RequestContext
from django.utils import simplejson

# Create your views here.
def user(request, id):
	return HttpResponse("Under Construction")
	
def riskmap(request, id):
	return HttpResponse("Under Construction")

def game(request, id):
	if request.GET.has_key('gp'):
		response_dict = {'A':(100,0,3), 'B':(100,200,5)}
	else:
		rc = RequestContext(request, locals())
		return render_to_response('game.html', rc)
	return HttpResponse(simplejson.dumps(response_dict), content_type = 'application/javascript; charset=utf8')