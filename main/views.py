from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
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
def Home_View(request):
    try:
        myDate = datetime.now()
        formatedDate = myDate.strftime("%a, %Y-%m-%d")
        user_ip = get_ip_address(request)
        pagedata = GetImportantLinks(request.user,True)
        updates = GetLatestUpdates(request.user)
        context = {'user_ip':user_ip, 'date':formatedDate,'data':pagedata,'updates': updates}
        return render(request,"main/index.html", context)  
    except:
        return render (request, "error-404.html")

@login_required
def Image_Gallery_View(request):
    #try:
        object_list = GetGalleryObjects(request.user)
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
def Local_Gallery(request):
    statpath = "media/Main/gallery/"
    img_list=os.listdir(statpath)
    for img in img_list[:]: 
        if not(img.endswith(".jpg") or img.endswith(".jpeg")):
            img_list.remove(img)
    context = {"images": img_list, "mediaPath": statpath, }
    return render(request, "main/local_gallery.html", context)

#File downloader  
@login_required  
def DownlaodUrlToGdrive(request):
    allfiles = GetAllDriveObjects(request.user)
    form = UrlToGdriveForm(request.POST)
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
                    if downlaodfile(url,fullfilepath):
                        folderid = request.user.profile.remote_fol_id
                        ext = file.split(".")[-1]
                        mimetype = GetmimeType(ext)
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
def notifications(request):
    objects = getAnnouncements()
    context = {'objects':objects}
    return render(request, "main/notifications.html",context)