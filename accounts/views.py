from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth import authenticate, login as login_user
from django.core.urlresolvers import reverse
from accounts.forms import NewUserForm
from django.http.response import HttpResponseRedirect


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
        form = NewUserForm()
        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.clean_password2()
            form.save()
            user = authenticate(username=username, password=password)
            login_user(request, user)

            return HttpResponseRedirect(reverse('survey:list'))

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
