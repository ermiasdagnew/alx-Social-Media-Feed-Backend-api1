from django.contrib import admin
from django.urls import path, include
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),  # GraphQL endpoint
    path('', include('feed.urls')),  # Include all your feed app URLs
]
