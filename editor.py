#!/usr/bin/env python3

import subprocess
import shutil
from pathlib import Path
import math

DOWNLOAD_DIR = Path.home() / "storage" / "downloads" / "JS-LINKS-VIDEOS"
EDIT_DIR = DOWNLOAD_DIR / "EDITADOS"
CAMERA_DIR = Path.home() / "storage" / "dcim" / "Camera"

VERDE = "\033[92m"
CIANO = "\033[96m"
AMARELO = "\033[93m"
RESET = "\033[0m"


def preparar_pastas():
    EDIT_DIR.mkdir(parents=True, exist_ok=True)
    CAMERA_DIR.mkdir(parents=True, exist_ok=True)


def publicar_na_galeria(arquivo):
    nome = arquivo.name
    if nome.startswith(".trashed-"):
        nome = "JS_" + nome[len(".trashed-"):]
    destino = CAMERA_DIR / nome
    shutil.copy2(arquivo, destino)

    try:
        subprocess.run(
            ["termux-media-scan", str(destino)],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except OSError:
        pass

    print(VERDE + f"[GALERIA] {destino}")

def duracao_video(arquivo):
    resultado = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(arquivo)
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return float(resultado.stdout.strip())


def dividir_video(arquivo):
    preparar_pastas()

    arquivo = Path(arquivo)
    duracao = duracao_video(arquivo)

    if duracao <= 0:
        raise ValueError("Duração de vídeo inválida.")

    nome = arquivo.stem
    saida = EDIT_DIR / f"{nome}_parte_%02d.mp4"

    print(VERDE + "\\n[+] Dividindo vídeo em partes de até 55 segundos...\\n")

    comando = [
        "ffmpeg", "-y",
        "-i", str(arquivo),
        "-map", "0:v:0",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "20",
        "-force_key_frames", "expr:gte(t,n_forced*55)",
        "-c:a", "aac",
        "-b:a", "192k",
        "-f", "segment",
        "-segment_time", "55",
        "-segment_start_number", "1",
        "-reset_timestamps", "1",
        "-segment_format", "mp4",
        str(saida)
    ]

    subprocess.run(comando, check=True)

    partes = sorted(EDIT_DIR.glob(f"{nome}_parte_*.mp4"))

    if not partes:
        raise RuntimeError("Nenhuma parte foi criada.")

    for numero, parte in enumerate(partes, 1):
        publicar_na_galeria(parte)
        print(VERDE + f"[OK] Parte {numero}: {parte.name}")

    print(CIANO + "\\n[OK] DIVISÃO CONCLUÍDA!")
    print(VERDE + f"[TOTAL] {len(partes)} partes")
    print(VERDE + f"[PASTA] {EDIT_DIR}")


def cortes_automaticos(arquivo):
    preparar_pastas()

    arquivo = Path(arquivo)
    duracao = duracao_video(arquivo)

    if duracao <= 0:
        raise ValueError("Duração de vídeo inválida.")

    tempo_total = min(55.0, duracao)
    quantidade_trechos = min(8, max(1, math.ceil(duracao / 55)))
    intervalo = duracao / quantidade_trechos
    tempo_trecho = tempo_total / quantidade_trechos

    nome = arquivo.stem
    lista = EDIT_DIR / f"{nome}_lista.txt"
    saida = EDIT_DIR / f"{nome}_cortes_automaticos.mp4"

    caminho = str(arquivo.resolve())
    caminho = caminho.replace("\\", "\\\\").replace("'", "'\\''")

    trechos = []

    for numero in range(quantidade_trechos):
        inicio = numero * intervalo
        fim = min(duracao, inicio + tempo_trecho)

        trechos.append(
            f"file '{caminho}'\n"
            f"inpoint {inicio:.6f}\n"
            f"outpoint {fim:.6f}\n"
        )

    lista.write_text("".join(trechos), encoding="utf-8")

    comando = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(lista),
        "-map", "0:v:0",
        "-map", "0:a?",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", str(tempo_total),
        "-movflags", "+faststart",
        str(saida)
    ]

    try:
        subprocess.run(comando, check=True)
        publicar_na_galeria(saida)
        print(VERDE + "\n[OK] CORTES AUTOMÁTICOS CONCLUÍDOS!")
        print(CIANO + f"[ARQUIVO] {saida}")
    finally:
        lista.unlink(missing_ok=True)


def escolher_video():
    preparar_pastas()

    extensoes = (".mp4", ".mkv", ".webm", ".mov", ".avi")

    pastas = [
        ("Downloads do JS LINKS VIDEOS", DOWNLOAD_DIR),
        ("Câmera do celular", Path.home() / "storage/dcim/Camera"),
        ("Downloads do Android", Path.home() / "storage/downloads"),
        ("Vídeos do celular", Path.home() / "storage/movies"),
    ]

    arquivos = []
    encontrados = set()

    for nome_pasta, pasta in pastas:
        try:
            for video in pasta.iterdir():
                if (
                    video.is_file()
                    and video.suffix.lower() in extensoes
                ):
                    caminho = video.resolve()

                    if caminho not in encontrados:
                        encontrados.add(caminho)
                        arquivos.append(video)
        except (OSError, FileNotFoundError):
            continue

    if not arquivos:
        print(AMARELO + "\\n[!] Nenhum vídeo encontrado.")
        return None

    print(CIANO + "\\n====== VÍDEOS DISPONÍVEIS ======\\n")

    for numero, video in enumerate(arquivos, 1):
        print(f"[{numero:02d}] {video.name}")
        print(f"     Pasta: {video.parent}")

    escolha = input(AMARELO + "\\nNúmero do vídeo: ").strip()

    if not escolha.isdigit():
        print(AMARELO + "[!] Opção inválida.")
        return None

    numero = int(escolha)

    if not 1 <= numero <= len(arquivos):
        print(AMARELO + "[!] Número fora da lista.")
        return None

    return arquivos[numero - 1]

def menu_editor():
    while True:
        preparar_pastas()

        print(VERDE + "\n╔══════════════════════════════════════╗")
        print(VERDE + "║           JS VIDEO EDITOR            ║")
        print(VERDE + "╚══════════════════════════════════════╝")

        print(CIANO + "\n[01] ✂ DIVIDIR EM PARTES DE 55 SEGUNDOS")
        print(CIANO + "[02] ⚡ CORTES AUTOMÁTICOS EM 55 SEGUNDOS")
        print(CIANO + "[03] ↩ VOLTAR")

        opcao = input(AMARELO + "\nJS-EDITOR@TERMUX:~$ ").strip()

        if opcao in ("1", "2"):
            arquivo = escolher_video()

            if arquivo and arquivo.is_file():
                try:
                    if opcao == "1":
                        dividir_video(arquivo)
                    else:
                        cortes_automaticos(arquivo)
                except Exception as erro:
                    print(AMARELO + f"\n[ERRO] {erro}")

            input(AMARELO + "\nPressione ENTER para continuar...")

        elif opcao == "3":
            break


if __name__ == "__main__":
    menu_editor()
