from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import PostViewSet, register_view, login_view, add_comment, like_post
from django.http import JsonResponse

# Root endpoint
def api_root(request):
    return JsonResponse({"message": "API is running"})

# Router for PostViewSet
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

urlpatterns = [
    path('', api_root, name='api-root'),                     # Root: /
    path('auth/register/', register_view, name='register'),  # /auth/register/
    path('auth/login/', login_view, name='login'),           # /auth/login/
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # refresh JWT
    path('posts/', include(router.urls)),                    # /posts/ and /posts/<id>/
    path('posts/<int:id>/comments/', add_comment, name='add_comment'),
    path('posts/<int:id>/like/', like_post, name='like_post'),
]
