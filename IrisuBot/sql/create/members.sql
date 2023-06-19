CREATE TABLE "members" (
	"member_id"	INTEGER NOT NULL UNIQUE,
	"user_id"	INTEGER NOT NULL,
	"guild_id"	INTEGER NOT NULL,
	"member_nickname"	TEXT,
	"member_roles"	TEXT,
	"member_incidents"	INTEGER NOT NULL DEFAULT 0,
	"member_banned"	INTEGER NOT NULL DEFAULT 0,
	"member_whitelisted"	INTEGER NOT NULL DEFAULT 0,
	"member_blacklisted"	INTEGER NOT NULL DEFAULT 0,
	"member_admin"	INTEGER NOT NULL DEFAULT 0,
	"member_moderator"	INTEGER NOT NULL DEFAULT 0,
	"member_developer"	INTEGER NOT NULL DEFAULT 0,
	FOREIGN KEY("user_id") REFERENCES "users"("user_id"),
	FOREIGN KEY("guild_id") REFERENCES "guilds"("guild_id"),
	PRIMARY KEY("member_id" AUTOINCREMENT)
)