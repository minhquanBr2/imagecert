from PIL import Image
import pillow_heif


def extract_metadata(filepath):        
    
    pillow_heif.register_heif_opener() 
    metadata = {}

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