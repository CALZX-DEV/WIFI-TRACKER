
# WIFI TRACKER

Terminal-based Wi-Fi Scanner for Termux.

WIFI TRACKER is a Python-based terminal tool designed to display nearby Wi-Fi networks and perform local password-strength checks.

## FEATURES

- Wi-Fi network scanning
- Display detected SSID
- Network selection by number
- Local password strength checker
- Password strength results
- Scan and check logs
- YouTube developer shortcut
- Neon terminal interface

## REQUIREMENTS

- Android device
- Termux
- Python 3
- Git
- Termux:API application
- Active Wi-Fi and Location permissions

## INSTALLATION

Follow the installation steps in order.

### 1. Update Termux packages

```bash
pkg update && pkg upgrade -y
```

### 2. Install required packages

```bash
pkg install git python termux-api -y
```

### 3. Install Termux:API application

Make sure the Termux:API Android application is installed from a compatible source.

### 4. Clone repository

```bash
git clone https://github.com/CALZX-DEV/WIFI-TRACKER.git
```

### 5. Enter project directory

```bash
cd WIFI-TRACKER
```

### 6. Run installer

```bash
bash install.sh
```

### 7. Start WIFI TRACKER

```bash
python wifi_tracker.py
```

## HOW TO USE

### Main Menu

After starting the application, the main menu will appear.

```text
WIFI TRACKER

[1] SCAN WIFI
[2] SUBSCRIBE YOUTUBE DEVELOPER
[0] EXIT

Select menu:
```

### Wi-Fi Scanning

1. Select menu 1.
2. Wait for the scanning process.
3. Available Wi-Fi networks will be displayed.
4. Select a network using its number.
5. Confirm to continue to the local password-strength check.

### Password Strength Check

Enter your own Wi-Fi password for a local strength assessment.

Available results:

- STRONG
- MEDIUM
- WEAK

## TROUBLESHOOTING

### Wi-Fi networks are not displayed

Check the following:

- Wi-Fi is enabled.
- Android Location is enabled.
- Termux:API is installed.
- Required Android permissions are granted.

### Termux:API command not found

```bash
pkg install termux-api -y
```

### Python not found

```bash
pkg install python -y
```

## UPDATE

To update the project:

```bash
cd WIFI-TRACKER
git pull
```

## SECURITY NOTICE

WIFI TRACKER only scans visible Wi-Fi networks and performs local password-strength assessments.

It does not perform brute-force attacks, attempt password combinations against routers, or access unauthorized networks.

Password strength results do not represent successful Wi-Fi authentication.

## DEVELOPER

Project: WIFI TRACKER

GitHub:
https://github.com/CALZX-DEV/WIFI-TRACKER

YouTube:
https://youtube.com/@calzxchannel

## LICENSE

For educational and authorized security testing purposes.
