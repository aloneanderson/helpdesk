from helpdesk.api.serialaizers import RegistrationSerializer, RequisitionsSerializer, CommentSerializer
from rest_framework import viewsets
from helpdesk.models import Requisitions, Comment, NewToken
from rest_framework.response import Response
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import exceptions
from .permissions import CommentPermisson


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['get', 'post', 'put', 'patch']


class CustomTokenAuthentication(TokenAuthentication):

    def authenticate_credentials(self, key):
        try:
            token = NewToken.objects.get(key=key)
        except NewToken.DoesNotExist:
            raise exceptions.AuthenticationFailed("Token ERROR")
        if not token.user.is_superuser:
            if token.time_to_die + timedelta(minutes=5) < timezone.now():
                token.delete()
                raise exceptions.AuthenticationFailed("Token ERROR")
            else:
                token.time_to_die = timezone.now()
                token.save()
        return token.user, token


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = NewToken.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'token_time': token.time_to_die
        })


class RequisitionsViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Requisitions.objects.all()
    serializer_class = RequisitionsSerializer
    http_method_names = ['get', 'post', 'put', 'patch']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    authentication_classes = [CustomTokenAuthentication]
    permission_classes = [IsAuthenticated, CommentPermisson]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
