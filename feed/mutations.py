import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from graphql import GraphQLError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Post, Comment, Like

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class RegisterUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, username, email, password):
        if User.objects.filter(username=username).exists():
            raise GraphQLError("Username already exists")
        User.objects.create_user(username=username, email=email, password=password)
        return RegisterUser(message="User registered successfully")

class LoginUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    access = graphene.String()
    refresh = graphene.String()

    def mutate(self, info, username, password):
        user = User.objects.filter(username=username).first()
        if not user or not user.check_password(password):
            raise GraphQLError("Invalid credentials")
        refresh = RefreshToken.for_user(user)
        return LoginUser(access=str(refresh.access_token), refresh=str(refresh))

class CreatePost(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)

    post = graphene.Field(PostType)

    def mutate(self, info, content):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")
        post = Post.objects.create(author=user, content=content)
        return CreatePost(post=post)

class AddComment(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)
        content = graphene.String(required=True)

    message = graphene.String()

    def mutate(self, info, post_id, content):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        Comment.objects.create(post=post, author=user, content=content)
        return AddComment(message="Comment added")

class LikePost(graphene.Mutation):
    class Arguments:
        post_id = graphene.Int(required=True)

    message = graphene.String()

    def mutate(self, info, post_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError("Authentication required")
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise GraphQLError("Post not found")
        if Like.objects.filter(post=post, user=user).exists():
            raise GraphQLError("Already liked")
        Like.objects.create(post=post, user=user)
        return LikePost(message="Post liked")

class Mutation(graphene.ObjectType):
    register = RegisterUser.Field()
    login = LoginUser.Field()
    create_post = CreatePost.Field()
    add_comment = AddComment.Field()
    like_post = LikePost.Field()
