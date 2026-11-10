#!/usr/bin/env python3
# WIFI TRACKER — safe Wi-Fi visibility and local password-strength checker.
# Does NOT guess, crack, or attempt passwords against nearby networks.

import json
import os
import re
import shutil
import subprocess
import sys
import webbrowser

YOUTUBE_URL = "https://youtube.com/@calzxchannel?si=llet1yqiVZe_139f"

C = {
    "cyan": "\033[96m", "blue": "\033[94m", "green": "\033[92m",
    "yellow": "\033[93m", "red": "\033[91m", "purple": "\033[95m",
    "white": "\033[97m", "dim": "\033[2m", "reset": "\033[0m",
    "bold": "\033[1m"
}

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def neon(text):
    return C["bold"] + C["cyan"] + text + C["reset"]

def banner():
    clear()
    print(C["cyan"] + C["bold"])
    print("██╗    ██╗██╗███████╗██╗")
    print("██║    ██║██║██╔════╝██║")
    print("██║ █╗ ██║██║█████╗  ██║")
    print("██║███╗██║██║██╔══╝  ██║")
    print("╚███╔███╔╝██║██║     ██║")
    print(" ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝")
    print(C["white"] + C["bold"] + "             TRACKER" + C["reset"])
    print(C["dim"] + "      TERMUX WI-FI TOOLKIT" + C["reset"])
    print(C["blue"] + "═" * 43 + C["reset"])

def pause():
    input("\nTekan ENTER untuk kembali...")


