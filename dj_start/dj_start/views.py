import logging

from django.shortcuts import render, HttpResponseRedirect
from django.views.generic.base import View
from django.core.urlresolvers import reverse

from .forms import ContactForm


logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html', {'msg': 'Nothing here yet...'})


class ContactView(View):
    form_class = ContactForm
    template_name = 'contact.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('contact'))
        return render(request, self.template_name, {'form': form})
