from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.http import HttpResponse
# Create your views here.
def sign_up(request):
	c = {}
	c.update(csrf(request))
	return render_to_response('register.html', c)

def register(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		return HttpResponse(username + password)
	except KeyError:
		return HttpResponse("You're not supposed to be here")
	