from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

def home(request):
    records = Record.objects.all()
    # check to see if user is logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # give feedback
            messages.success(request, 'login successful')
            # redirect the user to home page
            return redirect('home')
        else:
            # if somethiing goes wrong and user cant login
            messages.success(request, 'Error logging in, try')
            return redirect('home')
        
    else:
            
        return render(request, 'home.html', {'records':records})
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out!......')
    return redirect('home')
    
def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            
            # authenticate the user and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'you have been succesfully registered')
            return redirect('home')
    else:
        # when the form has not been filled yet
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
        
    return render(request, 'register.html', {'form':form})
        
    