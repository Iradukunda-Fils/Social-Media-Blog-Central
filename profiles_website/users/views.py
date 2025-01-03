from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    UserUpdateForm,
    ProfileUpdateForm,
    UserRegistrationForm
)



def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')    
            messages.success(request, f'Account created for {username}! Please login.')
            
            return redirect('blog-home')  
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {"form": form})

@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        try:
            if u_form.is_valid and  p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f"you account has been updated!")
                return redirect('profile')
        except ValueError:
            messages.error(request, f"update failed!")
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request,'users/profile.html',context)