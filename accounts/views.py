from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView
from django.views.generic.edit import FormView

from playoffs.models import Playoff


class RegistrationView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/'
    
    def form_valid(self, form):
        name = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = User.objects.create_user(name, password=password)
        new_user = authenticate(username=name, password=password)
        login(self.request, new_user)
        return super(RegistrationView, self).form_valid(form)


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        context['playoffs'] = Playoff.objects.filter(owner=self.request.user)
        return context


class UserPageView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'accounts/user_page.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        obj = get_object_or_404(User, username=username)
        return obj
    
    def get_context_data(self, *args, **kwargs):
        context = super(UserPageView, self).get_context_data(*args, **kwargs)
        context['playoffs'] = Playoff.objects.filter(owner=self.object)
        return context
