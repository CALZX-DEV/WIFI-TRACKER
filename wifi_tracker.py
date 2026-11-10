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
    banner()
    print(neon("[ WIFI SCAN ]"))
    print(C["dim"] + "Meminta daftar jaringan yang terlihat..." + C["reset"] + "\n")

    if not shutil.which("termux-wifi-scaninfo"):
        print(C["yellow"] + "[!] Perintah termux-wifi-scaninfo tidak ditemukan." + C["reset"])
        print("Pastikan aplikasi Termux:API terpasang dan paket termux-api sudah diinstal.")
        pause()
        return

    try:
        result = subprocess.run(
            ["termux-wifi-scaninfo"], capture_output=True, text=True, timeout=25
        )
        if result.returncode != 0:
            print(C["red"] + "[ERROR] Scan gagal." + C["reset"])
            print((result.stderr or result.stdout).strip())
            print("Periksa izin lokasi/perangkat terdekat dan aktifkan Location.")
            pause()
            return
        networks = json.loads(result.stdout or "[]")
    except Exception as exc:
        print(C["red"] + f"[ERROR] {exc}" + C["reset"])
        pause()
        return

    # Deduplicate by SSID while retaining the strongest reported signal.
    found = {}
    for item in networks:
        ssid = (item.get("ssid") or "").strip()
        if not ssid:
            continue
        level = item.get("level", -999)
        if ssid not in found or level > found[ssid].get("level", -999):
            found[ssid] = item

    items = list(found.values())
    items.sort(key=lambda x: x.get("level", -999), reverse=True)

    if not items:
        print(C["yellow"] + "Tidak ada SSID yang terlihat." + C["reset"])
        print("Pastikan Wi-Fi dan Location aktif, lalu coba lagi.")
        pause()
        return

    print(C["white"] + "JARINGAN TERDETEKSI\n" + C["reset"])
    for i, item in enumerate(items, 1):
        ssid = item.get("ssid", "(tanpa nama)")
        bssid = item.get("bssid", "-")
        level = item.get("level", "?")
        security = item.get("capabilities", "info tidak tersedia")
        print(f"{C['cyan']}[{i:02d}]{C['reset']} {C['bold']}{ssid}{C['reset']}")
        print(f"     Signal: {level} dBm | Security: {security}")
    print(f"\n{C['dim']}Catatan: pemindaian hanya menampilkan jaringan; tidak mencoba masuk.{C['reset']}")

    choice = input("\nPilih nomor Wi-Fi (0 untuk kembali): ").strip()
    if choice == "0":
        return
    if not choice.isdigit() or not (1 <= int(choice) <= len(items)):
        print(C["red"] + "Pilihan tidak valid." + C["reset"])
        pause()
        return

    selected = items[int(choice) - 1]
    ssid = selected.get("ssid", "(tanpa nama)")
    print(f"\nTarget dipilih: {C['bold']}{ssid}{C['reset']}")
    confirm = input("Lanjut ke pemeriksaan password milik Anda sendiri? (y/n): ").strip().lower()
    if confirm != "y":
        print(C["yellow"] + "[STOPPED] Proses dibatalkan." + C["reset"])
        pause()
        return
    password_check(ssid)

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
