CREATE TABLE "guilds" (
	"guild_id"	INTEGER NOT NULL UNIQUE,
	"guild_name"	TEXT NOT NULL,
	"guild_prefix"	TEXT NOT NULL DEFAULT '!',
	"guild_consolechannel"	INTEGER,
	"guild_relaychannel"	INTEGER,
	"guild_adminrole"	INTEGER,
	"guild_modrole"	INTEGER,
	"guild_devrole"	INTEGER,
	PRIMARY KEY("guild_id")
)