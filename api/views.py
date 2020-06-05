from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils.timezone import make_aware
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import (File, Ingredient, MyUser, Recipe, RecipeIngredient,
                         Token)

from .serializers import (FileSerializer, IngredientSerializer,
                          MyTokenObtainPairSerializer,
                          RecipeIngredientSerializer, RecipeSerializer,
                          UserSerializer, PasswordResetRequestSerializer, UserBaseSerializer)

from core.services import EmailService, TokenService


class CreateFileView(generics.CreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        owner = MyUser.objects.get(pk=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=owner)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.filter(is_public=True)
    serializer_class = RecipeSerializer
    lookup_field = 'uuid'

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        chef = MyUser.objects.get(pk=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chef=chef)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if not request.user.is_authenticated or instance.chef.id != request.user.id:
            raise exceptions.NotFound
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    

class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'uuid'

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def create(self, request, *args, **kwargs):
        user = MyUser.objects.get(pk=request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'

    def list(self, request: Request):
        if not request.user.is_superuser:
            raise exceptions.PermissionDenied()

        return super().list(request)

    def retrieve(self, request: Request, uuid):
        if uuid == 'me' and request.user.is_authenticated:
            serializer = super().get_serializer(MyUser.objects.get(id=request.user.id))
        else:
            serializer = UserBaseSerializer(MyUser.objects.get(uuid=uuid))

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if 'username' in request.data:
            request.data['username'] = request.data['username'].lower()

        serializer = super().get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.set_password(request.data['password'])
        user.save()


        if not user.uuid or not user.email:
            raise exceptions.APIException(detail="No data to send email.")

        token = TokenService.create(user.uuid, Token.TYPE_USER_CONFIRM, timedelta(hours=1)).get_token()

        EmailService().send_mail(
            'confirm_account.html',
            'Welcome to Cooksel',
            [user.email],
            { 'token': token, 'request': request,}
        )
        
        headers = super().get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super.destroy(request, args, kwargs)
        else:
            return exceptions.PermissionDenied()


class PasswordResetRequest(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = MyUser.objects.get(email=serializer.data['email'])
        except:
            return Response('ok')

        token = TokenService.create(user.uuid, Token.TYPE_PASSWORD_RESET, timedelta(hours=1)).get_token()

        EmailService().send_mail(
            'password_reset_request.html',
            'Reset your password',
            [user.email],
            { 'token': token, 'request': request,}
        )

        return Response('ok')

class RecipeIngredientViewset(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer

    permission_classes = (IsAuthenticatedOrReadOnly,)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RecipesForChef(generics.ListAPIView):
    model = Recipe
    serializer_class = RecipeSerializer

    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

    def get_queryset(self):
        chef_uuid = self.kwargs['chef_uuid']
        if self.request.user.is_authenticated and self.request.user.uuid == chef_uuid:
            return Recipe.objects.filter(chef__uuid=chef_uuid)
        else:
            return Recipe.objects.filter(chef__uuid=chef_uuid, is_public=True)