#!/data/data/com.termux/files/usr/bin/bash

set -e

echo "================================"
echo "      JS LINKS VIDEOS"
echo "      INSTALADOR"
echo "================================"

if [ -z "$PREFIX" ]; then
    echo "Erro: execute este instalador no Termux."
    exit 1
fi

pkg update -y
pkg install python git ffmpeg nodejs termux-api -y

termux-setup-storage

if [ -d "$HOME/Js-links-videos/.git" ]; then
    git -C "$HOME/Js-links-videos" pull --ff-only
else
    git clone https://github.com/hidansincero1510-maker/Js-links-videos.git "$HOME/Js-links-videos"
fi

cd "$HOME/Js-links-videos"

python -m pip install -r requirements.txt

python jslinks.py
