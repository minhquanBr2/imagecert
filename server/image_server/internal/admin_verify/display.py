import config
import requests


async def get_pending_images():
    url = f"{config.DB_ENDPOINT_URL}/select/pending_images"
    response = requests.get(url)
    if response.status_code != 200:
        return {"message": f"Internal server error with status code {response.status_code}."}

    results = response.json()["message"]
    if len(results) == 0:
        return {"message": "No pending images found."}

    return results


async def get_all_images():
    url = f"{config.DB_ENDPOINT_URL}/select/all_images"
    response = requests.get(url)
    if response.status_code != 200:
        return {"message": f"Internal server error with status code {response.status_code}."}

    results = response.json()["message"]
    if len(results) == 0:
        return {"message": "No images found."}

    return results


async def get_verification_history(admin_uid: str):
    url = f"{config.DB_ENDPOINT_URL}/select/verification_history/{admin_uid}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"message": f"Internal server error with status code {response.status_code}."}

    results = response.json()["message"]
    if len(results) == 0:
        return {"message": "No verification history found."}

    return results

    