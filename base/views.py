from django_filters.rest_framework import DjangoFilterBackend
from pymongo.errors import CollectionInvalid
from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request

from base.models import Type, Theme, Proposal, Debate, Comments
from polis.serializer import (TypeSerializer, ThemeSerializer,
                              ProposalSerializer, DebateSerializer)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = [DjangoFilterBackend]


class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    filter_backends = [DjangoFilterBackend]


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    filter_backends = [DjangoFilterBackend]


class DebateViewSet(viewsets.ModelViewSet):
    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
    filter_backends = [DjangoFilterBackend]


class CommentViewSet(views.APIView):
    def get(self, request: Request) -> Response:
        _invalid_filter = Response(
            data={'error': 'Invalid filter'},
            status=status.HTTP_400_BAD_REQUEST,
        )

        try:
            collection = self.kwargs['collection']

            if not collection:
                return  _invalid_filter
        except KeyError:
                return  _invalid_filter

        try:
            comments = Comments.get_comments(collection)
            return Response(
                data=comments,
                status=status.HTTP_200_OK,
            )
        except CollectionInvalid:
                return  _invalid_filter
