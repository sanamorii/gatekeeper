CREATE TABLE "users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"user_name"	TEXT NOT NULL,
	"user_mcname"	TEXT,
	"user_mcuuid"	TEXT,
	PRIMARY KEY("user_id")
)