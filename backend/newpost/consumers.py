import base64
import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from channels.db import database_sync_to_async
from .models import Post, Tag, Like, Comment, Follow, Notification
from .serializers import PostSerializer, NotificationSerializer
from .utils import mark_notification_read, follow_user, unfollow_user
from django.core.files.base import ContentFile
from django.contrib.auth.models import User
from chat_app.models import  Profile
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

logger = logging.getLogger(__name__)

class PostCreateConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'posts'
        
        # Just accept the connection without checking user authentication
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()
        logger.info("WebSocket connection established.")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        logger.info("WebSocket connection closed.")

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        try:
            if action == 'create':
                post_data = data.get('post')
                # Assuming you may need to remove 'user' or handle post creation without user
                post = await self.create_post(post_data)
                serialized_post = await self.serialize_post(post)
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'post_created',
                        'post': serialized_post
                    }
                )
                logger.info("Post created.")
            else:
                await self.send(text_data=json.dumps({'error': 'Invalid action'}))
                logger.warning(f"Invalid action received: {action}")
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            await self.send(text_data=json.dumps({
                'error': f'An error occurred while processing the request: {str(e)}'
            }))

    @database_sync_to_async
    def create_post(self, post_data):
        tags = post_data.pop('tags', [])
        media_data = post_data.pop('media', None)

        # Decode base64 media data if provided
        if media_data:
            format, imgstr = media_data.split(';base64,')
            ext = format.split('/')[-1]
            media_file = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        else:
            media_file = None

        with transaction.atomic():
            # Create the post without user or with a default user if necessary
            post = Post.objects.create(**post_data)

            if media_file:
                post.media.save(media_file.name, media_file)

            tag_objects = []
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                tag_objects.append(tag)

            post.tags.set(tag_objects)
            post.save()

        return post

    @database_sync_to_async
    def serialize_post(self, post):
        # Get user profile
        try:
            user_profile = Profile.objects.get(user=post.user)
            profile_picture_url = user_profile.profile_picture.url if user_profile.profile_picture else None
        except Profile.DoesNotExist:
            profile_picture_url = None
        
        return {
            'id': post.pk,
            'title': post.title,
            'description': post.description,
            'media': post.media.url if post.media else None,
            'location': post.location,
            'audience': post.audience,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
            'tags': list(post.tags.values_list('name', flat=True)),
            'count_like': post.count_like,
            'count_comment': post.count_comment,
            'username':post.username,
            "profile_picture":post.profile_picture,
        }
class PostFetchConsumer(WebsocketConsumer):
    def connect(self):
        self.group_name = 'posts'
        self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'fetch':
            try:
                posts = self.fetch_posts()
                posts_data = [self.serialize_post(post) for post in posts]
                self.send(text_data=json.dumps({
                    'action': 'fetch',
                    'posts': posts_data
                }))
            except Exception as e:
                logger.error(f"Error fetching posts: {e}")
                self.send(text_data=json.dumps({'error': 'An error occurred while fetching posts'}))
        else:
            self.send(text_data=json.dumps({'error': 'Invalid action'}))

    def fetch_posts(self):
        return Post.objects.all().order_by('-created_at')

    def serialize_post(self, post):
        # Assuming 'Profile' is the model storing additional user details
        user_profile = Profile.objects.filter(user=post.user).first()
        profile_picture_url = user_profile.photo.url if user_profile and user_profile.photo else None
        
        return {
            'id': post.pk,
            'title': post.title,
            'description': post.description,
            'media': post.media.url if post.media else None,
            'location': post.location,
            'audience': post.audience,
            'created_at': post.created_at.isoformat(),
            'updated_at': post.updated_at.isoformat(),
            'tags': list(post.tags.values_list('name', flat=True)),
            'count_like': post.count_like,
            'count_comment': post.count_comment,
            'username':post.username,
            "profile_picture":post.profile_picture,
        }
        
        
class PostLikeCommentFollow(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'post_updates'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        username = data.get('username')
        post_id = data.get('post_id')
        
        # Log received data
        print(f"Received action: {action} from username: {username}, post_id: {post_id}")

        try:
            if action == 'comment':
                await self.handle_comment(data)
            elif action == 'like':
                await self.handle_like(data)
            else:
                await self.send(text_data=json.dumps({'type': 'error', 'error': 'Invalid action'}))
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'error': f'An error occurred while processing the request: {str(e)}'
            }))

    async def handle_comment(self, data):
        try:
            user = await database_sync_to_async(User.objects.get)(username=data['username'])
            post = await database_sync_to_async(Post.objects.get)(id=data['post_id'])
            content = data['content']

            comment = await database_sync_to_async(Comment.objects.create)(user=user, post=post, content=content)
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'post_comment',
                    'comment': {
                        'id': comment.id,
                        'post_id': comment.post.id,
                        'content': comment.content,
                        'created_at': str(comment.created_at),
                    }
                }
            )
        except ObjectDoesNotExist as e:
            logger.error(f"Object not found: {e}")
            await self.send(text_data=json.dumps({'type': 'error', 'error': 'User or post not found'}))
        except Exception as e:
            logger.error(f"Error handling comment: {e}")
            await self.send(text_data=json.dumps({'type': 'error', 'error': 'An error occurred while handling comment'}))

    async def handle_like(self, data):
        try:
            user = await database_sync_to_async(User.objects.get)(username=data['username'])
            post = await database_sync_to_async(Post.objects.get)(id=data['post_id'])

            like, created = await database_sync_to_async(Like.objects.get_or_create)(user=user, post=post)
            if not created:
                await database_sync_to_async(like.delete)()

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'post_like',
                    'like': {
                        'post_id': post.id,
                        'created_at': str(like.created_at),
                        'liked': created,
                        'user': user.username
                    }
                }
            )
        except ObjectDoesNotExist as e:
            logger.error(f"Object not found: {e}")
            await self.send(text_data=json.dumps({'type': 'error', 'error': 'User or post not found'}))
        except Exception as e:
            logger.error(f"Error handling like: {e}")
            await self.send(text_data=json.dumps({'type': 'error', 'error': 'An error occurred while handling like'}))
