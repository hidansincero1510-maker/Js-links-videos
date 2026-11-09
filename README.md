🚀 JS LINKS VIDEOS

Ferramenta de download de vídeos para Termux com interface Hacker Green.

📥 1. Instalação automática (recomendada)

Copie e cole este comando inteiro no Termux:

pkg install curl -y && curl -fsSL https://raw.githubusercontent.com/hidansincero1510-maker/Js-links-videos/main/install.sh | bash

🛠️ 2. Instalação manual

Passo 1 — Entrar na pasta da ferramenta

cd ~/Js-links-videos

Passo 2 — Instalar o Python

pkg install python -y

Passo 3 — Instalar o yt-dlp

python -m pip install -U yt-dlp

Passo 4 — Configurar o armazenamento

termux-setup-storage

Aceite a permissão de acesso aos arquivos no Android.

Passo 5 — Iniciar o JS LINKS VIDEOS

python jslinks.py

🔄 3. Atualização

Passo 1 — Entrar na pasta

cd ~/Js-links-videos

Passo 2 — Atualizar o yt-dlp

python -m pip install -U yt-dlp

📂 4. Pasta dos downloads

Os vídeos são salvos em:

~/storage/downloads/JS-LINKS-VIDEOS

✨ 5. Recursos

- Download de vídeos por link.
- Interface Hacker Green.
- Barra de progresso.
- Lista de downloads.
- Atualização do yt-dlp.
- Salvamento no armazenamento do Android.

Desenvolvido por: JS LINKS VIDEOS 💚

---

## 🔄 6. REINSTALAÇÃO APÓS DESINSTALAR O TERMUX

Se você desinstalar o Termux e instalar novamente, siga os passos abaixo para recuperar o JS LINKS VIDEOS.

### Passo 1 — Atualizar o Termux

```bash
pkg update && pkg upgrade -y
pkg install python git ffmpeg nodejs termux-api -y
git clone https://github.com/hidansincero1510-maker/Js-links-videos.git
cd ~/Js-links-videos
pip install -r requirements.txt
pip install colorama
termux-setup-storage
python jslinks.py
```

### IMPORTANTE

- Instale também o aplicativo Termux:API no Android para usar a publicação de vídeos na galeria.
- Os vídeos que estavam no armazenamento do aparelho precisam de backup separado.
- O GitHub guarda o código-fonte da ferramenta, não os vídeos baixados.

💚 JS LINKS VIDEOS — Projeto recuperável pelo GitHub!
