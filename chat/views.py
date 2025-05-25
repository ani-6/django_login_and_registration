from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .models import Message

@login_required
def user_list(request):
    plus_users_group = Group.objects.get(name='PlusUsers')
    pu_admin_group = Group.objects.get(name='PUAdmin')  # New group reference
    current_user = request.user

    is_plus_user = current_user.groups.filter(name='PlusUsers').exists()
    is_PUAdmin = current_user.groups.filter(name='PUAdmin').exists()  # Check if the user is in PUAdmin group

    if not request.user.is_superuser:
        superuser_users = User.objects.filter(is_superuser=True).distinct().exclude(username=request.user.username)
        
        if not is_plus_user:
            if is_PUAdmin:
                plus_users_ids = plus_users_group.user_set.values_list('id', flat=True)
                nonsuperusers = User.objects.filter(
                    is_active=True
                ).distinct().exclude(
                    Q(username=request.user.username) |
                    ~Q(id__in=plus_users_ids)
                )
                
            else:
                # Get IDs from both PlusUsers and PUAdmin groups
                plus_users_ids = plus_users_group.user_set.values_list('id', flat=True)
                pu_admin_ids = pu_admin_group.user_set.values_list('id', flat=True)
                
                nonsuperusers = User.objects.filter(
                    is_active=True
                ).distinct().exclude(
                    Q(username=request.user.username) |
                    Q(id__in=plus_users_ids) |
                    Q(id__in=pu_admin_ids)
                )
        else:
            # Existing logic for PlusUsers
            pu_admin_ids = pu_admin_group.user_set.values_list('id', flat=True)
            plus_users_ids = plus_users_group.user_set.values_list('id', flat=True)
            nonsuperusers = User.objects.filter(
                is_active=True
            ).distinct().exclude(
                Q(username=request.user.username) |
                (~Q(id__in=plus_users_ids) &
                ~Q(id__in=pu_admin_ids))
            )
            
        users = nonsuperusers | superuser_users
    else:
        users = User.objects.all().distinct().exclude(username=request.user.username)
    
    context = {'pageobj':users,}
    return render(request, 'chat/user_list.html',context)

@login_required
def chat_room(request, username):
    other_user = User.objects.get(username=username)
    messages = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    )
    return render(request, 'chat/chat_room.html', {
        'other_user': other_user,
        'all_messages': messages
    })
