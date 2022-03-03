from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .utilities import create_notification

from .models import Post, Conversation, ConversationMessage, Notification
from django.contrib.auth.models import User
from .forms import UserProfileForm



# Create your views here.

def frontpage(request):
    #return HttpResponse("<h1> Hello </h1>")

    return render(request, 'frontpage.html')


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})


@login_required
def feed(request):
    userids = [request.user.id]

    for author in request.user.userprofile.follows.all():
        userids.append(author.user.id)

    posts = Post.objects.filter(created_by_id__in=userids)

    for post in posts:
        likes = post.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            post.liked = True
        else:
            post.liked = False


    return render(request, 'feed.html', {'posts': posts})



@login_required
def search(request):
    
    query = request.GET.get('query', '')

    if len(query) > 0:
        authors = User.objects.filter(username__icontains=query)
        posts = Post.objects.filter(body__icontains=query)
    else:
        authors = []
        posts = []

    context = {
        'query': query,
        'authors': authors,
        'posts': posts
    }

    return render(request, 'search.html', context)


@login_required
def userprofile(request, username):
    user = get_object_or_404(User, username=username)

    posts = user.posts.all()


    for post in posts:
        likes = post.likes.filter(created_by_id=request.user.id)

        if likes.count() > 0:
            post.liked = True
        else:
            post.liked = False

    context = {
        'user': user,
        'posts': posts
    }

    return render(request, 'userprofile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if form.is_valid():
            form.save()
            
            return redirect('userprofile', username=request.user.username)
    else:
        form = UserProfileForm(instance=request.user.userprofile)
    
    context = {
        'user': request.user,
        'form': form
    }

    return render(request, 'edit_profile.html',  context)



@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)

    request.user.userprofile.follows.add(user.userprofile)

    create_notification(request, user, 'follower')


    return redirect('userprofile', username=username)


@login_required
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)

    request.user.userprofile.follows.remove(user.userprofile)


    return redirect('userprofile', username=username)



def followers(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'followers.html', {'user': user})


def follows(request, username):
    user = get_object_or_404(User, username=username)

    return render(request, 'follows.html', {'user': user})



@login_required
def conversations(request):
    conversations = request.user.conversations.all()

    return render(request, 'conversations.html', {'conversations': conversations})


@login_required
def conversation(request, user_id):
    conversations = Conversation.objects.filter(users__in=[request.user.id])
    conversations = conversations.filter(users__in=[user_id])

    if conversations.count() == 1:
        conversation = conversations[0]
    else:
        recipient = User.objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.users.add(recipient)
        conversation.save()

    return render(request, 'conversation.html', {'conversation': conversation})

@login_required
def notifications(request):
    goto = request.GET.get('goto', '')
    notification_id = request.GET.get('notification', 0)

    if goto != '':
        notification = Notification.objects.get(pk=notification_id)
        notification.is_read = True
        notification.save()

        if notification.notification_type == Notification.MESSAGE:
            return redirect('conversation', user_id=notification.created_by.id)
        elif notification.notification_type == Notification.FOLLOWER:
            return redirect('userprofile', username=notification.created_by.username)
        elif notification.notification_type == Notification.LIKE:
            return redirect('userprofile', username=notification.to_user.username)
        elif notification.notification_type == Notification.MENTION:
            return redirect('userprofile', username=notification.created_by.username)
    
    return render(request, 'notifications.html')


