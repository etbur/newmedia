from django.urls import path
from .consumers import PostCreateConsumer,PostFetchConsumer ,PostLikeCommentFollow

websocket_urlpatterns = [
    path('ws/posts/create', PostCreateConsumer.as_asgi()),
    path('ws/posts/fetch', PostFetchConsumer.as_asgi()),
    path('ws/PostLikeCommentFollow', PostLikeCommentFollow.as_asgi()),
    
    
]
