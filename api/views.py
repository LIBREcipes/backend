from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import RecipeSerializer, IngredientSerializer, UserSerializer, RecipeIngredientSerializer, MyTokenObtainPairSerializer
from core.models import Recipe, Ingredient, RecipeIngredient, MyUser


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

    
class IngredientViewset(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'uuid'
    # permission_classes = (IsAuthenticated,)


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