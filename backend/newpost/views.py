from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from .serializers import PostSerializer, TagSerializer, LikeSerializer, CommentSerializer, FollowSerializer
from .models import Post, Tag, Like, Comment, Follow


# Create your views here.
class index(APIView):
    async def get(self, request):
        return Response('hello!')

# Tag view
class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

# Like view
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

# Comment view
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

# Post view
class PostViewSet(viewsets.ModelViewSet):
       queryset = Post.objects.all().order_by('-created_at')
       serializer_class = PostSerializer
     # permission_classes = [permissions.IsAuthenticated]


# Follow view
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    