from django.shortcuts import redirect, render

from .forms import SimpleUserForm
from .models import Profile

def register(request):  # sourcery skip: extract-method, remove-unnecessary-else
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
            user.utm = request.POST.get('utm_source', '')
            user.save()
            profile = Profile(user=user)
            profile.utm = request.POST.get('utm_source', '')
            code = request.POST.get('ref_code')
            profile_ref = Profile.objects.filter(code=code)
            if profile_ref.exists():
                user_ref = profile_ref.first().user
                if user_ref.ip_address != request.META['REMOTE_ADDR']:
                    profile.recommended_by = user_ref
            profile.save()
            return redirect('account:register_success')
        else:
            data['form'] = form
            return render(request, 'account/register.html', data)

def register_success(request):
    data = {'title': 'Registrado com sucesso'}
    return render(request, 'account/register_success.html', data)
