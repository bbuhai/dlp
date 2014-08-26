from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    context = {'bool': False}
    return render(request, 'personalitytests/home.html', context)



def test(request, test_id):
    return HttpResponse("Test id: {}".format(test_id))


def result(request, test_id):
    return HttpResponse("Test result for id: {}".format(test_id))