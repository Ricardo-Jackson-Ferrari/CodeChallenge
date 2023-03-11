from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.shortcuts import redirect, render

from .decorators import not_login_required
from .facade import authenticate_user, set_active_account
from .forms import AuthForm, RegisterForm
from .models import UserNotActivated


@not_login_required()
def register(request):
    data = {'title': 'Registro'}

    if request.method == 'GET':
        form = RegisterForm()
        data['form'] = form
        return render(request, 'account/register.html', data)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form_new = form.save(commit=False)
            form_new.is_active = False
            form_new.save()
            return redirect('account:login')
        else:
            data['form'] = form
            return render(request, 'account/register.html', data)


def active_account(request, uidb4, token):
    if set_active_account(uidb4=uidb4, token=token):
        messages.success(request, 'Seu usuário foi ativo com sucesso.')
    else:
        messages.error(request, 'A url acessada não é válida.')

    return redirect('account:login')


def logout(request):
    logout_django(request)
    return redirect('account:login')


@not_login_required()
def login(request):
    data = {'title': 'acesso'}

    if request.method == 'GET':
        form = AuthForm()
        data['form'] = form

        return render(request, 'account/login.html', data)
    elif request.method == 'POST':
        form = AuthForm(request.POST)

        if form.is_valid():
            try:
                user = authenticate_user(**form.cleaned_data)
                login_django(request, user)
                return redirect('common:index')
            except UserNotActivated:
                data['form'] = form
                messages.error(request, 'Conta não ativa.')

                return render(request, 'account/login.html', data)
            except get_user_model().DoesNotExist:
                data['form'] = form
                messages.error(request, 'Dados inválidos')

                return render(request, 'account/login.html', data)
        else:
            data['form'] = form

            return render(request, 'account/login.html', data)
