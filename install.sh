#!/data/data/com.termux/files/usr/bin/bash
set -e
clear
echo -e "\033[96m[ WIFI TRACKER INSTALLER ]\033[0m"
pkg update -y
pkg install -y python termux-api
echo
echo "PENTING:"
echo "1. Pasang aplikasi Termux:API dari sumber yang sama dengan Termux."
echo "2. Beri izin Location / Nearby devices kepada Termux:API."
echo "3. Aktifkan Wi-Fi dan Location Android sebelum scan."
chmod +x wifi_tracker.py
echo
echo "Instalasi selesai."
echo "Jalankan: python wifi_tracker.py"
