rm -rf deps
TAG=$(curl -sL https://api.github.com/repos/JanCaha/FuzzyMath/releases/latest | jq -r ".tag_name")
VERSION=$(echo $TAG | cut -c2-)
wget https://github.com/JanCaha/FuzzyMath/releases/download/$TAG/FuzzyMath-$VERSION-py3-none-any.whl -P deps