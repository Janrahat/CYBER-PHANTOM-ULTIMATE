# CYBER PHANTOM ULTIMATE
Colorful terminal toolkit for Termux and Kali Linux.

## Features
- Phone number numbering-plan metadata (country/region/possible-valid status; carrier metadata when available)
- Android device details where Termux permissions/tools allow
- Approximate public IP information
- DNS records
- Website security header audit
- TLS certificate check
- Authorized TCP port check (maximum 20 selected ports)
- Local network details
- Secure password generation and sample strength estimate
- SHA-256 file checker and report center

## Termux
```bash
pkg update && pkg upgrade -y
pkg install python -y
bash install-termux.sh
python main.py
```

## Kali Linux
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
bash install-kali.sh
source .venv/bin/activate
python3 main.py
```

Only test systems you own or have permission to assess. Phone number metadata does not identify the subscriber or provide live GPS. IP geolocation is approximate. This tool does not exploit systems, steal credentials, crack Wi-Fi, or bypass access controls. Reports are stored in `reports/`.
