from mytypes.CryptoHashGenerator import CryptoHashGenerator

class HashGeneratorFactory:
    @staticmethod
    def create_hash_generator(algorithm_name):
        return CryptoHashGenerator(algorithm_name)


factory = HashGeneratorFactory()
crypto_hash_gen = factory.create_hash_generator('sha256')

def get_crypto_hash_algorithm():
    return crypto_hash_gen.get_hash_algorithm()
