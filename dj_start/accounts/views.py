from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.views import login, logout_then_login
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import UserCreationForm


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        next_link = reverse('survey:list')
        template_response = login(request=request, template_name=self.template_name)
        template_response.context_data['next'] = next_link
        return template_response

    def post(self, request):
        template_response = login(request=request, template_name=self.template_name)
        return template_response


class LogoutView(View):
    def post(self, request):
        return logout_then_login(request=request)


class CreateView(View):
    template_name = 'accounts/create.html'

    def get(self, request):
        form = UserCreationForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
