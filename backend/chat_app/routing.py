from django.urls import re_path,path
from .consumers import PostConsumer,PostFetchConsumer ,PostLikeCommentFollow
websocket_urlpatterns = [
    path('ws/posts/', PostConsumer.as_asgi()),
    path('ws/posts/fetch', PostFetchConsumer.as_asgi()),
    path('ws/PostLikeCommentFollow', PostLikeCommentFollow.as_asgi()),
    # path('ws/follow', FollowConsumer.as_asgi()),
    # path('ws/notifications', NotificationConsumer.as_asgi()),
    
    
]
