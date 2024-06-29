from PIL import Image
import imagehash

def compute_perceptual_hash(filename):

    try: 
        filepath = filename             # change this if change file location
        hash = imagehash.phash(Image.open(filepath))
        return str(hash)
    except:
        return None