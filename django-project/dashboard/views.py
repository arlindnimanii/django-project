from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from .models import Log
import datetime

@login_required(login_url='/auth/login')
def dashboard(request):
    if request.user.groups.filter(name='employee').exists():
        logs = Log.objects.filter(user__id=request.user.id).order_by('-id')[:10:1]
        context = {'logs' : logs}
    if request.user.groups.filter(name='employer').exists():
        employees = User.objects.all().order_by('-id')
        context = {'employees' : employees}

    return render(request, 'dashboard.html', context)

@login_required(login_url='/auth/login')
@permission_required("dashboard.add_log", raise_exception=True)
def checkin(request):
    if request.method == 'POST':
        date = request.POST['date']
        dstime = request.POST['dstime']
        notes = request.POST['notes']
        Log(user_id=request.user.id, date=date, dstime=dstime, notes=notes).save()
        return redirect('dashboard')

@login_required(login_url='/auth/login')
@permission_required("dashboard.change_log", raise_exception=True)
def checkout(request):
    detime = datetime.datetime.now().strftime('%H:%M:%S')
    log = Log.objects.filter(user__id=request.user.id).last()
    log.detime = detime
    log.save()
    return redirect('dashboard')

@login_required(login_url='/auth/login')
@permission_required("dashboard.change_log", raise_exception=True)
def lunchbreak(request):
    if request.method == 'POST':
        pstime = request.POST['pstime']
        petime = request.POST['petime']
        log = Log.objects.filter(user__id=request.user.id).last()
        log.pstime = pstime
        log.petime = petime
        log.save()
        return redirect('dashboard')

@login_required(login_url='/auth/login')
def employeelog(request, id: int):
    logs = Log.objects.filter(user__id=id).order_by('-id')
    return render(request, 'log.html', {'logs' : logs})

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    context = {
        'form' : UserCreationForm()
    }
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            employee = Group.objects.get(name='employee')
            employee.user_set.add(user)
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/register.html', {'form' : form})
        
    return render(request, 'registration/register.html', context)

def signout(request):
    logout(request)
    return redirect('auth/login')