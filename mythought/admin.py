from django.contrib import admin

# Register your models here.

from .models import Post, ConversationMessage, Conversation, Notification

admin.site.register(Post)
admin.site.register(Conversation)
admin.site.register(ConversationMessage)
admin.site.register(Notification)
