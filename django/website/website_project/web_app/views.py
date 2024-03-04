from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
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
        
def customer_record(request, pk):
    # check to see if user is logged in in order to view customer record
    if request.user.is_authenticated:
        # look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, 'You must be logged in to view that page.....')
        return redirect('home')
        
        
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, 'Record Deleted succesfully')
        return redirect('home')
    else:
        messages.success(request, 'You must be logged in to do that....')
        return redirect('home')
    
def add_record(request):
    # are they posting a form, adding a record if not just go to webpage
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid:
                add_record = form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
              
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in ...")
        return redirect('Home')
        
        
        
        
def update_record(request, pk):
    # allow to update if someobne is logged in
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been updated....")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, "You must be logged in......")
        return redirect('home')
    
        
    