from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


from . import views


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'recipes', views.RecipeViewset)
router.register(r'ingredients', views.IngredientViewset)
router.register(r'users', views.UserViewset)


urlpatterns = [
    path('', include(router.urls)),
    path('auth', include('rest_framework.urls', namespace='rest_framework')),
    path('auth/password-reset-request', views.PasswordResetRequest.as_view(), name='password-reset-request'),

    path('token', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    path('users/<uuid:chef_uuid>/recipes', views.RecipesForChef.as_view(), name='recipes-for-chef'),

    path('files', views.CreateFileView.as_view(), name='files')
    # path('token/verify', TokenVerifyView.as_view(), name='token_verify'),
]

