from __future__ import unicode_literals
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView

from .forms import PlayoffForm
from .models import Playoff, Match
import services


class PlayoffIndexView(ListView):
    model = Playoff
    context_object_name = 'playoffs'
    template_name = 'playoffs/index.html'


class PlayoffDetailView(DetailView):
    model = Playoff
    context_object_name = 'playoff'
    template_name = 'playoffs/playoff_detail.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayoffDetailView, self).get_context_data(*args, **kwargs)
        services.update_last_viewed(self.request.session, self.object)
        services.inc_playoff_views(self.object)
        owned = (self.object.owner == self.request.user)
        ctx['editable'] = owned or not self.object.private
        ctx['grid'] = services.get_playoff_grid(self.object)
        ctx['is_detail_view'] = True
        return ctx


class PlayoffCreateView(CreateView):
    model = Playoff
    form_class = PlayoffForm
    initial = {'rounds': 3, 'double': True}
    template_name = 'playoffs/playoff_form.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayoffCreateView, self).get_context_data(*args, **kwargs)
        ctx['grid'] = services.get_edit_grid(self.request.POST)
        ctx['is_create_view'] = True
        return ctx

    def form_valid(self, form):
        self.object = form.save(self.request.user)
        services.save_matches(self.request.POST, self.object)
        services.update_last_edited(self.request.session, self.object)
        return HttpResponseRedirect(self.get_success_url())


class PlayoffUpdateView(UpdateView):
    model = Playoff
    context_object_name = 'playoff'
    fields = ['sport', 'title']  # private
    template_name = 'playoffs/playoff_form.html'

    def dispatch(self, request, *args, **kwargs):
        playoff = self.get_object()
        if playoff.private and playoff.owner != request.user:
            raise PermissionDenied('You can not edit this playoff')
        return super(PlayoffUpdateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(PlayoffUpdateView, self).get_context_data(*args, **kwargs)
        if self.request.POST:
            grid = services.get_edit_grid(self.request.POST, self.object)
        else:
            grid = services.get_playoff_grid(self.object)
        ctx['grid'] = grid
        return ctx

    def form_valid(self, form):
        self.object = form.save()
        services.update_matches(self.request.POST, self.object)
        services.update_last_edited(self.request.session, self.object)
        return HttpResponseRedirect(self.get_success_url())
