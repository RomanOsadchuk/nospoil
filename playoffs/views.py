from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

import services
from .helpers import get_empty_grid
from .models import Playoff
from .permissions import IsOwnerOrReadOnly
from .serializers import PlayoffListSerializer, PlayoffDetailSerializer



def index(request):
    context = {'playoffs': Playoff.objects.all()}
    return TemplateResponse(request, 'playoffs/index.html', context)


def create(request):
    context = {'is_create_view': True}
    return TemplateResponse(request, 'playoffs/form.html', context)


def update(request, pk):
    playoff = get_object_or_404(Playoff, pk=pk)
    # not allowed
    context = {'is_create_view': False, 'playoff': playoff}
    return TemplateResponse(request, 'playoffs/form.html', context)


def detail(request, pk, slug=None):
    playoff = get_object_or_404(Playoff, pk=pk)
    services.inc_playoff_views(playoff)
    context = {'playoff': playoff}
    return TemplateResponse(request, 'playoffs/detail.html', context)


# ==== REST views ==== #

@api_view(['GET'])
def empty_grid(request, format=None):
    return Response(get_empty_grid())


# update last viewed, last edited

class PlayoffList(generics.ListCreateAPIView):
    queryset = Playoff.objects.all()
    serializer_class = PlayoffListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PlayoffDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Playoff.objects.all()
    serializer_class = PlayoffDetailSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
