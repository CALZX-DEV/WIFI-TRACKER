# WIFI TRACKER

Terminal toolkit untuk Termux dengan tampilan neon.

## Fitur
- Scan SSID Wi-Fi yang terlihat melalui Termux:API.
- Pilih jaringan berdasarkan nomor.
- Pemeriksaan kekuatan password secara lokal untuk jaringan milik sendiri.
- Menu menuju YouTube developer: https://youtube.com/@calzxchannel?si=llet1yqiVZe_139f

## Batasan keamanan
Tool ini **tidak** melakukan brute-force, menebak password, mencoba kombinasi ke router, atau mengakses jaringan. Status password tidak dapat dinyatakan `CORRECT/WRONG` tanpa autentikasi yang sah. Password yang dimasukkan hanya diperiksa indikator kekuatannya secara lokal dan tidak dicatat.

## Persyaratan
- Android dengan Termux.
- Aplikasi Termux:API terpasang.
- Paket `termux-api`.
- Izin Location / Nearby devices dan Wi-Fi/Location Android aktif.

## Instalasi
```bash
chmod +x install.sh
bash install.sh
python wifi_tracker.py
```

## Catatan
Hasil scan bergantung pada versi Android, izin, dan pembatasan pemindaian Wi-Fi sistem. Tool ini tidak menjamin semua access point akan ditampilkan.
