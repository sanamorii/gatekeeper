import aiomcrcon
import asyncio
import json
import re
import exceptions

from patterns import Singleton

class RCONClient(object, metaclass=Singleton):
    
    def __init__(self) -> None:
        with open("./config.json", "r") as f:
            config_data = json.load(f)
            self.port = config_data["rcon_port"]
            self.host = config_data["host_ip"]
            self.password = config_data["rcon_password"]
        self.client = aiomcrcon.Client(self.host, self.port, self.password)
        self.connected : bool = False
        
    async def __aenter__(self, *args, **kwargs):
        try:
            await self.client.connect()
        except aiomcrcon.RCONConnectionError:
            raise aiomcrcon.RCONConnectionError
        else:
            self.connected = False
        
        return self
    
    async def __aexit__(self, *args, **kwargs):
         if self.connected: self.client.close()
    
    async def whitelistAdd(self, username: str) -> None:
        '''add to whitelist'''
        cmd = f"whitelist add {username}"
        response = await self.client.send_cmd(cmd=cmd)
        response = self.clean(response[0])
        
        if response.lower() == "player is already whitelisted":
            raise exceptions.PlayerAlreadyExists(username=username)
        elif response.lower() == "that player does not exist":
            raise exceptions.PlayerDoesNotExist(username=username)
        
    async def getPlayers(self):
        response = await self.client.send_cmd(cmd="list")
        return response
    
    @staticmethod
    def clean(text: str):
        return re.sub(r"(\xA7[0-9a-fk-orA-FK-OR])", "", text)