from mytypes.HashGenerator import HashGenerator
from cryptography.hazmat.primitives import hashes

class CryptoHashGenerator(HashGenerator):
    def __init__(self, algorithm_name):
        self.algorithm_name = algorithm_name

    def get_hash_algorithm(self):
        if self.algorithm_name.lower() == 'sha256':
            return hashes.SHA256()
        elif self.algorithm_name.lower() == 'sha512':
            return hashes.SHA512()
        
        else:
            raise ValueError(f"Unsupported hash algorithm: {self.algorithm_name}")
