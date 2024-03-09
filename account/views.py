from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *
from .forms import *

# Create your views here.
class registerView(View):
    form_class = register_form
    initial = {'key': 'value'}
    template_name = 'account/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(registerView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Users')   #Get users group
            user.groups.add(group)     #Add user to users group
            messages.success(request, f'Account created for {username}')
            return redirect(to='account:login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class customLogin(LoginView):
    form_class = login_form

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(600)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
        else:
            self.request.session['remember_me'] = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(customLogin, self).form_valid(form)


class resetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('account:login')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'account/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('account:users-settings')


@login_required
def settings_view(request):
    if request.method == 'POST':
        user_form = updateUser_form(request.POST, instance=request.user)
        profile_form = updateProfile_form(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='account:users-settings')
    else:
        user_form = updateUser_form(instance=request.user)
        profile_form = updateProfile_form(instance=request.user.profile)

    return render(request, 'account/settings.html', {'user_form': user_form, 'profile_form': profile_form})

#Delete Avtar
@login_required 
def deleteAvtar_view(request):
    profile = Profile.objects.get(user=request.user)
    profile.profile_pic = "Account/profile_images/default.jpg"
    profile.save()
    messages.success(request, 'Avtar deleted successfully')
    return redirect(to='account:users-settings')

#Profile view
@login_required
def profile_view(request):
    return render(request, "account/profile.html")

@login_required
def chats_view(request):
    users = User.objects.filter(is_active=True).distinct().exclude(username=request.user.username)
    context = {'pageobj':users,}
    return render(request, 'account/chats.html',context)


@login_required
def chat_view(request,id):
    userName = User.objects.get(id=id)
    print(userName)
    query = Q() | (Q(sender__exact=request.user) & Q(receiver_id=id)) | (Q(sender_id=id) & Q(receiver__exact=request.user))
    all_commnets = Messages.objects.filter(query).order_by('created_at').distinct()
    form = messages_form(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            message = form.cleaned_data['message']
            fbform = form.save(commit=False)           
            fbform.sender = request.user
            fbform.receiver = User.objects.get(id=id)
            fbform.message = message
            fbform.save()
            messages.success(request, 'Message sent!')
            to_url = '/account/chat/'+str(id)
            return HttpResponseRedirect(to_url)
    else:
        form = form
    context = {'pageobj':all_commnets,'userName':userName,'form':form,}
    return render(request, 'account/chat.html',context)

#Logout method
def logoutUser_view(request):
    logout(request)
    return redirect('account:login')