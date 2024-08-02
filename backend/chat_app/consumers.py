# import base64
# import json
# import logging
# from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
# from channels.db import database_sync_to_async
# from .models import Post, Tag, Like, Comment, Follow, Notification
# from .serializers import PostSerializer, NotificationSerializer
# from .utils import mark_notification_read, follow_user, unfollow_user
# from django.core.files.base import ContentFile
# from django.contrib.auth.models import User
# from django.core.exceptions import ObjectDoesNotExist

# logger = logging.getLogger(__name__)

# class PostConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = 'posts'
#         await self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get('action')

#         try:
#             if action == 'create':
#                 post_data = data.get('post')
#                 post = await self.create_post(post_data)
#                 await self.channel_layer.group_send(
#                     self.group_name,
#                     {
#                         'type': 'post_created',
#                         'post': PostSerializer(post).data
#                     }
#                 )
#             else:
#                 await self.send(text_data=json.dumps({'error': 'Invalid action'}))
#         except Exception as e:
#             logger.error(f"Error processing request: {e}")
#             await self.send(text_data=json.dumps({
#                 'error': f'An error occurred while processing the request: {str(e)}'
#             }))

#     @database_sync_to_async
#     def create_post(self, post_data):
#         tags = post_data.pop('tags', [])
#         media_data = post_data.pop('media', None)

#         # Decode base64 media data if provided
#         if media_data:
#             format, imgstr = media_data.split(';base64,')
#             ext = format.split('/')[-1]
#             media_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#         else:
#             media_file = None

#         post = Post.objects.create(**post_data)

#         if media_file:
#             post.media.save(media_file.name, media_file)

#         tag_objects = []
#         for tag_name in tags:
#             tag, created = Tag.objects.get_or_create(name=tag_name)
#             tag_objects.append(tag)

#         post.tags.set(tag_objects)
#         post.save()

#         return post
    

# class PostFetchConsumer(WebsocketConsumer):
#     def connect(self):
#         self.group_name = 'posts'
#         self.channel_layer.group_add(
#             self.group_name,
#             self.channel_name
#         )
#         self.accept()

#     def disconnect(self, close_code):
#         self.channel_layer.group_discard(
#             self.group_name,
#             self.channel_name
#         )

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get('action')

#         if action == 'fetch':
#             try:
#                 posts = self.fetch_posts()
#                 posts_data = [self.serialize_post(post) for post in posts]
#                 self.send(text_data=json.dumps({
#                     'action': 'fetch',
#                     'posts': posts_data
#                 }))
#             except Exception as e:
#                 logger.error(f"Error fetching posts: {e}")
#                 self.send(text_data=json.dumps({'error': 'An error occurred while fetching posts'}))
#         else:
#             self.send(text_data=json.dumps({'error': 'Invalid action'}))

#     def fetch_posts(self):
#         return Post.objects.all().order_by('-created_at')

#     def serialize_post(self, post):
#         return {
#             'id': post.pk,
#             'title': post.title,
#             'description': post.description,
#             'media': post.media.url if post.media else None,
#             'location': post.location,
#             'audience': post.audience,
#             'created_at': post.created_at.isoformat(),
#             'updated_at': post.updated_at.isoformat(),
#             'tags': list(post.tags.values_list('name', flat=True)),
#             'count_like': post.count_like,
#             'count_comment': post.count_comment,
#         }

# class PostLikeCommentFollow(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.group_name = 'post_updates'
#         await self.channel_layer.group_add(self.group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.group_name, self.channel_name)

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get('action')
#         username = data.get('username')
#     # Log received username
#         print(f"Received action: {action} from username: {username}")
  
#         try:
#             if action == 'comment':
#                 await self.handle_comment(data)
#             elif action == 'like':
#                 await self.handle_like(data)
#             else:
#                 await self.send(text_data=json.dumps({'error': 'Invalid action'}))
#         except Exception as e:
#             logger.error(f"Error processing request: {e}")
#             await self.send(text_data=json.dumps({
#                 'error': f'An error occurred while processing the request: {str(e)}'
#             }))

#     async def handle_comment(self, data):
#         try:
#             user = await database_sync_to_async(User.objects.get)(username=data['username'])
#             post = await database_sync_to_async(Post.objects.get)(id=data['post_id'])
#             content = data['content']

#             comment = await database_sync_to_async(Comment.objects.create)(user=user, post=post, content=content)
#             await self.channel_layer.group_send(
#                 self.group_name,
#                 {
#                     'type': 'post_comment',
#                     'comment': {
#                         'id': comment.id,
#                         # 'user': comment.user.username,
#                         'post_id': comment.post.id,
#                         'content': comment.content,
#                         'created_at': str(comment.created_at),
#                     }
#                 }
#             )
#         except ObjectDoesNotExist as e:
#             logger.error(f"Object not found: {e}")
#             await self.send(text_data=json.dumps({'error': 'User or post not found'}))
#         except Exception as e:
#             logger.error(f"Error handling comment: {e}")
#             await self.send(text_data=json.dumps({'error': 'An error occurred while handling comment'}))

#     async def handle_like(self, data):
#         try:
#             user = await database_sync_to_async(User.objects.get)(username=data['username'])
#             post = await database_sync_to_async(Post.objects.get)(id=data['post_id'])

#             like, created = await database_sync_to_async(Like.objects.get_or_create)(user=user, post=post)
#             if not created:
#                 await database_sync_to_async(like.delete)()

#             await self.channel_layer.group_send(
#                 self.group_name,
#                 {
#                     'type': 'post_like',
#                     'like': {
#                         # 'user': user.username,
#                         'post_id': post.id,
#                         'created_at': str(like.created_at),
#                         'liked': created,
#                     }
#                 }
#             )
#         except ObjectDoesNotExist as e:
#             logger.error(f"Object not found: {e}")
#             await self.send(text_data=json.dumps({'error': 'User or post not found'}))
#         except Exception as e:
#             logger.error(f"Error handling like: {e}")
#             await self.send(text_data=json.dumps({'error': 'An error occurred while handling like'}))

#     async def post_comment(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'comment',
#             'comment': event['comment']
#         }))

#     async def post_like(self, event):
#         await self.send(text_data=json.dumps({
#             'type': 'like',
#             'like': event['like']
#         }))
