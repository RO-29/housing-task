from django.http import *
from django.shortcuts import *

from functools import wraps


#User redirected to login page if not logged in , since we are storing logged in our session object when user logged in

#Wrap is not your dominos cheesy wrap ,Sigh!

def auth_check(responseauth):
    def wrap(request,*args,**kwargs):
        logged = request.session.get('logged',False)
        if logged:
            return responseauth(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login')
    wrap.__doc__ = responseauth.__doc__
    wrap.__name__ = responseauth.__name__
    return wrap

