from PIL import Image
import imagehash
import pillow_heif
import config
import requests


pillow_heif.register_heif_opener()                  # Register HEIF plugin to allow Pillow to open HEIC files


def compute_perceptual_hash(filepath):
    try: 
        hash_object = imagehash.phash(Image.open(filepath))
        print(f"Computed pHash: {hash_object}")
        return {
            "type": "pHash",
            "value": str(hash_object)
        }
    except:
        return None


async def get_all_hash_values():
    url = f"{config.DB_ENDPOINT_URL}/select/all_hashes"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["message"]
    return None
    