from PIL import Image
import pillow_heif
import imagehash


def extract_metadata(filename):        
    
    pillow_heif.register_heif_opener() 
    metadata = {}
    filepath = filename                             # change this if change file location

    with Image.open(filepath) as img:
        metadata = img.info                         # Extract basic metadata
        exif_data = img.getexif()
        if exif_data:
            for tag, value in exif_data.items():
                tag_name = Image.ExifTags.TAGS.get(tag, tag)
                metadata[tag_name] = str(value)

    drop_keys = ['exif', 'xmp', 'icc_profile']
    for key in drop_keys:
        if key in metadata:
            metadata.pop(key)

    return metadata 