def scan_wifi():
    import json
    import shutil
    import subprocess
    import time

    banner()
    print(CYAN + "[ WIFI SCANNER ]" + RESET)

    # Periksa Termux:API
    if not shutil.which("termux-wifi-scaninfo"):
        print(RED + "[ERROR] Termux:API belum tersedia." + RESET)
        pause()
        return

    # Picu permintaan izin lokasi Android
    if not shutil.which("termux-location"):
        print(RED + "[ERROR] termux-location tidak ditemukan." + RESET)
        pause()
        return

    print(YELLOW + "[INFO] Memeriksa izin lokasi..." + RESET)

    try:
        permission = subprocess.run(
            ["termux-location", "-p", "network", "-r", "once"],
            capture_output=True,
            text=True,
            timeout=25
        )

        if permission.returncode != 0:
            print(RED + "[ERROR] Izin lokasi belum tersedia." + RESET)
            print("Buka pengaturan Termux:API dan izinkan Location.")
            subprocess.run([
                "am", "start", "-a",
                "android.settings.APPLICATION_DETAILS_SETTINGS",
                "-d", "package:com.termux.api"
            ])
            pause()
            return

    except subprocess.TimeoutExpired:
        print(RED + "[ERROR] Pemeriksaan izin melewati batas waktu." + RESET)
        pause()
        return

    print(GREEN + "[OK] Pemeriksaan izin selesai." + RESET)
    print(YELLOW + "[INFO] Membaca hasil scan WiFi..." + RESET)

    try:
        result = subprocess.run(
            ["termux-wifi-scaninfo"],
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0:
            print(RED + "[ERROR] Gagal membaca hasil WiFi." + RESET)
            print(result.stderr)
            pause()
            return

        networks = json.loads(result.stdout or "[]")

        unique = {}
        for item in networks:
            ssid = (item.get("ssid") or "").strip()
            if ssid:
                unique[ssid] = item

        networks = sorted(
            unique.values(),
            key=lambda x: x.get("level", -999),
            reverse=True
        )

        if not networks:
            print(YELLOW + "[INFO] Belum ada hasil scan WiFi." + RESET)
            print("Buka pengaturan WiFi Android, tunggu pemindaian selesai,")
            print("kemudian kembali ke WIFI TRACKER dan scan lagi.")
            pause()
            return

        print(GREEN + "\nWIFI TERDETEKSI:\n" + RESET)

        for i, wifi in enumerate(networks, 1):
            print(
                f"{CYAN}[{i}]{RESET} "
                f"{WHITE}{wifi['ssid']}{RESET}"
            )
            print(
                f"Signal: {wifi.get('level', '?')} dBm"
            )

        choice = input("\nPilih nomor WiFi (0 kembali): ").strip()

        if choice == "0":
            return

        if not choice.isdigit() or not 1 <= int(choice) <= len(networks):
            print(RED + "Pilihan tidak valid." + RESET)
            pause()
            return

        ssid = networks[int(choice) - 1]["ssid"]

        print(f"\nWiFi dipilih: {GREEN}{ssid}{RESET}")

        confirm = input(
            "Lanjutkan pemeriksaan password lokal? (ya/tidak): "
        ).lower()

        if confirm in ("ya", "y"):
            password_check(ssid)
        else:
            print(YELLOW + "[STOPPED] Dibatalkan." + RESET)
            pause()

    except subprocess.TimeoutExpired:
        print(RED + "[ERROR] Pemindaian timeout." + RESET)
        pause()

    except Exception as e:
        print(RED + f"[ERROR] {e}" + RESET)
        pause()


def password_check(ssid):
    banner()
    print(neon("[ LOCAL PASSWORD CHECK ]"))
    print(f"Jaringan yang dipilih: {C['bold']}{ssid}{C['reset']}")
    print("\nMasukkan password jaringan milik Anda untuk diperiksa secara lokal.")
    print(C["dim"] + "Password tidak dikirim ke internet dan tidak disimpan dalam LOG." + C["reset"])
    print(C["yellow"] + "WIFI TRACKER tidak menebak atau mencoba password ke router." + C["reset"])
    try:
        import getpass
        pw = getpass.getpass("\nPassword (kosong untuk batal): ")
    except Exception:
        pw = input("\nPassword (input terlihat; kosong untuk batal): ")
    if not pw:
        print(C["yellow"] + "[STOPPED] Pemeriksaan dibatalkan." + C["reset"])
        pause()
        return

    score = 0
    notes = []
    if len(pw) >= 12: score += 2
    elif len(pw) >= 8: score += 1
    else: notes.append("Panjang kurang dari 8 karakter.")
    if re.search(r"[a-z]", pw): score += 1
    else: notes.append("Belum ada huruf kecil.")
    if re.search(r"[A-Z]", pw): score += 1
    else: notes.append("Belum ada huruf besar.")
    if re.search(r"\d", pw): score += 1
    else: notes.append("Belum ada angka.")
    if re.search(r"[^A-Za-z0-9]", pw): score += 1
    else: notes.append("Belum ada simbol.")
    common = {"12345678", "password", "qwerty123", "123456789", "admin123", "password123"}
    if pw.lower() in common:
        score = 0
        notes.append("Password termasuk pola umum yang mudah ditebak.")

    print("\n" + C["blue"] + "─" * 43 + C["reset"])
    if score >= 5:
        print(C["green"] + "[RESULT] KUAT" + C["reset"])
    elif score >= 3:
        print(C["yellow"] + "[RESULT] SEDANG" + C["reset"])
    else:
        print(C["red"] + "[RESULT] LEMAH" + C["reset"])
    print(f"Skor indikator: {score}/6")
    for note in notes:
        print(C["yellow"] + "[INFO] " + note + C["reset"])
    if not notes:
        print(C["green"] + "[INFO] Memenuhi indikator dasar." + C["reset"])
    print(C["dim"] + "\n[LOG] Pemeriksaan lokal selesai. Tidak ada percobaan login." + C["reset"])
    pw = None
    pause()

def main():
    while True:
        banner()
        print(f"{C['green']}[1]{C['reset']} SCAN WIFI")
        print(f"{C['green']}[2]{C['reset']} SUBSCRIBE YOUTUBE DEVELOPER")
        print(f"{C['red']}[0]{C['reset']} EXIT")
        choice = input("\nPilih menu: ").strip()
        if choice == "1":
            scan_wifi()
        elif choice == "2":
            print("Membuka YouTube developer...")
            try:
                webbrowser.open(YOUTUBE_URL)
            except Exception:
                pass
            print(YOUTUBE_URL)
            pause()
        elif choice == "0":
            print(C["yellow"] + "\nWIFI TRACKER ditutup. Sampai jumpa!" + C["reset"])
            break
        else:
            print(C["red"] + "Pilihan tidak valid." + C["reset"])
            pause()

if __name__ == "__main__":
    main()
