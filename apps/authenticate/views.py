from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from apps.authenticate.forms import SignUpForm, EditProfileForm


def login_user(request):
    if(request.method=='POST'):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request,'Voce está logado no sistema!')
            nxt = request.GET.get("next", None)
            if not nxt is None:
                return redirect(request.GET['next'])
            else:
                return redirect('home')

        else:
            messages.success(request,'Falha na autenticação, tente novamente...')
            return redirect(reverse("login_user"))
    else:
        return render(request, 'authenticate/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request,'Logout realizado com sucesso!')
    return redirect ('home')

def register_user(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request,user)
            messages.success(request,'Conta criada com sucesso!')
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form':form}
    return render(request, 'authenticate/register.html', context)

def edit_profile(request):
    if request.method=='POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Perfil atualizado com sucesso!')
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form':form}
    return render(request, 'authenticate/edit_profile.html', context)

def change_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,'Perfil atualizado com sucesso!')
            return redirect('home')
    else:
        form = PasswordChangeForm(user=request.user)

    context = {'form':form}
    return render(request, 'authenticate/change_password.html', context)
