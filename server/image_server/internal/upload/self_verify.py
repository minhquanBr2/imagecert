import config
from internal.upload.hash import compute_perceptual_hash


HIGH_THRESHOLD = 0.95
LOW_THRESHOLD = 0.7


# TODO: design similarity metrics
def get_hash_similarity(hash1, hash2):
    # difference = hash1 - hash2
    # similarity = 1 - difference / len(hash1)
    # return similarity
    return 0.72


def self_verify_image(filepath: str):
    hash_object = compute_perceptual_hash(filepath)
    hash_value = hash_object["value"]
    # TODO: get all hash in db, can we optimize this to not iterating? Can we let multiple images vote? 
    saved_hashes = ["abc"]    
    # return ref_image_ids as a list of image ids (actually a list of 2 random numbers between 1 and 10)
    ref_image_ids = [1, 2]
    for hash in saved_hashes:
        similarity = get_hash_similarity(hash_value, hash)
        if similarity >= HIGH_THRESHOLD:
            return config.VERIFICATION_STATUS["REJECTED"], hash_object, ref_image_ids
        elif similarity >= LOW_THRESHOLD:
            return config.VERIFICATION_STATUS["PENDING"], hash_object, ref_image_ids
    return config.VERIFICATION_STATUS["ACCEPTED"], hash_object, []