import requests
import json

from exceptions import InvalidMinecraftUsername

class MojangAPI:
    
    @staticmethod
    def usernameToUUID(username) -> dict:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        try: response.raise_for_status
        except requests.HTTPError as e:
            print("usernameToUUID failed - httperror")
            raise e
            
        content = json.loads(response.content)
        if content.get("errorMessage") is not None:
            raise InvalidMinecraftUsername(f"{username} is not valid.")
        else:
            return content