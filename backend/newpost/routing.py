from django.urls import path
from .consumers import PostCreateConsumer,PostFetchConsumer ,PostLikeComment

websocket_urlpatterns = [
    path('ws/posts/create', PostCreateConsumer.as_asgi()),
    path('ws/posts/fetch', PostFetchConsumer.as_asgi()),
    path('ws/PostLikeComment', PostLikeComment.as_asgi()),
    
    
]
