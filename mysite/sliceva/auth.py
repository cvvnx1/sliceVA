from hashlib import md5
from django.shortcuts import get_object_or_404
from sliceva.models import User

def auth_match(request):
    if "user" in request.COOKIES:
        login = get_object_or_404(User, username=request.COOKIES["user"])
# getting ip can be a function
        if request.META.has_key('HTTP_X_FORWARDED_FOR'):
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        if request.COOKIES["dna"] == md5(request.COOKIES["user"] + login.password + ip).hexdigest():
            # return False for if condition,
            # if auth_match(request):
            #     HttpResponseRedirect("somewhere")
            return False
        else:
            return True
    else:
        return True

def admin_match(request):
    if "user" in request.COOKIES:
        login = get_object_or_404(User, username=request.COOKIES["user"])
        if login.admin:
            return False
        else:
            return True
    else:
        return True
