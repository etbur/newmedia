from django.urls import path

from chat_app.consumers.message import MessageConsumer
from chat_app.consumers.notification import NewUserConsumer
from newpost.consumers import PostConsumer,PostFetchConsumer,PostLikeCommentFollow

websocket_urlpatterns = [
    path('ws/notification/', NewUserConsumer.as_asgi()),
    path('ws/message/<str:username>/', MessageConsumer.as_asgi()),
    path('ws/posts/', PostConsumer.as_asgi()),
    path('ws/posts/fetch', PostFetchConsumer.as_asgi()),
    path('ws/PostLikeCommentFollow', PostLikeCommentFollow.as_asgi()),
]
