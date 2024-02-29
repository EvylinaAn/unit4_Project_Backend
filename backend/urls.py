"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main_app import views
# from .views import add_photo

from rest_framework_simplejwt import views as jwt_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'looks', views.LookViewSet)
router.register(r'looksCategories', views.LooksCategoryViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'photos', views.PhotoViewSet)
router.register(r'featuredPhoto', views.FeaturedPhotoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('logout/', views.LogoutView.as_view(), name ='logout'),
    path('signup/', views.SignupView.as_view(), name='auth_register'),
    # path('home/', views.HomeView.as_view(), name ='home'),
    # path('add_photo/<int:post_id>/', views.add_photo, name='add_photo'),
    # path('posts/<int:post_id>/add_photo/', add_photo , name='add_photo'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/current_user/', views.current_user, name='current_user'),
    # path('api/create_comment/', views.create_comment, name='create_comment')
]






