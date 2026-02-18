# feed/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment, Like
from .serializers import (
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    RegisterSerializer,
    LoginSerializer
)
from django.views.decorators.csrf import csrf_exempt
# --------------------------
# Auth: Register
# --------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "user": RegisterSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------
# Auth: Login
# --------------------------
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": RegisterSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --------------------------
# Post ViewSet
# --------------------------
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# --------------------------
# Add Comment
# --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt  # Disable CSRF for JWT/API usage
def add_comment(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------------
# Like Post
# --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if user already liked
    if Like.objects.filter(post=post, user=request.user).exists():
        return Response({"detail": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

    like = Like.objects.create(post=post, user=request.user)
    serializer = LikeSerializer(like)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
