from django.db.utils import IntegrityError as AlreadyExists
from rest_framework import views, status
from rest_framework.request import Request
from rest_framework.response import Response

from user.models import Profile
from polis.serializer import ProfileSerializer, SingInSerializer, LoginSerializer
from polis.utils import Tool


class ProfileViewSet(views.APIView):
    def get(self, request: Request) -> Response:
        # if request.user.is_anonymous:
        #     return Response(
        #         data={'error': 'Unauthorized'},
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )

        _query = request.query_params

        if not Tool.validate_request_query(_query, requireds={'id', 'first_name', 'last_name'}):
            return Response(
                data={ 'error': 'Invalid query!' },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer = ProfileSerializer(Profile.objects.filter(**_query))
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={ 'error': e.args},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SingInViewSet(views.APIView):
    queryset = Profile.objects.all()

    def post(self, request: Request) -> Response:
        _data = request.data

        if not _data:
            return Response(
                data={ 'error': 'Invalid payload' },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer = SingInSerializer(data=_data)

            if not serializer.is_valid():
                return Response(
                    data=serializer.error_messages,
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.create(_data)

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except AlreadyExists:
            return Response(
                data={ 'error': 'User already exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data={ 'error': e.args},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginViewSet(views.APIView):
    def post(self, request: Request) -> Response:
       return Response(
           data='OK',
            status=status.HTTP_200_OK,
       )
