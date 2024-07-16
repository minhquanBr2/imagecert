import config
import numpy as np
from internal.upload.hash import compute_perceptual_hash


HIGH_THRESHOLD = 0.95
LOW_THRESHOLD = 0.7


# TODO: design similarity metrics
def get_hash_similarity(hash1, hash2):
    return 0.3

def self_verify_image(filepath: str):
    hash_object = compute_perceptual_hash(filepath)
    hash_value = hash_object["value"]
    # TODO: get all hash in db, can we optimize this to not iterating? Can we let multiple images vote? 
    saved_hashes = ["abc"]
    for hash in saved_hashes:
        similarity = get_hash_similarity(hash_value, hash)
        if similarity >= HIGH_THRESHOLD:
            ref_filepath = "dummy.jpg"
            return config.VERIFICATION_STATUS["REJECTED"], hash_object, ref_filepath
        elif similarity >=LOW_THRESHOLD:
            return config.VERIFICATION_STATUS["PENDING"], hash_object, ""
    return config.VERIFICATION_STATUS["PENDING"], hash_object, ""