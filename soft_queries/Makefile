.PHONY: zip

prepare: clean

zip: clean replace_db zipfiles

replace_db:
	rm database/plugin.db
	cp database/empty_backup.db database/plugin.db

clean:
	py3clean .

zipfiles:
	pb_tool zip