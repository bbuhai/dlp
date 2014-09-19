from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'msg': 'Nothing here yet...'})
