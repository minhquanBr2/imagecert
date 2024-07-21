import requests
import config


async def get_user_uid_from_image_id(image_id: int) -> str:
    url = f"{config.DB_ENDPOINT_URL}/select/image/{image_id}/user_uid"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    results = response.json()["message"]
    return results