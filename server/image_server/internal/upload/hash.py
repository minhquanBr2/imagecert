from abc import abstractmethod
from PIL import Image
import imagehash
import pillow_heif
import config
import requests


pillow_heif.register_heif_opener()                  # Register HEIF plugin to allow Pillow to open HEIC files


class HashManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HashManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "hash_generators"):
            self.hash_generators = {
                'aHash': AverageHashGenerator(),
                'dHash': DifferentHashGenerator(),
                'pHash': PerceptualHashGenerator()
            }

    def register_hash_generator(self, hash_type, hash_generator):
        if hash_type not in self.hash_generators.keys():
            self.hash_generators[hash_type] = hash_generator

    def get_hash_generator(self, hash_type):
        generator = self.hash_generators.get(hash_type)
        if not generator:
            raise ValueError(f"No hash generator registered for type: {hash_type}")
        return generator     


class HashGenerator():
    def __init__(self, hash_type):
        self.hash_type = hash_type

    @abstractmethod
    def compute_hash(self, filepath):
        pass


class AverageHashGenerator(HashGenerator):
    def __init__(self):
        super().__init__("aHash")

    @staticmethod
    def compute_hash(filepath):
        try: 
            hash_object = imagehash.average_hash(Image.open(filepath))
            print(f"Computed average hash: {hash_object}")
            return {
                "type": "aHash",
                "value": str(hash_object)
            }
        except:
            return None


class DifferentHashGenerator(HashGenerator):
    def __init__(self):
        super().__init__("dHash")

    @staticmethod
    def compute_hash(filepath):
        try: 
            hash_object = imagehash.dhash(Image.open(filepath))
            print(f"Computed different hash: {hash_object}")
            return {
                "type": "dHash",
                "value": str(hash_object)
            }
        except:
            return None
        

class PerceptualHashGenerator(HashGenerator):
    def __init__(self):
        super().__init__("pHash")

    @staticmethod
    def compute_hash(filepath):
        try: 
            hash_object = imagehash.phash(Image.open(filepath))
            print(f"Computed pHash: {hash_object}")
            return {
                "type": "pHash",
                "value": str(hash_object)
            }
        except:
            return None


async def get_all_accepted_hash_values():
    url = f"{config.DB_ENDPOINT_URL}/select/all_accepted_hashes"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()["result"]
        return results
    else:
        return []


async def get_image_last_verification_status(image_id):
    url = f"{config.DB_ENDPOINT_URL}/last_verification_status/{image_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["message"]
    return None
    

if __name__ == "__main__":
    HashManager().get_hash_generator("aHash").compute_hash("romania.jpg")
    HashManager().get_hash_generator("dHash").compute_hash("romania.jpg")
    HashManager().get_hash_generator("pHash").compute_hash("romania.jpg")