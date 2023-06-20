import requests
import json
import exceptions

def usernameToUUID(username) -> dict:
    """content:dict = {
        "name" : "xxx",
        "id" : "xxx"
        }
    """
    response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
    try: response.raise_for_status
    except requests.HTTPError as e:
        print("usernameToUUID failed - httperror")
        raise e
        
    content = json.loads(response.content)
    if content.get("errorMessage"):
        raise exceptions.PlayerDoesNotExist(username)
    else:
        return content