import os
from PIL import Image

def generate_thumbnail(image_path):
    # Open the uploaded image using Pillow
    image = Image.open(image_path)

    # Define the size for the thumbnail
    thumbnail_size = (100, 100)

    # Resize the image to create a thumbnail
    image.thumbnail(thumbnail_size)

    # Save the thumbnail to the same path as the original image
    thumb_path = os.path.join(os.path.dirname(image_path), 'thumbnail_' + os.path.basename(image_path))
    image.save(thumb_path)

def delete_old_image(old_profile_pic):
    directory, filename = os.path.split(old_profile_pic)
    print(filename)
    if filename == 'default.jpg':
        return None
    # Delete old image if it exists
    if old_profile_pic and os.path.exists(old_profile_pic):
        os.remove(old_profile_pic)

    # Add 'thumbnail_' prefix to the filename
    thumbnail_filename = 'thumbnail_' + filename

    # Concatenate the directory and the modified filename to create the new thumbnail path
    thumbnail_path = os.path.join(directory, thumbnail_filename)
    if thumbnail_path and os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)