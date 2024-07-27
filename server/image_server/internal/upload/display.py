import config
import requests

async def get_all_images():
    url = f"{config.DB_ENDPOINT_URL}/select/all_images"
    response = requests.get(url)
    if response.status_code != 200:
        return {"message": f"Internal server error with status code {response.status_code}."}

    results = response.json()["message"]
    if len(results) == 0:
        return {"message": "No images found."}

    return results
