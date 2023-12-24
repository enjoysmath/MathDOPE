from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile

#def sign_up(request):
    #if request.method == 'POST':
        #form = UserCreationForm(request.POST)
        #if form.is_valid():
            #form.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            #return redirect('user_home')
    #else:
        #form = UserCreationForm()
    #return render(request, 'sign_up.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('user_home')
    else:
        form = LoginForm()
    return render(request, 'sign_in.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')

@login_required
def user_home(request):
    return render(request, 'user_home.html')
        
        
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()            
            # Create the user profile:
            Profile.objects.create(user=new_user)
            #return render(request, 'accounts/register_done.html', {'new_user': new_user})
            return redirect('user_home')
        
    else:
        user_form = UserRegistrationForm()
        
    return render(request, 'sign_up.html', {'form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():            
            user_form.save()
            profile_form.save()
            
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})