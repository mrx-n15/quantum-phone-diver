#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║                 QUANTUM PHONE DIVER v3.0                ║
║                    CONFIGURATION FILE                   ║
║                    👑 CREDIT: ZAMXYZ                   ║
╚══════════════════════════════════════════════════════════╝

📌 CARA ISI API KEY:
1. Daftar di website masing-masing (GRATIS!)
2. Copy API key yang didapat
3. Paste di bawah ini (diapit tanda petik)
4. Simpan file

⚠️ JANGAN SHARE API KEY LU KE SIAPAPUN!
⚠️ KALO KOSONG, FITUR TERKAIT TIDAK AKAN JALAN.
"""

import os
from pathlib import Path

# ==================== API CONFIGURATION ====================

CONFIG = {
    # ------------------------------------------------------
    # NUMLOOKUP API - Untuk data Truecaller-like
    # Daftar: https://numlookupapi.com
    # Format: "num_live_xxxxxxxxxxxx"
    # Gratis: 100 requests/bulan
    # ------------------------------------------------------
    "NUMLOOKUP_API_KEY": "",  # <-- ISI DI SINI!
    
    # ------------------------------------------------------
    # HAVE I BEEN PWNED API - Cek kebocoran data
    # Daftar: https://haveibeenpwned.com/API/Key
    # Format: 32 karakter hex (contoh: a1b2c3d4e5f6...)
    # Gratis: 1500 requests/bulan  
    # ------------------------------------------------------
    "HIBP_API_KEY": "",  # <-- ISI DI SINI!
    
    # ------------------------------------------------------
    # HUNTER.IO API - Verifikasi & cari email
    # Daftar: https://hunter.io/api-keys
    # Format: 32 karakter alfanumerik
    # Gratis: 25 requests/bulan
    # ------------------------------------------------------
    "HUNTER_IO_API_KEY": "",  # <-- ISI DI SINI!
    
    # ------------------------------------------------------
    # PROXY CONFIGURATION (Opsional)
    # Gunakan kalo lu pengen anonim
    # Format: "http://user:pass@host:port" atau "socks5://host:port"
    # ------------------------------------------------------
    "USE_PROXY": False,
    "PROXY_LIST": [
        # "socks5://127.0.0.1:9050",  # Contoh Tor
        # "http://proxy1.example.com:8080",
    ],
    
    # ------------------------------------------------------
    # USER AGENT ROTATION
    # Biar gak kena blocking
    # ------------------------------------------------------
    "USER_AGENTS": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/537.36",
        "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 Chrome/112.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0",
    ],
    
    # ------------------------------------------------------
    # TIMEOUT SETTINGS (detik)
    # ------------------------------------------------------
    "REQUEST_TIMEOUT": 15,
    "BATCH_DELAY": 0.5,  # Delay antar request di batch mode
}

# ==================== DIRECTORY SETTINGS ====================

# Buat folder output kalo belum ada
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

# Buat folder logs kalo belum ada
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

# ==================== COLOR SETTINGS ====================

# Matiin warna kalo di Windows yang gak support
DISABLE_COLORS = False  # Set True kalo di CMD jadul

# ==================== EXPORT SETTINGS ====================

EXPORT_CONFIG = {
    "csv_delimiter": ",",  # Pemisah CSV (bisa ";" buat Excel Indonesia)
    "csv_encoding": "utf-8-sig",  # Biar gak jadi mojok di Excel
    "html_template": "default",  # Template HTML
    "include_timestamp": True,  # Sertakan timestamp di nama file
}

# ==================== VERIFIKASI ====================

def verify_config():
    """Cek konfigurasi, kasih warning kalo ada yang kosong"""
    
    print("╔════════════════════════════════════════════════╗")
    print("║        🔍 QUANTUM CONFIG VERIFICATION         ║")
    print("╚════════════════════════════════════════════════╝")
    
    if not CONFIG["NUMLOOKUP_API_KEY"]:
        print("⚠️  NumLookup API Key: [KOSONG] - Fitur carrier lookup tidak aktif")
    else:
        print("✅ NumLookup API Key: [TERISI]")
    
    if not CONFIG["HIBP_API_KEY"]:
        print("⚠️  HIBP API Key: [KOSONG] - Fitur breach check tidak aktif") 
    else:
        print("✅ HIBP API Key: [TERISI]")
    
    if not CONFIG["HUNTER_IO_API_KEY"]:
        print("⚠️  Hunter.io API Key: [KOSONG] - Fitur email verifikasi terbatas")
    else:
        print("✅ Hunter.io API Key: [TERISI]")
    
    print("\n📁 Output directory:", OUTPUT_DIR.absolute())
    print("📁 Logs directory:", LOGS_DIR.absolute())
    print("\n✅ Verifikasi selesai.\n")

# Uncomment baris di bawah kalo lu mau auto-verifikasi setiap run
# if __name__ != "__main__":
#     verify_config()