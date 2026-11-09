#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path
from urllib.parse import urlparse

import yt_dlp
from colorama import init, Fore, Style

init(autoreset=True)

VERDE = Fore.GREEN
NEON = Fore.LIGHTGREEN_EX
BRANCO = Fore.WHITE
VERMELHO = Fore.LIGHTRED_EX
AMARELO = Fore.YELLOW
CIANO = Fore.CYAN

DOWNLOAD_DIR = (
    Path.home() / "storage" / "downloads" / "JS-LINKS-VIDEOS"
)

BANNER = r"""
       ██╗███████╗
       ██║██╔════╝
       ██║███████╗
  ██   ██║╚════██║
  ╚█████╔╝███████║
   ╚════╝ ╚══════╝

      JS LINKS VIDEOS
       HACKER TERMINAL
"""


def preparar_pasta():
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)


def banner():
    os.system("clear")

    print(NEON + BANNER)
    print(VERDE + "╔══════════════════════════════════════╗")
    print(VERDE + "║" + BRANCO + "        VIDEO DOWNLOADER PRO          " + VERDE + "║")
    print(VERDE + "╚══════════════════════════════════════╝")

    print(NEON + "\n  [01] ▶  BAIXAR VÍDEO")
    print(NEON + "  [02] ▣  MEUS DOWNLOADS")
    print(NEON + "  [03] ↻  ATUALIZAR FERRAMENTA")
    print(NEON + "  [04] ▤  PASTA DE DOWNLOADS")
    print(NEON + "  [05] ✖  SAIR")

    print(VERDE + "\n  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(NEON + "  ● SYSTEM STATUS: " + BRANCO + "ONLINE")
    print(NEON + "  ● DOWNLOAD ENGINE: " + BRANCO + "YT-DLP")
    print(VERDE + "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


def validar_link(url):
    try:
        dados = urlparse(url)
        return (
            dados.scheme in ("http", "https")
            and bool(dados.netloc)
        )
    except Exception:
        return False


def barra_progresso(dados):
    status = dados.get("status")

    if status == "downloading":
        total = dados.get("total_bytes") or dados.get("total_bytes_estimate")
        baixado = dados.get("downloaded_bytes", 0)

        if total:
            porcentagem = min(100, baixado / total * 100)
            preenchido = int(porcentagem / 4)
            barra = "█" * preenchido + "░" * (25 - preenchido)

            velocidade = dados.get("_speed_str", "calculando...")
            tamanho = dados.get("_total_bytes_str", "calculando...")

            print(
                f"\r{NEON}[{barra}] {porcentagem:5.1f}% "
                f"{VERDE}{baixado / total * 100:.0f}% "
                f"{BRANCO}| {velocidade} | {tamanho}",
                end="",
                flush=True
            )
        else:
            print(
                f"\r{NEON}Baixando... {BRANCO}"
                + dados.get("_percent_str", ""),
                end="",
                flush=True
            )

    elif status == "finished":
        print("\n\n" + NEON + "[+] Download recebido. Finalizando arquivo...")


def baixar_video(url):
    preparar_pasta()

    opcoes = {
        "format": "best[ext=mp4]/best",
        "outtmpl": str(DOWNLOAD_DIR / "%(title).100s.%(ext)s"),
        "noplaylist": True,
        "retries": 5,
        "fragment_retries": 5,
        "continuedl": True,
        "overwrites": False,
        "socket_timeout": 30,
        "progress_hooks": [barra_progresso],
    }

    try:
        print(NEON + "\n[+] Preparando download...")
        print(NEON + "[+] Salvando no celular...\n")

        with yt_dlp.YoutubeDL(opcoes) as downloader:
            resultado = downloader.download([url])

        if resultado == 0:
            print(NEON + "\n[OK] DOWNLOAD CONCLUÍDO!")
            print(VERDE + f"[PASTA] {DOWNLOAD_DIR}")
        else:
            print(VERMELHO + "\n[ERRO] Download não concluído.")

    except KeyboardInterrupt:
        print(AMARELO + "\n[!] Download interrompido.")

    except Exception as erro:
        print(VERMELHO + f"\n[ERRO] {erro}")


def listar_downloads():
    preparar_pasta()

    extensoes = (
        ".mp4", ".mkv", ".webm", ".mov",
        ".avi", ".m4v", ".mp3", ".m4a"
    )

    arquivos = sorted(
        arquivo for arquivo in DOWNLOAD_DIR.iterdir()
        if arquivo.is_file()
        and arquivo.suffix.lower() in extensoes
    )

    print(NEON + "\n╔══════════ MEUS DOWNLOADS ══════════╗\n")

    if not arquivos:
        print(AMARELO + "[!] Nenhum arquivo encontrado.")
    else:
        for numero, arquivo in enumerate(arquivos, start=1):
            tamanho = arquivo.stat().st_size / (1024 * 1024)
            print(NEON + f"[{numero:02}] " + BRANCO + arquivo.name)
            print(VERDE + f"     Tamanho: {tamanho:.2f} MB\n")

    print(VERDE + f"[PASTA] {DOWNLOAD_DIR}")


def atualizar_ferramenta():
    print(NEON + "\n[+] Atualizando yt-dlp...\n")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"],
            check=True
        )
        print(NEON + "\n[OK] Atualização concluída!")

    except subprocess.CalledProcessError:
        print(VERMELHO + "\n[ERRO] Não foi possível atualizar.")

    except Exception as erro:
        print(VERMELHO + f"\n[ERRO] {erro}")


def menu():
    preparar_pasta()

    while True:
        banner()

        opcao = input(NEON + "\nJS-LINKS@TERMUX:~$ " + BRANCO).strip()

        if opcao == "1":
            url = input(NEON + "\n[+] Cole o link: " + BRANCO).strip()

            if validar_link(url):
                baixar_video(url)
            else:
                print(VERMELHO + "\n[ERRO] Link inválido.")

            input(AMARELO + "\nPressione ENTER para continuar...")

        elif opcao == "2":
            listar_downloads()
            input(AMARELO + "\nPressione ENTER para continuar...")

        elif opcao == "3":
            atualizar_ferramenta()
            input(AMARELO + "\nPressione ENTER para continuar...")

        elif opcao == "4":
            print(NEON + "\n[PASTA DE DOWNLOADS]")
            print(BRANCO + str(DOWNLOAD_DIR))
            input(AMARELO + "\nPressione ENTER para continuar...")

        elif opcao == "5":
            print(NEON + "\n[+] JS LINKS VIDEOS ENCERRADO.")
            sys.exit(0)

        else:
            print(VERMELHO + "\n[!] Opção inválida.")
            input(AMARELO + "\nPressione ENTER para continuar...")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print(AMARELO + "\n\n[+] JS LINKS VIDEOS encerrado.")
        sys.exit(0)
