import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import Post, Comment, Interaction

class UserType(DjangoObjectType):
    class Meta:
        model = User

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class InteractionType(DjangoObjectType):
    class Meta:
        model = Interaction

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int())

    def resolve_all_posts(self, info):
        return Post.objects.all().select_related('author').prefetch_related('comments')

    def resolve_post_by_id(self, info, id):
        return Post.objects.get(id=id)
