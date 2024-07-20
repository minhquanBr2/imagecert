import config
from internal.upload.hash import compute_perceptual_hash


HIGH_THRESHOLD = 0.95
LOW_THRESHOLD = 0.7


# TODO: design similarity metrics
def get_hash_similarity(hash1, hash2):
    return 0.72


def self_verify_image(filepath: str):
    hash_object = compute_perceptual_hash(filepath)
    hash_value = hash_object["value"]
    # TODO: get all hash in db, can we optimize this to not iterating? Can we let multiple images vote? 
    saved_hashes = ["abc"]    
    dummy_ref_filepath = "http://104.154.115.168:8001/image/29d5076702c4444e671797f3e95160c874f72f539f14fb88ac73a5a3eeb80a37.webp"
    for hash in saved_hashes:
        similarity = get_hash_similarity(hash_value, hash)
        if similarity >= HIGH_THRESHOLD:
            return config.VERIFICATION_STATUS["REJECTED"], hash_object, dummy_ref_filepath
        elif similarity >= LOW_THRESHOLD:
            return config.VERIFICATION_STATUS["PENDING"], hash_object, dummy_ref_filepath
    return config.VERIFICATION_STATUS["ACCEPTED"], hash_object, dummy_ref_filepath