from cryptography.hazmat.primitives import hashes

class HashGenerator:
    def get_hash_algorithm(self):
        raise NotImplementedError("Subclasses should implement this method")
