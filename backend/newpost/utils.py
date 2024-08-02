from asgiref.sync import sync_to_async
from .models import Notification, Follow
from django.contrib.auth.models import User

@sync_to_async
def mark_notification_read(user, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=user)
        if not notification.read:
            notification.read = True
            notification.save()
    except Notification.DoesNotExist:
        pass

@sync_to_async
def follow_user(follower, followed_user_id):
    followed_user = User.objects.get(id=followed_user_id)
    follow, created = Follow.objects.get_or_create(follower=follower, followed=followed_user)
    if created:
        # Notify the followed user about the new follower
        Notification.objects.create(
            user=followed_user,
            follower=follow,
            message=f"{follower.username} started following you."
        )

@sync_to_async
def unfollow_user(follower, followed_user_id):
    followed_user = User.objects.get(id=followed_user_id)
    follow = Follow.objects.filter(follower=follower, followed=followed_user).first()
    if follow:
        follow.delete()
        # Notify the unfollowed user about the unfollowing
        Notification.objects.create(
            user=followed_user,
            follower=follow,
            message=f"{follower.username} stopped following you."
        )