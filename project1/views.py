from django.shortcuts import render, redirect,get_object_or_404
from .models import login,Notification,Message
# from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.http import JsonResponse
from twilio.rest import Client
from django.conf import settings
from django.contrib.auth.hashers import make_password
from .models import Post, Like, Comment
# Twilio client initialization
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if user already exists
        if not login.objects.filter(username=username).exists():
            login.objects.create(username=username, password=password)
            return redirect('success')
        else:
            return render(request, 'register.html', {'error': 'Username already exists'})
    
    return render(request, 'register.html')

from django.contrib.auth import authenticate, login as auth_login
def success(request):
    return render(request, 'success.html')

def loginform(request):
    next_url = request.GET.get('next', '/profile')  # Default redirect to /profile
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect(next_url)
        return render(request, 'loginform.html', {'error': 'Invalid username or password'})

    return render(request, 'loginform.html')

def forget(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        
        # Check if the username exists in the database
        user = login.objects.filter(username=username).first()
        
        if user and user.password != new_password:
            # Update the user's password
            user.password = new_password
            user.save()
            return redirect('success')
        else:
            return render(request, 'forget.html', {'error': 'Enter valid details'})
    
    return render(request, 'forget.html')

def otp(request):
    return render(request, 'otp.html')

def newpass(request):
    return render(request, 'newpass.html')

def loginsuccess(request):
    user_id = request.session.get('user_id')  # Retrieve user_id from session

    if request.method == 'GET':
        if user_id:
            current_user = login.objects.filter(id=user_id).first()
            if current_user:
                all_posts = Post.objects.select_related('user')
                post_details = []
                for post in all_posts:
                    post_owner = post.user
                    post_owner_image_url = post_owner.image.url if post_owner.image and post_owner.image.name else '/static/default-avatar.png'
                    
                    # Append post details
                    post_details.append({
                        'id': post.id,
                        'user': post_owner.username,
                        'user_image_url': post_owner_image_url,
                        'image_url': post.image.url if post.image and post.image.name else '/static/default-post.png',
                        'video_url': post.video.url if post.video and post.video.name else None,  # Video URL
                        'caption': post.caption,
                    })
                return render(request, 'loginsuccess.html', {
                    'username': current_user.username,
                    'image_url': current_user.image.url if current_user.image and current_user.image.name else '/static/default-avatar.png',
                    'posts': sorted(post_details, key=lambda x: x['id'], reverse=True),
                })
        return redirect('loginform')

    if request.method == 'POST':
        username = request.POST.get('username')
        gmail = request.POST.get('gmail')
        password = request.POST.get('password')
        user = login.objects.filter(
            Q(username=username) | Q(gmail=gmail),
            password=password
        ).first()
        if user:
            request.session['user_id'] = user.id
            return redirect('loginsuccess')
        else:
            return render(request, 'loginform.html', {'error': 'Invalid credentials'})

    return redirect('loginform')


def search(request):
    if request.method == "GET" and "query" in request.GET:
        query = request.GET.get("query", "").strip()
        
        if not query:
            return JsonResponse({"success": False, "error": "No query provided"})

        # Filter users based on the query (e.g., search by username)
        users = login.objects.filter(username__icontains=query)
        
        # Prepare the results as a list of dictionaries
        results = [
            {
                "id": user.id,
                "username": user.username,
                "image_url": user.image.url if user.image else "/static/default-avatar.png"
            }
            for user in users
        ]

        return JsonResponse({"success": True, "results": results})

    return render(request, "search.html")
import logging
def notifications(request):
    logger = logging.getLogger(__name__)
    user_id = request.session.get('user_id')  # Assuming session stores the user ID
    if user_id:
        current_user = get_object_or_404(login, id=user_id)
        notifications = Notification.objects.filter(user=current_user, is_deleted=False).order_by('-timestamp')

        # Prepare notification data
        notification_data = []
        for notification in notifications:
            # Extract triggered_by user details if available
            if notification.triggered_by:
                user_profile_image = (
                    notification.triggered_by.image.url
                    if notification.triggered_by.image
                    else '/static/default-avatar.png'
                )
                username = notification.triggered_by.username
            else:
                user_profile_image = '/static/default-avatar.png'
                username = "Unknown User"

            # Add notification data to the list
            notification_data.append({
                'id': notification.id,
                'message': notification.message,
                'timestamp': notification.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'user_profile_image': user_profile_image,
                'username': username,
            })

        # Log the data being sent to the template for debugging
        logger.debug(f"Notification data for user {current_user.username}: {notification_data}")

        # Get unseen notifications count for badge display
        unseen_count = Notification.objects.filter(user=current_user, is_seen=False, is_deleted=False).count()

        # Mark all unseen notifications as seen when the page loads
        Notification.objects.filter(user=current_user, is_seen=False, is_deleted=False).update(is_seen=True)

        return render(request, 'notifications.html', {
            'notifications': notification_data,
            'unseen_count': unseen_count,  # Include unseen count for badge
        })
    else:
        # Redirect to login if no session exists
        return redirect('loginform')

  # Re


from .models import login,Post  # Import your custom login model
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def delete_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.delete()
    return JsonResponse({'success': True, 'message': 'Notification deleted successfully.'})
# @login_required
def profile(request):
    user_id = request.session.get('user_id')  # Assuming session stores the user ID
    if user_id:
        current_user = login.objects.get(id=user_id)
        posts = Post.objects.filter(user=current_user)
        username = current_user.username or "Unknown User"
        image_url = current_user.image.url if current_user.image else '/media/profile_pics/default-profile.png'
    else:
        return redirect("loginform")  # Redirect to login if not authenticated

    return render(request, "profile.html", {
        "username": username,
        "image_url": image_url,
        "posts": posts
    })
def changepass(request):
    return render(request, 'changepass.html')

def message(request):
    user = request.user
    contacts = login.objects.exclude(id=user.id)  # Exclude the logged-in user
    return render(request, 'messages.html', {'contacts': contacts})


from django.db import models
def chat(request, recipient_id):
    user = request.user
    recipient = get_object_or_404(login, id=recipient_id)

    # Fetch chat messages
    chat_messages = Message.objects.filter(
        (Q(sender_id=user.id) & Q(recipient_id=recipient.id)) |
        (Q(sender_id=recipient.id) & Q(recipient_id=user.id))
    ).order_by('timestamp')

    # Handle new message submission
    if request.method == 'POST':
        content = request.POST.get('message', '').strip()
        if content:
            Message.objects.create(
                # sender_id=user.id,
                sender_username=user.username,
                recipient_id=recipient.id,
                recipient_username=recipient.username,
                content=content
            )
        return redirect('chat', recipient_id=recipient.id)

    return render(request, 'chat.html', {
    'recipient': recipient,
    'messages': chat_messages,
    'user': user,
})

# @login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Post
from django.contrib.auth.decorators import login_required

# View to create or update a post
# @login_required
def create_post(request, post_id=None):
    """
    Handles the creation of new posts or the editing of existing posts.
    Sends notifications to other users when a new post is created.
    """
    if request.method == "POST":
        current_user = request.user  # The logged-in user

        # Retrieve uploaded files and form data
        image = request.FILES.get("image")
        video = request.FILES.get("video")
        caption = request.POST.get("caption", "").strip()

        if post_id:
            # Editing an existing post
            post = get_object_or_404(Post, id=post_id)

            # Ensure the current user is the author
            if post.user != current_user:
                return JsonResponse(
                    {"error": "You are not authorized to edit this post."},
                    status=403
                )

            # Update the post's fields if new data is provided
            if image:
                post.image = image
            if video:
                post.video = video
            post.caption = caption or post.caption
            post.save()

            return redirect("profile")  # Redirect after updating the post

        else:
            # Creating a new post
            if not (image or video):
                return JsonResponse(
                    {"error": "Please upload an image or video."},
                    status=400
                )

            # Create the post
            post = Post.objects.create(user=current_user, image=image, video=video, caption=caption)

            # Notify other users about the new post
            users_to_notify = login.objects.exclude(id=current_user.id)  # Exclude the post creator
            for recipient in users_to_notify:
                Notification.objects.create(
                    user=recipient,
                    message=f"{current_user.username} posted something new!",
                    notification_type='post',
                )

            return redirect("profile")  # Redirect after creating the post

    # Redirect if the request is not POST
    return redirect("profile")
  # Redirect if it's not a POST request
 # Fallback for non-POST requests


# @login_required
def delete_post(request, post_id):
    user_id = request.session.get('user_id')  # Retrieve the user ID from the session
    if not user_id:
        return JsonResponse({"error": "User not logged in"}, status=403)

    # Get the currently logged-in user
    current_user = get_object_or_404(login, id=user_id)

    # Get the post to be deleted, ensuring it belongs to the current user
    post = get_object_or_404(Post, id=post_id, user=current_user)

    # Delete the post
    post.delete()
    return redirect('profile')  # Redirect to the
def index(request):
    return render(request, 'profile.html') 
def change_profile_photo(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('loginform')

    user = get_object_or_404(login, id=user_id)
    if request.method == 'POST':
        profile_photo = request.FILES.get('profile_photo')
        if profile_photo:
            user.image = profile_photo
            user.save()

            # Notify other users about the profile update
            users_to_notify = login.objects.exclude(id=user.id)
            for recipient in users_to_notify:
                Notification.objects.create(
                    user=recipient,
                    message=f"{user.username} updated their profile picture.",
                    notification_type='profile',
                )

            messages.success(request, "Profile photo updated successfully.")
            return redirect('profile')
    return render(request, 'change_profile_photo.html', {'user': user})

import json

# def open(request):
#     return render(request,'open.html')
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post, Like, Comment
import json
from django.views.decorators.csrf import csrf_exempt

# Toggle Like
# Toggle Like
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.csrf import csrf_protect
# @login_required
# @login_required
import logging
logger = logging.getLogger(__name__)

@csrf_exempt
def toggle_like(request, post_id):
    # if not request.user.is_authenticated:
    #     return JsonResponse({'success': False, 'message': 'User is not authenticated'}, status=401)

    if request.method == 'POST':
        user = request.username
        post = get_object_or_404(Post, id=post_id)

        like, created = Like.objects.get_or_create(user=user, post=post)

        if created:
            # Liked the post
            post.likes_count += 1
            liked = True
        else:
            # Unlike the post
            like.delete()
            post.likes_count -= 1
            liked = False

        post.save()
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': post.likes_count,
        })
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def add_comment(request, post_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content', '').strip()

            if not content:
                logger.warning("Comment content is empty.")
                return JsonResponse({'success': False, 'message': 'Comment cannot be empty!'})

            user = request.user
            post = get_object_or_404(Post, id=post_id)
            logger.info(f"User: {user}, Post ID: {post.id}, Content: {content}")

            # Create the comment
            comment = Comment.objects.create(user=user, post=post, content=content)
            post.comments_count += 1
            post.save()

            logger.info(f"Comment added to Post {post.id}. Comments count: {post.comments_count}")

            return JsonResponse({
                'success': True,
                'comment': {
                    'user': user.username,
                    'content': comment.content,
                },
                'comments_count': post.comments_count,
            })
        except json.JSONDecodeError:
            logger.error("Invalid JSON data received.")
            return JsonResponse({'success': False, 'message': 'Invalid JSON data!'}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

@csrf_exempt
def share_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)

        # Increment the shares count
        post.shares_count += 1
        post.save()

        return JsonResponse({
            "success": True,
            "shares_count": post.shares_count
        })
    return JsonResponse({'success': True, 'shares_count': 5})
def delete_notification(request):
    if request.method == 'POST':
        notification_id = request.POST.get('id')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()  # Soft delete or flag as deleted in DB
            return JsonResponse({'status': 'success'}, status=200)
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

def permanent_delete_notification(request):
    if request.method == 'POST':
        notification_id = request.POST.get('id')
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()  # Permanent delete from DB
            return JsonResponse({'status': 'success'}, status=200)
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
@csrf_exempt
def restore_notification(request):
    """Restore a soft-deleted notification."""
    if request.method == 'POST':
        notification_id = request.POST.get('id')
        try:
            notification = Notification.objects.get(id=notification_id, is_deleted=True)
            notification.is_deleted = False  # Restore notification
            notification.save()
            return JsonResponse({'status': 'success', 'message': 'Notification restored.'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found or not deleted.'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})