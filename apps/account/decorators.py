from django.shortcuts import redirect


def not_login_required(redirect_url='/'):
    def _func(func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return func(request, *args, **kwargs)

        return wrapper

    return _func
