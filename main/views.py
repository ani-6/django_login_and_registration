from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import HttpResponseRedirect
from datetime import datetime
from .helpers import *
from .models import *
from .forms import *
from .services import *
from base.Gdrive.gdriveOps import *

# Create your views here.
@login_required
def home_view(request):
    try:
        myDate = datetime.now()
        formatedDate = myDate.strftime("%a, %Y-%m-%d")
        user_ip = get_ip_address(request)
        pagedata = get_ImportantLinks(request.user,True)
        updates = get_LatestUpdates(request.user)
        context = {'user_ip':user_ip, 'date':formatedDate,'data':pagedata,'updates': updates}
        return render(request,"main/index.html", context)  
    except:
        return render (request, "error-404.html")

@login_required
def imageGallery_view(request):
    object_list = get_GalleryObjects(request.user)
    page = request.GET.get('page', 1)

    paginator = Paginator(object_list, 8)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {"page_obj":page_obj,}
    return render(request, "main/image_gallery.html",context)

#Main Gallery
@login_required
def localGallery_view(request):
    # Path to the directory you want to scan
    directory_path = 'media/Main/gallery/'

    # Get a list of all files in the specified directory
    directory_contents = [file for file in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, file))]

    # Filter out only image files
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = [file for file in directory_contents if os.path.splitext(file)[1].lower() in image_extensions]

    # Pagination
    paginator = Paginator(image_files, 8)  # Show 8 images per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj,'dir_path': directory_path}

    return render(request, 'main/local_gallery.html', context)

#File downloader  
@login_required  
def downlaodUrlToGdrive_view(request):
    allfiles = get_AllDriveObjects(request.user)
    form = urlToGdrive_form(request.POST)
    path = "media/Main/downloads/"

    if request.method == 'POST':
        if form.is_valid():
            url = form.cleaned_data['local_path']
            if (url != None and url != ''):
                file = url.split("/")[-1]
                if IfDriveObjectExists(request.user,file,url):
                    messages.info(request, file +' already downloaded.')
                else:     
                    fullfilepath = path+file     
                    if downlaod_file(url,fullfilepath):
                        folderid = request.user.profile.remote_fol_id
                        ext = file.split(".")[-1]
                        mimetype = get_mimeType(ext)
                        data = UploadToDrive(fullfilepath,folderid,mimetype)
                        urld = form.save(commit=False)           
                        urld.user = request.user
                        urld.filename = file
                        urld.original_path = url
                        urld.fileid = data['FileID']  
                        urld.folderid = data['FolderID']         
                        urld.shared = data['Shared']     
                        urld.save()
                        messages.success(request, 'File downloaded sucsessfullty : '+file)
                        os.remove(fullfilepath)   
                        return HttpResponseRedirect('/urldownloader/')
    context = {'list':list,'form':form,'allfiles':allfiles}
    return render(request, "main/urltodrive.html",context)

@login_required
def notifications_view(request):
    objects = get_Announcements()
    context = {'objects':objects}
    return render(request, "main/notifications.html",context)