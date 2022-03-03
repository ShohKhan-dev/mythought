from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)
    avatar = models.ImageField(upload_to='uploads/', blank=True, null=True)

User.userprofile = property(lambda u:UserProfile.objects.get_or_create(user=u)[0])


class Post(models.Model):
    body = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    users = models.ManyToManyField(User, related_name='conversations')
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-modified_at']

    
class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        self.conversation.save()

        super(ConversationMessage, self).save(*args, **kwargs)


class Notification(models.Model):
    MESSAGE = 'message'
    FOLLOWER = 'follower'
    LIKE = 'like'
    MENTION = 'mention'

    CHOICES = (
        (MESSAGE, 'Message'),
        (FOLLOWER, 'Follower'),
        (LIKE, 'Like'),
        (MENTION, 'Mention')
    )

    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)

    notification_type = models.CharField(max_length=20, choices=CHOICES)
    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='creatednotifications', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']
