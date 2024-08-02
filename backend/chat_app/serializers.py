import datetime

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from chat_app.models import Message, Group, GroupMember, ChatMessage, FileUpload, Share, Student

class MessageSerializer(serializers.Serializer):
    text = serializers.CharField()
    read = serializers.BooleanField(read_only=True)
    date_time = serializers.DateTimeField(required=False)
    sender_id = serializers.IntegerField(read_only=True)
    receiver = serializers.SlugField(write_only=True)

    def create(self, validated_data):
        try:
            user = User.objects.get(username=validated_data['receiver'])
            message = Message()
            message.text = validated_data['text']
            message.sender = self.context['request'].user
            message.receiver = user
            message.save()
            self.__broadcast(message)
            return validated_data
        except Exception as e:
            raise Exception('Error', e)

    def __broadcast(self, message: Message):
        serializer = MessageModelSerializer(message, many=False)
        n_message = serializer.data
        n_message['read'] = False
        print(n_message)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_%s' % message.receiver.username, {
                'type': 'new_message',
                'message': n_message
            }
        )


class MessageModelSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(read_only=True, source='sender.username')
    read = serializers.BooleanField(default=True)

    class Meta:
        model = Message
        fields = ('text', 'sender', 'date_time', 'read')


class UsersWithMessageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    photo = serializers.ImageField(source='profile.photo')
    online = serializers.BooleanField(source='profile.online')
    status = serializers.CharField(source='profile.status')
    messages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('name', 'username', 'photo', 'online', 'status', 'messages')

    def get_name(self, obj):
        if obj.first_name:
            return obj.get_full_name()
        return obj.username

    def get_messages(self, obj):
        messages = Message.objects.filter(
            Q(receiver=obj, sender=self.context['request'].user) |
            Q(sender=obj, receiver=self.context['request'].user)).prefetch_related('sender', 'receiver')
        serializer = MessageModelSerializer(messages.order_by('date_time'), many=True)
        return serializer.data


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    photo = serializers.ImageField(source='profile.photo')
    online = serializers.BooleanField(source='profile.online')
    status = serializers.CharField(source='profile.status')
    messages = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('name', 'username', 'photo', 'online', 'status', 'messages')

    def get_name(self, obj):
        if obj.first_name:
            return obj.get_full_name()
        return obj.username

    def get_messages(self, obj):
        return []


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        user = super(RegistrationSerializer, self).create(validated_data)
        self.__notify_others(user)
        return validated_data

    def __notify_others(self, user):
        serializer = UserSerializer(user, many=False)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notification', {
                'type': 'new_user_notification',
                'message': serializer.data
            }
        )

# class CommentSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Comment
#         fields = ['id', 'user', 'post', 'content', 'created_at', 'updated_at']

# class PostSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     comments = CommentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Post
#         fields = ['id', 'user', 'content', 'created_at', 'updated_at', 'comments']


# group


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'members']

class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'user', 'is_admin']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'group', 'sender', 'content', 'timestamp']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ['id', 'group', 'user', 'file', 'timestamp']
        

#  social Post
# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')

#     class Meta:
#         model = Comment
#         fields = ('id', 'user', 'content', 'created_at')

class ShareSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Share
        fields = ('id', 'user', 'created_at')

# class PostSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
#     likes_count = serializers.SerializerMethodField()
#     comments = CommentSerializer(many=True, read_only=True)
#     shares = ShareSerializer(many=True, read_only=True)

#     class Meta:
#         model = Post
#         fields = ('id', 'user', 'content', 'created_at', 'updated_at', 'likes_count', 'likes', 'comments', 'shares')

    # def get_likes_count(self, obj):
    #     return obj.likes.count()



class StudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Student
    fields = ['id', 'stuname', 'email']





#  selam work

# class TagSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tag
#         fields = '__all__'

# class LikeSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()

#     class Meta:
#         model = Like
#         fields = '__all__'

# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()

#     class Meta:
#         model = Comment
#         fields = '__all__'

# class PostSerializer(serializers.ModelSerializer):
#     tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)

#     class Meta:
#         model = Post
#         fields = ['title', 'description', 'media', 'tags', 'location', 'audience', 'created_at', 'updated_at']
#     def get_media_url(self, obj):
#         if obj.media:
#             return obj.media.url
#         return None


# class NotificationSerializer(serializers.ModelSerializer):
#     user = serializers.StringRelatedField()
#     post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False)
#     comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), required=False)
#     like = serializers.PrimaryKeyRelatedField(queryset=Like.objects.all(), required=False)

#     class Meta:
#         model = Notification
#         fields = '__all__'

# class FollowSerializer(serializers.ModelSerializer):
#     follower = serializers.StringRelatedField()
#     followed = serializers.StringRelatedField()

#     class Meta:
#         model = Follow
#         fields = '__all__'
