from django.shortcuts import redirect, render

from .decorators import not_login_required
from .forms import SimpleUserForm


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
            form_new = form.save(commit=False)
            form_new.is_active = False
            form_new.save()
            return redirect('account:login')
        else:
            data['form'] = form
            return render(request, 'account/register.html', data)
