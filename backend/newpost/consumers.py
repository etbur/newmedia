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
from django.contrib.auth import get_user_model


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
#         # Assuming 'Profile' is the model storing additional user details
#         user_profile = Profile.objects.filter(user=post.user).first()
#         profile_picture_url = user_profile.photo.url if user_profile and user_profile.photo else None
        
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
#             'username':post.username,
#             "profile_picture":post.profile_picture,
#         }

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
            self.fetch_posts()
        elif action == 'edit':
            self.edit_post(data.get('post_id'), data.get('new_data'))
        elif action == 'delete':
            self.delete_post(data.get('post_id'))
        else:
            self.send(text_data=json.dumps({'error': 'Invalid action'}))

    def fetch_posts(self):
        posts = Post.objects.all().order_by('-created_at')
        posts_data = [self.serialize_post(post) for post in posts]
        self.send(text_data=json.dumps({
            'action': 'fetch',
            'posts': posts_data
        }))

    def edit_post(self, post_id, new_data):
        try:
            post = Post.objects.get(id=post_id)
            # Ensure the user is authorized to edit the post
            if self.scope['user'] != post.user:
                self.send(text_data=json.dumps({'error': 'Unauthorized'}))
                return

            for key, value in new_data.items():
                setattr(post, key, value)
            post.save()

            self.send(text_data=json.dumps({'action': 'edit', 'post': self.serialize_post(post)}))
        except Post.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Post not found'}))

    def delete_post(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
            # Ensure the user is authorized to delete the post
            if self.scope['user'] != post.user:
                self.send(text_data=json.dumps({'error': 'Unauthorized'}))
                return

            post.delete()
            self.send(text_data=json.dumps({'action': 'delete', 'post_id': post_id}))
        except Post.DoesNotExist:
            self.send(text_data=json.dumps({'error': 'Post not found'}))

    def serialize_post(self, post):
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
            'username': post.username,
            'profile_picture': profile_picture_url,
        }


class PostLikeComment(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"Client {self.channel_name} connected.")
        # Allow all users to connect
        await self.channel_layer.group_add(
            "post_group",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"Client {self.channel_name} disconnected.")
        await self.channel_layer.group_discard(
            "post_group",
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")
        post_id = data.get("post_id")
        username = data.get("username")

        if action == "like":
            liked = data.get("liked")
            await self.handle_like(post_id, username, liked)
        elif action == "comment":
            content = data.get("content")
            await self.handle_comment(post_id, username, content)
        elif action == "fetch_comments":
            await self.fetch_comments(post_id)

    async def handle_like(self, post_id, username, liked):
        try:
            post = await database_sync_to_async(Post.objects.get)(id=post_id)
            if liked:
                post.count_like += 1
            else:
                post.count_like -= 1
            await database_sync_to_async(post.save)()
            await self.channel_layer.group_send(
                "post_group",
                {
                    "type": "send_like",
                    "like": {
                        "post_id": post_id,
                        "liked": liked
                    }
                }
            )
        except ObjectDoesNotExist:
            await self.send_error("Post does not exist.")
        except Exception as e:
            await self.send_error(f"An error occurred while handling like: {str(e)}")

    async def handle_comment(self, post_id, username, content):
        if not content.strip():
            await self.send_error("Comment content cannot be empty.")
            return

        try:
            user = await database_sync_to_async(get_user_model().objects.get)(username=username)
            post = await database_sync_to_async(Post.objects.get)(id=post_id)
            comment = await database_sync_to_async(Comment.objects.create)(
                post=post,
                user=user,
                content=content,
            )
            post.count_comment += 1
            await database_sync_to_async(post.save)()

            await self.channel_layer.group_send(
                "post_group",
                {
                    "type": "send_comment",
                    "comment": {
                        "post_id": post_id,
                        "username": username,
                        "content": content,
                        "created_at": comment.created_at.isoformat(),
                    }
                }
            )
        except ObjectDoesNotExist:
            await self.send_error("Post or user does not exist.")
        except Exception as e:
            await self.send_error(f"An error occurred while handling comment: {str(e)}")

    async def fetch_comments(self, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id)
            comments_data = [
                {
                    "username": comment.user.username,
                    "content": comment.content,
                    "created_at": comment.created_at.isoformat(),
                }
                for comment in comments
            ]
            await self.send(text_data=json.dumps({
                "type": "comments",
                "post_id": post_id,
                "comments": comments_data
            }))
        except Exception as e:
            await self.send_error(f"An error occurred while fetching comments: {str(e)}")
    
    async def send_like(self, event):
        await self.send(text_data=json.dumps({
            "type": "like",
            "like": event["like"]
        }))

    async def send_comment(self, event):
        await self.send(text_data=json.dumps({
            "type": "comment",
            "comment": event["comment"]
        }))

    async def send_error(self, error_message):
        await self.send(text_data=json.dumps({
            "type": "error",
            "error": error_message
        }))
