import os, json, requests
from django.conf import settings

# fetch remote ip
def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_mimeType(find):
    f = open(os.path.join(settings.BASE_DIR,'base/static/data/mimetype.json'))
    data = json.load(f)
    return data[find]

def downlaod_file(remote_url, fullfilepath):
    try:
        data = requests.get(remote_url)
        # Save file data to local copy
        with open(fullfilepath, 'wb')as file:
            file.write(data.content)
        return True
    except:
        print("Something went wrong.")