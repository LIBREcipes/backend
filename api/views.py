from datetime import datetime, timedelta

from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.utils.timezone import make_aware
from rest_framework import exceptions, filters, generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.models import (File, Ingredient, MyUser, Recipe, RecipeIngredient,
                         Token)

from .serializers import (FileSerializer, IngredientSerializer,
                          MyTokenObtainPairSerializer,
                          RecipeIngredientSerializer, RecipeSerializer,
                          UserSerializer)


class CreateFileView(generics.CreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()

    def post(self, request, *args, **kwargs):
        if not request.user:
            raise exceptions.NotAuthenticated()

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
            raise exceptions.NotFound()

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
        raise exceptions.PermissionDenied()

    def retrieve(self, request: Request, uuid):
        if uuid == 'me' and request.user.is_authenticated:
            user = MyUser.objects.get(id=request.user.id)
        else:
            user = MyUser.objects.get(uuid=uuid)
        
        serializer = super().get_serializer(user)

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if 'username' in request.data:
            request.data['username'] = request.data['username'].lower()
        returnVal =  super().create(request, args, kwargs)

        if not returnVal.data['uuid'] or not returnVal.data['email']:
            raise exceptions.APIException(detail="No data to send email.")

        token = Token.objects.create(
            type=Token.TYPE_USER_CONFIRM,
            reference=returnVal.data['uuid'],
            valid_until=make_aware(datetime.now() + timedelta(hours=1))
        )

        html_body = get_template('api/emails/confirm_account.html').render(
            {"request": request, "token": token}
        )

        send_mail(
            "Welcome to Cooksel",
            html_body,
            'cooksel@madebit.be',
            [returnVal.data['email']],
            html_message=html_body
        )
        
        return returnVal
    
    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super.destroy(request, args, kwargs)
        else:
            return exceptions.PermissionDenied()


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
