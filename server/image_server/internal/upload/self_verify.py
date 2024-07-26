import config
from internal.upload.hash import HashManager, get_all_hash_values, get_image_last_verification_status


HIGH_THRESHOLD = 0.95
LOW_THRESHOLD = 0.7


def hex_to_int(hex_str):
    return int(hex_str, 16)


def count_differing_bits(int1, int2):
    return bin(int1 ^ int2).count('1')


def compute_bitwise_difference(hex_str1, hex_str2):
    int1 = hex_to_int(hex_str1)
    int2 = hex_to_int(hex_str2)
    num_differing_bits = count_differing_bits(int1, int2)
    return num_differing_bits


def get_hash_similarity(hash1, hash2):
    try:
        difference = compute_bitwise_difference(hash1, hash2)
        similarity = 1 - difference / (4 * len(hash1))
        return similarity
    except:
        return 0.0


async def self_verify_image(filepath: str):
    hash_object = HashManager().get_hash_generator('pHash').compute_hash(filepath)
    hash_value = hash_object["value"]
    saved_hash_values = await get_all_hash_values()
    print(f"{len(saved_hash_values)} hash values retrieved from database.")
    ref_image_ids = []

    # first image
    if saved_hash_values is None:
        print("ACCEPTED")
        return config.VERIFICATION_STATUS["ACCEPTED"], hash_object, ref_image_ids
    
    # second image...
    for image_id, saved_hash_value in saved_hash_values:
        similarity = get_hash_similarity(hash_value, saved_hash_value)
        if similarity == 1 and await get_image_last_verification_status(image_id) == config.VERIFICATION_STATUS["REJECTED"]:
            print("REJECTED")
            return config.VERIFICATION_STATUS["REJECTED"], hash_object, ref_image_ids
        elif similarity >= HIGH_THRESHOLD:
            ref_image_ids.append(image_id)
            print("REJECTED")
            return config.VERIFICATION_STATUS["REJECTED"], hash_object, ref_image_ids
        elif similarity >= LOW_THRESHOLD:
            ref_image_ids.append(image_id)

    print(f"Ref image IDs: {ref_image_ids}")
    if len(ref_image_ids) == 0:
        print("ACCEPTED")
        return config.VERIFICATION_STATUS["ACCEPTED"], hash_object, ref_image_ids
    print("PENDING")
    return config.VERIFICATION_STATUS["PENDING"], hash_object, ref_image_ids