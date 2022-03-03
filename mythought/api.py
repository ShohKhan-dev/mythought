import json 
import re

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .utilities import create_notification
from .models import Post, Like, ConversationMessage, Conversation
from django.contrib.auth.models import User

@login_required
def api_add_post(request):

    data = json.loads(request.body)
    body = data['body']

    post= Post.objects.create(body=body, created_by=request.user)

    results = re.findall("(^|[^@\w])@(\w{1,20})", body)

    for result in results:
        result = result[1]

        if User.objects.filter(username=result).exists() and result != request.user.username:
            create_notification(request, User.objects.get(username=result), 'mention')

    return JsonResponse({'success': True})



@login_required
def api_add_like(request):

    data = json.loads(request.body)
    post_id = data['post_id']

    if not Like.objects.filter(post_id=post_id).filter(created_by=request.user).exists():
        like = Like.objects.create(post_id=post_id, created_by=request.user)
        post = Post.objects.get(pk=post_id)

        if post.created_by != request.user:

            create_notification(request, post.created_by, 'like')
    
    return JsonResponse({'success': True})


@login_required
def api_add_message(request):
    data = json.loads(request.body)
    content = data['content']
    conversation_id = data['conversation_id']

    message = ConversationMessage.objects.create(conversation_id=conversation_id, content=content, created_by=request.user)

    to_user = None

    for user in message.conversation.users.all():
        if user != request.user:
            create_notification(request, user, 'message')

    return JsonResponse({'success': True})