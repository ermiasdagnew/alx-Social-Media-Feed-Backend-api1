import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from .models import Post, Comment

class UserType(DjangoObjectType):
    class Meta:
        model = User

class PostType(DjangoObjectType):
    class Meta:
        model = Post

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment

class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType, first=graphene.Int(), skip=graphene.Int())
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))

    def resolve_all_posts(self, info, first=None, skip=None):
        qs = Post.objects.all().select_related('author').prefetch_related('comments').order_by('-created_at')
        if skip:
            qs = qs[skip:]
        if first:
            qs = qs[:first]
        return qs

    def resolve_post_by_id(self, info, id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExist:
            return None
