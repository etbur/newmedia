from django.urls import path
from .consumers import PostConsumer,PostFetchConsumer ,PostLikeCommentFollow

websocket_urlpatterns = [
    path('ws/posts/', PostConsumer.as_asgi()),
    path('ws/posts/fetch', PostFetchConsumer.as_asgi()),
    path('ws/PostLikeCommentFollow', PostLikeCommentFollow.as_asgi()),
    
    
]
