from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login, logout
from django.contrib import messages
# Create your views here.

def home(request):
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
            
        return render(request, 'home.html', {})
def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out!......')
    return redirect('home')
    