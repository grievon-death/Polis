from rest_framework import views, viewsets

from base.models import Type, Theme, Proposal, Debate, Comments
from polis.serializer import (TypeSerializer, ThemeSerializer,
                              ProposalSerializer, DebateSerializer,
                              CommentsSerializer)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class DebateViewSet(viewsets.ModelViewSet):
    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
