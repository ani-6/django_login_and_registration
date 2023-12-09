import json, requests

# fetch remote ip
def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        ip = user_ip_address.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def GetmimeType(find):
    f = open('main/static/data/mimetype.json')
    data = json.load(f)
    return data[find]

def downlaodfile(remote_url, fullfilepath):
    try:
        data = requests.get(remote_url)
        # Save file data to local copy
        with open(fullfilepath, 'wb')as file:
            file.write(data.content)
        return True
    except:
        print("Something went wrong.")