from django.shortcuts import redirect, render

from .decorators import not_login_required
from .forms import SimpleUserForm
from .models import Profile

@not_login_required()
def register(request):
    data = {'title': 'Registro'}

    if request.method == 'GET':
        form = SimpleUserForm()
        data['form'] = form
        return render(request, 'account/register.html', data)
    elif request.method == 'POST':
        form = SimpleUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.ip_address = request.META['REMOTE_ADDR']
            user.save()
            profile = Profile(user=user, recommended_by=user)
            profile.save()
            return redirect('account:register_success')
        else:
            data['form'] = form
            return render(request, 'account/register.html', data)

def register_success(request):
    data = {'title': 'Registrado com sucesso'}
    return render(request, 'account/register_success.html', data)
