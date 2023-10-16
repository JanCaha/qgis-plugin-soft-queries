.PHONY: zip

prepare: clean

zip: clean download replace_db zipfiles

replace_db:
	rm database/plugin.db
	cp database/empty_backup.db database/plugin.db

clean:
	py3clean .

download: 
	rm -rf deps
	TAG=$(curl -sL https://api.github.com/repos/JanCaha/FuzzyMath/releases/latest | jq -r ".tag_name")
	VERSION=$(echo $TAG | cut -c2-)
	wget https://github.com/JanCaha/FuzzyMath/releases/download/$TAG/FuzzyMath-$VERSION-py3-none-any.whl -P deps

zipfiles:
	pb_tool zip