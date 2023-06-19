# Irisu
Minecraft whitelisting bot for discord.  

- `IrisuBot` is the discord bot.
- `IrisuHook` is the server plugin to integrate the bot.

IrisuBot requires a `config.json` file to be made in `IrisuBot/`.
```json
{
    "application_id": DISCORD_APPLICATION_ID,
    "token": "DISCORD_BOT_TOKEN",
    "host_ip": "MINECRAFT_SERVER_IP",
    "host_port": MINECRAFT_PORT,
    "rcon_port": RCON_PORT,
    "rcon_password": "RCON_PASSWORD"
}
```

TODO:
- [ ] look into mongodb