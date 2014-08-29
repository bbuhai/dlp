import logging

from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import ContactForm


logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html', {'msg': 'Nothing here yet...'})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return render(request, 'contact.html', {'msg': 'Thanks!'})

    form = ContactForm()
    logger.debug(form)

    return render(request, 'contact.html', {'form': form})