from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Playoff
from .permissions import IsOwnerOrPublicOrReadOnly
from .serializers import PlayoffListSerializer, PlayoffDetailSerializer
from .services import get_empty_grid, inc_playoff_views, update_last_viewed


# ==== Template Views ==== #

def index(request):
    context = {'playoffs': Playoff.objects.all()}
    return TemplateResponse(request, 'playoffs/index.html', context)


def create(request):
    context = {'is_create_view': True}
    return TemplateResponse(request, 'playoffs/form.html', context)


def update(request, pk):
    playoff = get_object_or_404(Playoff, pk=pk)
    if playoff.private and request.user != playoff.owner:
        raise PermissionDenied('You can not edit this playoff')
    context = {'playoff': playoff, 'is_owner': request.user==playoff.owner}
    return TemplateResponse(request, 'playoffs/form.html', context)


def detail(request, pk, slug=None):
    playoff = get_object_or_404(Playoff, pk=pk)
    inc_playoff_views(playoff)
    update_last_viewed(request.session, playoff)
    is_editable = playoff.owner == request.user or not playoff.private
    context = {'playoff': playoff, 'is_editable': is_editable}
    return TemplateResponse(request, 'playoffs/detail.html', context)


# ==== Api Views ==== #

@api_view(['GET'])
def empty_grid(request, format=None):
    return Response(get_empty_grid())


class PlayoffList(generics.ListCreateAPIView):
    queryset = Playoff.objects.all()
    serializer_class = PlayoffListSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)
        else:
            serializer.save()


class PlayoffDetail(generics.RetrieveUpdateAPIView):
    queryset = Playoff.objects.all()
    serializer_class = PlayoffDetailSerializer
    permission_classes = (IsOwnerOrPublicOrReadOnly, )

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.owner:
            # only owner can make playoff private
            serializer.save(private=False)
        else:
            serializer.save()
