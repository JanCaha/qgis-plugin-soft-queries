CREATE TABLE "fuzzy_variables" (
	"variable_name"	TEXT NOT NULL UNIQUE,
	"python_object"	TEXT,
	PRIMARY KEY("variable_name")
);