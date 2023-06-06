import requests
import json

class MojangAPI:
    @staticmethod
    def usernameToUUID(username) -> dict:
        response = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}")
        try: response.raise_for_status
        except requests.HTTPError as e:
            print("usernameToUUID failed - httperror")
            raise e
            
        content = json.loads(response.content)
        if content.get("errorMessage") is None:
            raise Exception
        else:
            return content