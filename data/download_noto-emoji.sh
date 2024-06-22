VERSION=2.042
curl -L --compressed https://github.com/googlefonts/noto-emoji/archive/refs/tags/v$VERSION.tar.gz -o noto-emoji.tar.gz
tar -xzf noto-emoji.tar.gz noto-emoji-$VERSION/png/512
mv noto-emoji-$VERSION/png/512 noto-emoji
rm -rf noto-emoji-$VERSION
rm noto-emoji.tar.gz
