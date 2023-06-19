import aiomcrcon
import asyncio


async def connectToServer():
    command = "list"
    
    client = aiomcrcon.Client("140.238.96.2", 25575, "35Vnu96Hr3C9Yw5")
    try: await client.connect()
    except aiomcrcon.RCONConnectionError: print("no server")
    
    else:
        response = await client.send_cmd("list")
        print(response)
        await client.close()

asyncio.run(connectToServer())
        