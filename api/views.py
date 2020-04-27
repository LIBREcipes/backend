from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from rest_framework import viewsets, generics, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RecipeSerializer, IngredientSerializer, UserSerializer, RecipeIngredientSerializer, MyTokenObtainPairSerializer, FileSerializer
from core.models import Recipe, Ingredient, RecipeIngredient, MyUser, File

class CreateFileView(generics.CreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user:
            raise HttpResponseForbidden

        owner = MyUser.objects.get(pk=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=owner)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data))


class RecipeViewset(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    lookup_field = 'uuid'
    # permission_classes = (IsAuthenticated,)

    def list(self, request: Request):
        if request.user.is_authenticated:
            items = Recipe.objects.filter(Q(is_public=True) | Q(chef__uuid=request.user.uuid))
        else:
            items = Recipe.objects.filter(is_public=True)
        serializer = super().get_serializer(items, many=True)

        return Response(serializer.data)

    def retrieve(self, request: Request, uuid):
        if request.user.is_authenticated:
            item = Recipe.objects.filter(Q(is_public=True) | Q(chef__uuid=request.user.uuid), uuid=uuid)
        else:
            item = Recipe.objects.filter(uuid=uuid, is_public=True)

        if not item:
            raise Http404

        serializer = super().get_serializer(item[0])

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        chef = MyUser.objects.get(pk=request.user.id)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(chef=chef)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        # serializer.save(ingredients=ingredients)
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

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

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
    # permission_classes = (IsAuthenticated,)

    def list(self, request: Request):
        return HttpResponseForbidden()

    def retrieve(self, request: Request, uuid):
        if uuid == 'me' and request.user.is_authenticated:
            user = MyUser.objects.get(id=request.user.id)
        else:
            user = MyUser.objects.get(uuid=uuid)
        
        serializer = super().get_serializer(user)

        return Response(serializer.data)


class RecipeIngredientViewset(viewsets.ModelViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer
    # permission_classes = (IsAuthenticated,)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RecipesForChef(generics.ListAPIView):
    model = Recipe
    serializer_class = RecipeSerializer

    def get_queryset(self):
        chef_uuid = self.kwargs['chef_uuid']
        if self.request.user.is_authenticated and self.request.user.uuid == chef_uuid:
            return Recipe.objects.filter(chef__uuid=chef_uuid)
        else:
            return Recipe.objects.filter(chef__uuid=chef_uuid, is_public=True)