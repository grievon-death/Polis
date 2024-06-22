from django.db.utils import IntegrityError as AlreadyExists
from django_filters.rest_framework import DjangoFilterBackend
from pymongo.errors import CollectionInvalid
from rest_framework import views, viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.request import Request

from base.models import Type, Theme, Proposal, Debate, Comments
from polis.serializer import (TypeSerializer, ThemeSerializer,
                              ProposalSerializer, DebateSerializer)


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = ThemeSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    def create(self, request: Request, **kwargs: dict) -> Response:
        _data = request.data
        _proposal = Proposal(**_data)
        _serializer = ProposalSerializer(_proposal)

        if not _serializer.is_valid():
            return Response(
                data=_serializer.error_messages,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            _proposal.save()
        except AlreadyExists:
            return Response(
                data={ 'error': 'These proposal is already in debate!' }
            )

        return Response(
            data=ProposalSerializer(_proposal).data,
            status=status.HTTP_201_CREATED,
        )

    def list(self, request: Request, **kwargs: dict) -> Response:
        try:
            return Response(
                data=ProposalSerializer(Proposal.objects.filter(**kwargs)),
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={ 'error': str(e.args) },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class DebateViewSet(viewsets.ModelViewSet):
    queryset = Debate.objects.all()
    serializer_class = DebateSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]


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
