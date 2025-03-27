from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

# Create your views here.

def registration_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
        return HttpResponse(form.errors)
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form':form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/home')
        return HttpResponse(form.errors)
    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form':form})