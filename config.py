#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
████████╗ ██████╗  ██████╗ ██╗     ███████╗
╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝
   ██║   ██║   ██║██║   ██║██║     ███████╗
   ██║   ██║   ██║██║   ██║██║     ╚════██║
   ██║   ╚██████╔╝╚██████╔╝███████╗███████║
   ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝

██████╗ ██╗██╗   ██╗███████╗██████╗ 
██╔══██╗██║██║   ██║██╔════╝██╔══██╗
██████╔╝██║██║   ██║█████╗  ██████╔╝
██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
██████╔╝██║ ╚████╔╝ ███████╗██║  ██║
╚═════╝ ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝

QUANTUM PHONE DIVER v4.0 - KONFIGURASI API
Author : mrx-n15 (Zamxyz)
Repo   : https://github.com/mrx-n15/quantum-phone-diver

⚠️  PENTING! WAJIB ISI API KEY SENDIRI!
⚠️  JANGAN SHARE FILE INI KE SIAPAPUN!
⚠️  DILARANG digunakan untuk kejahatan!
"""

import os
from pathlib import Path

# ==================== KONFIGURASI API KEY ====================
# 🔴 WAJIB DIISI! Daftar GRATIS di website masing-masing
# ============================================================

CONFIG = {
    # --------------------------------------------------------
    # 1. NUMLOOKUP API - Data pemilik nomor (Truecaller-style)
    # --------------------------------------------------------
    # 📌 Fungsi: Mendapatkan NAMA, GENDER, KOTA, PROVIDER
    # 🌐 Daftar: https://numlookupapi.com
    # 💰 Gratis: 100 requests/bulan
    # ✅ Format: "num_live_xxxxxxxxxxxx"
    # --------------------------------------------------------
    "NUMLOOKUP_API_KEY": "",  # <-- ISI API KEY LU DISINI!
    
    # --------------------------------------------------------
    # 2. HIBP API - Cek kebocoran data (Breach Checker)
    # --------------------------------------------------------
    # 📌 Fungsi: Cek email apakah kena hack/data bocor
    # 🌐 Daftar: https://haveibeenpwned.com/API/Key
    # 💰 Gratis: 1500 requests/bulan
    # ✅ Format: 32 karakter hex (a1b2c3d4e5f6...)
    # --------------------------------------------------------
    "HIBP_API_KEY": "",  # <-- ISI API KEY LU DISINI!
    
    # --------------------------------------------------------
    # 3. OPENWEATHERMAP API - Info cuaca kota (OPSIONAL)
    # --------------------------------------------------------
    # 📌 Fungsi: Menampilkan cuaca terkini di lokasi nomor
    # 🌐 Daftar: https://openweathermap.org/api
    # 💰 Gratis: 60 requests/menit
    # ✅ Format: 32 karakter hex
    # --------------------------------------------------------
    "WEATHER_API_KEY": "",  # <-- ISI KALAU MAU FITUR CUACA
}

# ==================== VALIDASI ====================

def validate_config():
    """Cek konfigurasi dan kasih peringatan"""
    
    print("\n" + "="*60)
    print("🔍 QUANTUM PHONE DIVER - CONFIG VALIDATOR")
    print("="*60 + "\n")
    
    # Cek NumLookup API
    if not CONFIG["NUMLOOKUP_API_KEY"]:
        print("❌ NUMLOOKUP API KEY: [KOSONG]")
        print("   ⚠️  Fitur data pemilik (nama, gender, kota) TIDAK AKTIF!")
        print("   ✅ Daftar GRATIS di: https://numlookupapi.com")
        print("   📝 Format: num_live_xxxxxxxxxxxx\n")
    else:
        print("✅ NUMLOOKUP API KEY: [TERISI]")
        print("   ✓ Fitur data pemilik AKTIF\n")
    
    # Cek HIBP API
    if not CONFIG["HIBP_API_KEY"]:
        print("❌ HIBP API KEY: [KOSONG]")
        print("   ⚠️  Fitur breach checker (cek kebocoran data) TIDAK AKTIF!")
        print("   ✅ Daftar GRATIS di: https://haveibeenpwned.com/API/Key")
        print("   📝 Format: 32 karakter hex\n")
    else:
        print("✅ HIBP API KEY: [TERISI]")
        print("   ✓ Fitur breach checker AKTIF\n")
    
    # Cek Weather API
    if not CONFIG["WEATHER_API_KEY"]:
        print("ℹ️  WEATHER API KEY: [KOSONG]")
        print("   • Fitur info cuaca TIDAK AKTIF (opsional)")
        print("   • Daftar di: https://openweathermap.org/api\n")
    else:
        print("✅ WEATHER API KEY: [TERISI]")
        print("   ✓ Fitur cuaca AKTIF\n")
    
    print("="*60)
    print("📌 CARA ISI API KEY:")
    print("   1. Buka link di atas")
    print("   2. Register / Sign Up (GRATIS!)")
    print("   3. Verifikasi email")
    print("   4. Copy API key yang didapat")
    print("   5. Paste di file config.py ini")
    print("="*60 + "\n")
    
    return all([CONFIG["NUMLOOKUP_API_KEY"], CONFIG["HIBP_API_KEY"]])

# ==================== AUTO-VALIDATE ====================

if __name__ != "__main__":
    # Auto-validate pas diimport
    if not all([CONFIG["NUMLOOKUP_API_KEY"], CONFIG["HIBP_API_KEY"]]):
        print("⚠️  PERINGATAN: API key belum lengkap!")
        print("   Fitur terbatas. Isi config.py dulu, bang!\n")
