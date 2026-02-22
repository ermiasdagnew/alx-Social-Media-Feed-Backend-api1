from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import PostViewSet, register_view, login_view, add_comment, like_post
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({"message": "API is running"})

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', api_root, name='api-root'),
    path('auth/register/', register_view, name='register'),
    path('auth/login/', login_view, name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', include(router.urls)),  # ✅ FIXED HERE

    path('posts/<int:id>/comments/', add_comment, name='add_comment'),
    path('posts/<int:id>/like/', like_post, name='like_post'),
]
