from django.db.utils import IntegrityError as AlreadyExists
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from user.models import Profile
from polis.serializer import ProfileSerializer, SingInSerializer, LoginSerializer
from polis.utils import Tool


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    )
    ordering = ['id']
    lookup_field = 'id'
    ordering_fields= ['id']
    filterset_fields = {
        'id': ['exact'],
    }
    serializer_class = ProfileSerializer

    def list(self, request: Request) -> Response:
        return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request: Request) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request: Request, id: int) -> Response:
        _data = request.data

        try:
            _profile = Profile.objects.get(id=id)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            _profile.first_name = _data.get('first_name', _profile.first_name)
            _profile.last_name = _data.get('last_name', _profile.last_name)
            _profile.email = _data.get('email', _profile.email)

            if _data.get('password'):
                _profile.set_password(_data.pop('password'))

            _profile.save()
        except AlreadyExists:
            return Response(
                data={ 'error': 'Invalid change!' },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                data={ 'error': str(e) },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=ProfileSerializer(_profile).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request: Request) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def singin(request: Request) -> Response:
    _requireds = ["first_name", "last_name", "email", "document", "password"]
    _data = request.data

    if not all([k in _requireds for k in _data.keys()]) or not _data.keys():
        return Response(
            data={ 'error': f'All and only these fields: {",".join(_requireds)}' },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        _password = _data.pop('password')
        _profile = Profile(**_data)
        _profile.set_password(_password)
        _profile.save()
    except AlreadyExists:
        return Response(
            data={ 'error': 'User already exist!' },
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        return Response(
            data={ 'error': str(e) },
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        data=SingInSerializer(_profile).data,
        status=status.HTTP_201_CREATED,
    )


@api_view(['POST'])
def login(request: Request) -> Response:
    _requireds = ['email', 'password']
    _data = request.data

    if not all([k in _requireds for k in _data.keys()]) or not _data.keys():
        return Response(
            data={ 'error': f'All and only these fields: {",".join(_requireds)}' },
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        _user = Profile.objects.get(email=_data['email'])

        if not _user.check_password(_data['password']):
            return Response(
                data={ 'error': 'Invalid email or password!' },
                status=status.HTTP_404_NOT_FOUND,
            )
    except Profile.DoesNotExist:
        return Response(
            data={ 'error': 'Invalid email or password!' },
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        data={ 'token': 'toma essa token, caraio' },
        status=status.HTTP_200_OK,
    )   
