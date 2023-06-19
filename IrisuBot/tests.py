from integration.rcon import RCONClient
import asyncio

async def main():
    async with RCONClient() as client:
        await client.whitelistAdd("asfageqwfasfasfawr")
            
asyncio.run(main())
