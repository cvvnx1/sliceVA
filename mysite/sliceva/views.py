from hashlib import md5
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import get_template
from django.template import Context
from sliceva.models import Device, User
from sliceva.modelform import DeviceForm, UserForm
from sliceva.auth import auth_match, admin_match
from sliceva.worker import Assignment
from sliceva.scan import alive, search_config, run_config, show_running

def listdevice(request):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    username = request.COOKIES["user"]
    password = User.objects.filter(username=username)[0].password
    list = Device.objects.all().extra(order_by = ['host'])
    hosts = []
    for device in list:
         hosts.append(device.host)
#    work = alive()
#    result = Assignment(work, username, password, hosts, 20)
    for device in list:
#        device.status = result[device.host]
        device.status = False
    return render_to_response('listdevice.html', {'list': list})

def listuser(request):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    if admin_match(request):
        return HttpResponseRedirect(reverse(listdevice))
    list = User.objects.all()
    return render_to_response('listuser.html', {'list': list})

def adduser(request):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    if admin_match(request):
        return HttpResponseRedirect(reverse(listdevice))
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(listuser))
        else:
            return render_to_response('adduser.html', {'form': form})
    return render_to_response('adduser.html', {'form': UserForm()})

def updateuser(request, id):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    if admin_match(request):
        return HttpResponseRedirect(reverse(listdevice))
    user = get_object_or_404(User, pk=int(id))
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(listuser))
    return render_to_response('adduser.html', {'form': UserForm(instance=user)})

def deleteuser(request, id):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    if admin_match(request):
        return HttpResponseRedirect(reverse(listdevice))
    user = get_object_or_404(User, pk=int(id))
    user.delete()
    return HttpResponseRedirect(reverse(listuser))

def adddevice(request):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(listdevice))
        else:
            return render_to_response('adddevice.html', {'form': form})
    return render_to_response('adddevice.html', {'form': DeviceForm()})

def updatedevice(request, id):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    device = get_object_or_404(Device, pk=int(id))
    if request.method == "POST":
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(listdevice))
    return render_to_response('adddevice.html', {'form': DeviceForm(instance=device)})

def deletedevice(request, id):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    device = get_object_or_404(Device, pk=int(id))
    device.delete()
    return HttpResponseRedirect(reverse(listdevice))

def device(request, id):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    device = get_object_or_404(Device, pk=int(id))
    username = request.COOKIES["user"]
    password = User.objects.filter(username=username)[0].password
    status_bar = []
    if 'submitcode' in request.POST:
        code = request.POST.get('submitcode').replace('\r', '').split('\n')
        commands = [x for x in code if x != '']
        work = run_config(commands)
        result = work.run(hostname=device.host, username=username, password=password)
        if result:
            status_bar = ['Commands sent...']
        else:
            status_bar = ['Commands sent failed...']
    if 'checkcode' in request.POST:
        code = request.POST.get('checkcode').replace('\r', '').split('\n')
        commands = [x for x in code if x != '']
        work = search_config(commands)
        result = work.run(hostname=device.host, username=username, password=password)
        if result:
            status_bar = ['Config matched...']
        else:
            status_bar = ['Config not matched...']
    work = show_running()
    running_config = work.run(hostname=device.host, username=username, password=password)
    if not running_config:
        running_config = []
        status_bar = "Host %s can not connect..." % device.host
    return render_to_response('device.html', {'running_config': running_config, 'status_bar': status_bar})

def scan(request):
    if auth_match(request):
        return HttpResponseRedirect(reverse(login))
    username = request.COOKIES["user"]
    password = User.objects.filter(username=username)[0].password
    list = Device.objects.all()
    hosts = []
    for device in list:
        device.status = False
        hosts.append(device.host)
    if 'submitcode' in request.POST:
        code = request.POST.get('submitcode').replace('\r', '').split('\n')
        commands = [x for x in code if x != '']
        work = run_config(commands)
        result = Assignment(work, username, password, hosts, 20)
        for device in list:
            device.status = result[device.host]
    if 'checkcode' in request.POST:
        code = request.POST.get('checkcode').replace('\r', '').split('\n')
        commands = [x for x in code if x != '']
        work = search_config(commands)
        result = Assignment(work, username, password, hosts, 20)
        for device in list:
            device.status = result[device.host]
    return render_to_response('scan.html', {'list': list})

def login(request):
    if request.method == "POST":
        login = get_object_or_404(User, username=request.POST.get('username'))
        if login.password == request.POST.get('password'):
            if login.admin:
                response = HttpResponse(get_template('auth.html').render(Context({'redirect': reverse(listuser)})))
            else:
                response = HttpResponse(get_template('auth.html').render(Context({'redirect': reverse(listdevice)})))
# getting ip can be a function
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            response.set_cookie("user", login.username)
            response.set_cookie("dna", md5(login.username + login.password + ip).hexdigest())
            return response
        else:
            return HttpResponseRedirect(reverse(login))
    else:
        return render_to_response('login.html', {'form': UserForm()})

def logout(request):
    response = HttpResponse(get_template('auth.html').render(Context({'redirect': reverse(login)})))
    response.delete_cookie("user")
    response.delete_cookie("dna")
    return response

