from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import *
from .models import *
from django.conf import settings
from datetime import datetime
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os, wget
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Q
from .Gdrive.upload import UploadToDrive

#fetch remote ip
def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

#Home view
@login_required
def home(request):
    myDate = datetime.now()
    formatedDate = myDate.strftime("%a, %Y-%m-%d")
    user_ip = get_ip_address(request)
    pagedata = HomeContent.objects.filter(user=request.user)
    update = HomeUpdates.objects.filter(user=request.user).order_by('-id')[:3][::-1]
    updates= reversed(update)
    context = {'user_ip':user_ip, 'date':formatedDate,'data':pagedata,'updates': updates}
    return render(request, 'users/home.html', context)


#Register view
class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        

        if form.is_valid():
            user = form.save()

            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='Users')
            user.groups.add(group)
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

#Logout view
def logoutUser(request):
    logout(request)
    return redirect('login')

#Reset password View
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')

#Change password View
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

#Settings view
@login_required
def Settings(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-settings')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/settings.html', {'user_form': user_form, 'profile_form': profile_form})

#Delete Avtar
@login_required 
def DeleteAvtar(request):
    profile = Profile.objects.get(user=request.user)
    print(profile)
    profile.profile_pic = "profile_images/default.jpg"
    profile.save()
    messages.success(request, 'Avtar deleted successfully')
    return redirect(to='users-settings')

#Profile view
@login_required
def ProfileView(request):
    return render(request, "users/profile.html")

#Notebook view
@login_required
def NotebookView(request):
    notes = Notebook.objects.filter(user=request.user)
    try:
        if request.method == 'POST':
            form = CreateNoteForm(request.POST)
    
            if form.is_valid():
                notebook = form.save(commit=False)
                notebook.user = request.user
                notebook.save()
                form=CreateNoteForm()
                messages.success(request, 'Your Note updated successfully')
                return HttpResponseRedirect('/notebook')
        else:
            form = CreateNoteForm()
    except:
        pass
    return render(request, "notebook/index.html", {'form': form, 'notes':notes})

#Main Gallery
@login_required
def MainGallery(request):
    statpath = "media/images/gallery/"
    img_list=os.listdir(statpath)
    for img in img_list[:]: 
        if not(img.endswith(".jpg") or img.endswith(".jpeg")):
            img_list.remove(img)
    context = {"images": img_list, "mediaPath": statpath, }
    return render(request, "gallery/maingallery.html", context)

#Gallery with pagination
@login_required
def Gallery(request):
    img_list = GalleryContent.objects.filter(user_id__exact=request.user).values()
    page = request.GET.get('page', 1)

    paginator = Paginator(img_list, 8)
    try:
        imgs = paginator.page(page)
    except PageNotAnInteger:
        imgs = paginator.page(1)
    except EmptyPage:
        imgs = paginator.page(paginator.num_pages)

    context = {"imgs":imgs,}
    return render(request, "gallery/extgallery.html",context)

#File downloader  
@login_required  
def Downloadfile(request):
    allfiles = UrlDownloaderGdrive.objects.filter(user=request.user)
    form = UrlDownloaderGdriveForm(request.POST)
    path = "media/images/downloads"

    if request.method == 'POST':
        if form.is_valid():
            search_id = form.cleaned_data['local_path']
            if search_id != None:
                file = search_id.split("/")[-1]
                if os.path.exists(os.path.join(path, file)):
                    print(file, "already downloaded")
                else:     
                    filename = wget.download(search_id, out=path) 
                    messages.success(request, 'File downloaded sucsessfullty : '+file)
                    folderid = "1A5O9S20pzgC6toVPbcY3FMoHAiEiJ5yY"
                    data = UploadToDrive(filename,folderid)
                    urld = form.save(commit=False)           
                    urld.user = request.user
                    urld.filename = file
                    urld.local_path = path+"/"+file  
                    urld.fileid = data['FileID']  
                    urld.folderid = data['FolderID']         
                    urld.shared = data['Shared']     
                    urld.save()
                    os.remove(filename)   
                    return HttpResponseRedirect('/urldownloader')
    context = {'list':list,'form':form,'allfiles':allfiles}
    return render(request, "downloader/download.html",context)

@login_required
def MarkdownView(request):
    mdata = Notebook.objects.filter(user = request.user)[:1].values()
    context = {'mdata':mdata}
    return render(request,'markdown/index.html', context)