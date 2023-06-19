# from integration.rcon import RCONClient
# import asyncio

# async def main():
#     async with RCONClient() as client:
#         await client.whitelistAdd("asfahwrge")
            
# asyncio.run(main())


from database import SQLiteDatabase

db = SQLiteDatabase("./database.db")

print(db.isMember(1324135))