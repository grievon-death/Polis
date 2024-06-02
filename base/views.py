from rest_framework import views, viewsets, status
from rest_framework.response import Response
from rest_framework.request import Request

from base.models import Type, Theme, Proposal, Debate, Comments
from polis.serializer import (TypeSerializer, ThemeSerializer,
                              ProposalSerializer, DebateSerializer)


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


class CommentViewSet(views.APIView):
    def get(self, request: Request, pk: int=None) -> Response:
        try:
            proposal = Proposal.objects.get(pk=pk)
        except Proposal.DoesNotExist:
            return Response(
                data={'error': 'Not found!'},
                status=status.HTTP_404_NOT_FOUND,
            )

        comments = Comments.get_comments(proposal)

        return Response(
            data=comments,
            status=status.HTTP_200_OK,
        )
