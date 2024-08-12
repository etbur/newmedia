from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, default='girl.svg')
    status = models.CharField(default="Hi i'm using Etbur chat", max_length=255)
    online = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user_id=instance.pk)


class Message(models.Model):
    text = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True)
    date_time = models.DateTimeField(auto_now_add=True, blank=True)
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)

class Group(models.Model):
    pass

class Friends(models.Model):
    pass

class Markatplace(models.Model):
    pass

class Event(models.Model):
    pass

# from django.contrib.auth.models import User
# from django.db import models

# class Post(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

# class Comment(models.Model):
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

class Share(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


    # ///////////////////////////////// to///////////////////////




# group 

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='GroupMember')

class GroupMember(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)

class ChatMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class FileUpload(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)





class YourFollower(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    numberoffollowers = models.CharField(max_length=255, null=True, default='0')

class Student(models.Model):
    stuname = models.CharField(max_length=100)
    email = models.CharField(max_length=100)




# selam work


# class Tag(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name

# class Post(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     title = models.CharField(max_length=100, blank=True, null=True)
#     description = models.TextField()
#     media = models.FileField(upload_to='uploads/', blank=True, null=True)
#     tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
#     location = models.CharField(max_length=100, blank=True, null=True)
#     audience = models.CharField(max_length=20, choices=[
#         ('public', 'Public'),
#         ('friends', 'Friends'),
#         ('group', 'Group'),
#     ], default='public')
#     count_like = models.PositiveIntegerField(default=0)
#     count_comment = models.PositiveIntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title or "Untitled Post"

    

# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         unique_together = ('user', 'post')
    
#     def __str__(self):
#         return f'Like by {self.user} on {self.post}'


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f'Comment by {self.user} on {self.post}'



# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
#     post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
#     like = models.ForeignKey(Like, on_delete=models.CASCADE, null=True, blank=True)
#     message = models.CharField(max_length=200)
#     created_at = models.DateTimeField(auto_now_add=True)
#     read = models.BooleanField(default=False)

# class Follow(models.Model):
#     follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
#     followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('follower', 'followee')
    
#     def __str__(self):
#         return f'{self.follower} follows {self.followee}'


   