.PHONY: zip

prepare: clean

zip: clean download replace_db zipfiles

replace_db:
	rm database/plugin.db
	cp database/empty_backup.db database/plugin.db

clean:
	py3clean .

download: 
	./scripts/get_deps.sh

zipfiles:
	pb_tool zip