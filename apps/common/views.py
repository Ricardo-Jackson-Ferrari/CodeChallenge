from django.shortcuts import render


def index(request):
    data = {'title': 'home'}
    return render(request, 'common/index.html', data)
