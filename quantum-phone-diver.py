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

QUANTUM PHONE DIVER v4.0 - DEEP OSINT LEGAL EDITION
Author : mrx-n15 (Zamxyz)
License: Islamic MIT - Haram digunakan untuk kejahatan!
Repo   : https://github.com/mrx-n15/quantum-phone-diver
"""

import os
import re
import json
import time
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
from datetime import datetime
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys
import csv
from urllib.parse import quote

# ==================== KONFIGURASI WARNA ====================
class Colors:
    """Warna terminal biar keren"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    END = '\033[0m'

# ==================== KONFIGURASI API ====================
# ⚠️  WAJIB DIISI! Daftar gratis di website masing-masing
CONFIG = {
    # NumLookup API - https://numlookupapi.com
    "NUMLOOKUP_API_KEY": "",  # ISI SENDIRI! Format: "num_live_xxxxxxxxxxxx"
    
    # HIBP API - https://haveibeenpwned.com/API/Key
    "HIBP_API_KEY": "",       # ISI SENDIRI! Format: 32 karakter hex
    
    # OpenWeatherMap API - https://openweathermap.org/api (OPSIONAL)
    "WEATHER_API_KEY": "",    # ISI SENDIRI kalo mau fitur cuaca
}

# ==================== BANNER ====================
BANNER = f"""
{Colors.BOLD}{Colors.CYAN}
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   ██████╗ ██████╗ ██████╗     ██╗   ██╗  ██████╗   ██████╗         ║
║   ██╔══██╗██╔══██╗██╔══██╗    ██║   ██║ ██╔═══██╗ ██╔════╝         ║
║   ██████╔╝██████╔╝██║  ██║    ██║   ██║ ██║   ██║ ██║  ███╗        ║
║   ██╔═══╝ ██╔══██╗██║  ██║    ╚██╗ ██╔╝ ██║▄▄ ██║ ██║   ██║        ║
║   ██║     ██║  ██║██████╔╝     ╚████╔╝  ╚██████╔╝ ╚██████╔╝        ║
║   ╚═╝     ╚═╝  ╚═╝╚═════╝       ╚═══╝    ╚══▀▀═╝   ╚═════╝         ║
║                                                                      ║
║   🔥 QUANTUM PHONE DIVER v4.0 - DEEP OSINT LEGAL EDITION           ║
║   📱 TRACKING JEJAK DIGITAL NOMOR TELEPON - BUKAN LOKASI!          ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   👑 Author  : mrx-n15 (Zamxyz)                                    ║
║   🕋 Support : Allah SWT, Anonymous Cyber Muslim Indonesia         ║
║   📜 License : Islamic MIT - HARAM untuk kejahatan!                ║
║   🔗 Repo    : https://github.com/mrx-n15/quantum-phone-diver      ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
{Colors.END}
"""

# ==================== VALIDASI NOMOR TELEPON ====================
class PhoneValidator:
    """Validasi nomor telepon internasional"""
    
    @staticmethod
    def validate(phone_number):
        """Validasi dan ekstrak informasi dasar"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                return None, "Nomor tidak valid"
            
            # Dapatkan lokasi dalam Bahasa Indonesia kalo bisa
            location_id = geocoder.description_for_number(parsed, "id")
            if not location_id:
                location_id = geocoder.description_for_number(parsed, "en")
            
            # Dapatkan operator
            carrier_name = carrier.name_for_number(parsed, "id")
            if not carrier_name:
                carrier_name = carrier.name_for_number(parsed, "en")
            
            info = {
                "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "country_code": parsed.country_code,
                "national_number": parsed.national_number,
                "location": location_id or "Unknown",
                "carrier": carrier_name or "Unknown",
                "timezone": list(timezone.time_zones_for_number(parsed))[0] if timezone.time_zones_for_number(parsed) else "Unknown",
                "is_valid": True,
                "is_mobile": phonenumbers.number_type(parsed) == 1,
                "is_possible": phonenumbers.is_possible_number(parsed),
            }
            return parsed, info
        except Exception as e:
            return None, f"Error: {str(e)}"

# ==================== INFORMASI OPERATOR LENGKAP ====================
class CarrierInfoEngine:
    """Informasi detail operator berdasarkan prefix"""
    
    @staticmethod
    def get_carrier_details(phone_number):
        """Dapatkan detail lengkap operator"""
        # Bersihkan nomor
        clean_number = phone_number.replace('+', '').replace(' ', '').replace('-', '')
        
        # Ambil 5 digit pertama untuk identifikasi
        prefix = clean_number[:5] if len(clean_number) >= 5 else clean_number
        
        # Database operator Indonesia (publik)
        carrier_db = {
            # Telkomsel
            "62811": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62812": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62813": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62821": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62822": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62823": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62851": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62852": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62853": {"carrier": "Telkomsel", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            
            # Indosat
            "62814": {"carrier": "Indosat", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62815": {"carrier": "Indosat", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62816": {"carrier": "Indosat", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62855": {"carrier": "Indosat", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62856": {"carrier": "Indosat", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62857": {"carrier": "Indosat", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62858": {"carrier": "Indosat", "type": "GSM", "generation": "4G", "technology": "LTE"},
            
            # XL
            "62817": {"carrier": "XL", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62818": {"carrier": "XL", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62819": {"carrier": "XL", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62859": {"carrier": "XL", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62877": {"carrier": "XL", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62878": {"carrier": "XL", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            "62879": {"carrier": "XL", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
            
            # Axis
            "62831": {"carrier": "Axis", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62832": {"carrier": "Axis", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62833": {"carrier": "Axis", "type": "GSM", "generation": "4G", "technology": "LTE"},
            
            # Smartfren
            "62881": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62882": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62883": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62884": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62885": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62886": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62887": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62888": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            "62889": {"carrier": "Smartfren", "type": "CDMA/4G", "generation": "4G", "technology": "LTE"},
            
            # Three
            "62895": {"carrier": "Three", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62896": {"carrier": "Three", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62897": {"carrier": "Three", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62898": {"carrier": "Three", "type": "GSM", "generation": "4G", "technology": "LTE"},
            "62899": {"carrier": "Three", "type": "GSM", "generation": "4G", "technology": "LTE"},
            
            # By.U
            "62838": {"carrier": "By.U", "type": "GSM", "generation": "4G/5G", "technology": "LTE/5G NR"},
        }
        
        default = {"carrier": "Unknown", "type": "Unknown", "generation": "Unknown", "technology": "Unknown"}
        
        # Cari berdasarkan prefix
        for i in range(5, 3, -1):  # Coba dari 5 digit turun ke 4 digit
            prefix_part = clean_number[:i]
            if prefix_part in carrier_db:
                return carrier_db[prefix_part]
        
        return default

# ==================== INFORMASI LOKASI (KOORDINAT KOTA) ====================
class LocationInfoEngine:
    """Informasi geografis berdasarkan lokasi nomor (BUKAN TRACKING INDIVIDU)"""
    
    @staticmethod
    def get_city_coordinates(city_name):
        """Dapatkan koordinat kota (PUBLIC DATA)"""
        
        # Database koordinat kota-kota di Indonesia
        city_coordinates = {
            "Jakarta": {"lat": -6.2088, "lon": 106.8456, "province": "DKI Jakarta", "timezone": "WIB"},
            "Surabaya": {"lat": -7.2575, "lon": 112.7521, "province": "Jawa Timur", "timezone": "WIB"},
            "Bandung": {"lat": -6.9175, "lon": 107.6191, "province": "Jawa Barat", "timezone": "WIB"},
            "Medan": {"lat": 3.5952, "lon": 98.6722, "province": "Sumatera Utara", "timezone": "WIB"},
            "Semarang": {"lat": -6.9931, "lon": 110.4203, "province": "Jawa Tengah", "timezone": "WIB"},
            "Makassar": {"lat": -5.1477, "lon": 119.4327, "province": "Sulawesi Selatan", "timezone": "WITA"},
            "Palembang": {"lat": -2.9911, "lon": 104.7567, "province": "Sumatera Selatan", "timezone": "WIB"},
            "Yogyakarta": {"lat": -7.7956, "lon": 110.3695, "province": "DIY", "timezone": "WIB"},
            "Denpasar": {"lat": -8.6705, "lon": 115.2126, "province": "Bali", "timezone": "WITA"},
            "Manado": {"lat": 1.4748, "lon": 124.8421, "province": "Sulawesi Utara", "timezone": "WITA"},
            "Balikpapan": {"lat": -1.2654, "lon": 116.8312, "province": "Kalimantan Timur", "timezone": "WITA"},
            "Jayapura": {"lat": -2.5910, "lon": 140.6690, "province": "Papua", "timezone": "WIT"},
            "Pontianak": {"lat": -0.0263, "lon": 109.3425, "province": "Kalimantan Barat", "timezone": "WIB"},
            "Banjarmasin": {"lat": -3.3186, "lon": 114.5944, "province": "Kalimantan Selatan", "timezone": "WITA"},
            "Samarinda": {"lat": -0.4948, "lon": 117.1436, "province": "Kalimantan Timur", "timezone": "WITA"},
            "Pekanbaru": {"lat": 0.5071, "lon": 101.4478, "province": "Riau", "timezone": "WIB"},
            "Batam": {"lat": 1.0456, "lon": 104.0305, "province": "Kepulauan Riau", "timezone": "WIB"},
            "Padang": {"lat": -0.9471, "lon": 100.4172, "province": "Sumatera Barat", "timezone": "WIB"},
            "Lampung": {"lat": -5.3971, "lon": 105.2663, "province": "Lampung", "timezone": "WIB"},
            "Malang": {"lat": -7.9666, "lon": 112.6326, "province": "Jawa Timur", "timezone": "WIB"},
            "Bogor": {"lat": -6.5971, "lon": 106.8060, "province": "Jawa Barat", "timezone": "WIB"},
            "Tangerang": {"lat": -6.1702, "lon": 106.6403, "province": "Banten", "timezone": "WIB"},
            "Bekasi": {"lat": -6.2416, "lon": 106.9924, "province": "Jawa Barat", "timezone": "WIB"},
            "Depok": {"lat": -6.4025, "lon": 106.7942, "province": "Jawa Barat", "timezone": "WIB"},
            "Cirebon": {"lat": -6.7069, "lon": 108.5570, "province": "Jawa Barat", "timezone": "WIB"},
            "Solo": {"lat": -7.5667, "lon": 110.8167, "province": "Jawa Tengah", "timezone": "WIB"},
            "Kupang": {"lat": -10.1772, "lon": 123.6070, "province": "NTT", "timezone": "WITA"},
            "Ambon": {"lat": -3.6954, "lon": 128.1814, "province": "Maluku", "timezone": "WIT"},
            "Ternate": {"lat": 0.7893, "lon": 127.3848, "province": "Maluku Utara", "timezone": "WIT"},
            "Mataram": {"lat": -8.5833, "lon": 116.1167, "province": "NTB", "timezone": "WITA"},
            "Banda Aceh": {"lat": 5.5483, "lon": 95.3238, "province": "Aceh", "timezone": "WIB"},
            "Jambi": {"lat": -1.5899, "lon": 103.6071, "province": "Jambi", "timezone": "WIB"},
            "Bengkulu": {"lat": -3.8003, "lon": 102.2562, "province": "Bengkulu", "timezone": "WIB"},
            "Pangkal Pinang": {"lat": -2.1290, "lon": 106.1138, "province": "Bangka Belitung", "timezone": "WIB"},
            "Tanjung Pinang": {"lat": 0.9169, "lon": 104.4435, "province": "Kepulauan Riau", "timezone": "WIB"},
            "Palangka Raya": {"lat": -2.2105, "lon": 113.9201, "province": "Kalimantan Tengah", "timezone": "WIB"},
            "Tanjung Selor": {"lat": 2.8368, "lon": 117.3652, "province": "Kalimantan Utara", "timezone": "WITA"},
            "Mamuju": {"lat": -2.6806, "lon": 118.8861, "province": "Sulawesi Barat", "timezone": "WITA"},
            "Kendari": {"lat": -3.9985, "lon": 122.5129, "province": "Sulawesi Tenggara", "timezone": "WITA"},
            "Palu": {"lat": -0.8986, "lon": 119.8507, "province": "Sulawesi Tengah", "timezone": "WITA"},
            "Gorontalo": {"lat": 0.5333, "lon": 123.0667, "province": "Gorontalo", "timezone": "WITA"},
            "Serang": {"lat": -6.1200, "lon": 106.1503, "province": "Banten", "timezone": "WIB"},
        }
        
        # Cari kota yang cocok
        for city, coord in city_coordinates.items():
            if city.lower() in city_name.lower():
                return {
                    "city": city,
                    "province": coord["province"],
                    "timezone": coord["timezone"],
                    "latitude": coord["lat"],
                    "longitude": coord["lon"],
                    "google_maps": f"https://www.google.com/maps?q={coord['lat']},{coord['lon']}",
                    "note": "Koordinat PUSAT KOTA, BUKAN lokasi individu! Untuk referensi geografis."
                }
        
        return None
    
    @staticmethod
    def get_location_info(phone_number, location_name):
        """Dapatkan informasi lokasi lengkap"""
        
        # Coba dapatkan koordinat
        coords = LocationInfoEngine.get_city_coordinates(location_name)
        
        result = {
            "city": location_name,
            "province": coords["province"] if coords else "Unknown",
            "timezone": coords["timezone"] if coords else await TimeZoneEngine.get_timezone(phone_number),
            "coordinates": {
                "lat": coords["latitude"] if coords else None,
                "lon": coords["longitude"] if coords else None,
                "google_maps": coords["google_maps"] if coords else None
            } if coords else None,
            "note": "Lokasi berdasarkan kode area (BUKAN tracking individu). Koordinat adalah PUSAT KOTA untuk referensi."
        }
        
        return result

# ==================== ENGINE ZONA WAKTU ====================
class TimeZoneEngine:
    """Dapatkan zona waktu berdasarkan nomor telepon"""
    
    @staticmethod
    async def get_timezone(phone_number):
        """Dapatkan zona waktu dari nomor"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            tz_list = timezone.time_zones_for_number(parsed)
            if tz_list:
                return list(tz_list)[0]
        except:
            pass
        return "Unknown"

# ==================== ENGINE NUMLOOKUP ====================
class NumLookupEngine:
    """Integrasi NumLookup API - Truecaller-style"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.numlookupapi.com/v1/validate/"
    
    def lookup(self, phone_number):
        """Cari data pemilik nomor"""
        if not self.api_key:
            return {"error": "API key kosong. Daftar di numlookupapi.com"}
        
        try:
            url = f"{self.base_url}{phone_number}"
            response = requests.get(url, params={"apikey": self.api_key}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "valid": data.get("valid", False),
                    "line_type": data.get("line_type", "Unknown"),
                    "carrier": data.get("carrier", "Unknown"),
                    "location": data.get("location", "Unknown"),
                    "country_name": data.get("country_name", "Unknown"),
                    "country_code": data.get("country_code", "Unknown"),
                    "name": data.get("name", None),  # Nama pemilik (kalo ada)
                    "gender": data.get("gender", None),  # Gender (kalo ada)
                    "city": data.get("city", None),  # Kota (kalo ada)
                    "province": data.get("province", None),  # Provinsi (kalo ada)
                }
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

# ==================== ENGINE TELEGRAM ====================
class TelegramEngine:
    """Deteksi username Telegram dari nomor"""
    
    @staticmethod
    def get_username(phone_number):
        """Ambil username Telegram asli"""
        try:
            clean_number = phone_number.replace('+', '').replace(' ', '')
            url = f"https://t.me/+{clean_number}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                html = response.text
                
                # Ekstrak username dari meta tag
                patterns = [
                    r'<meta property="og:url" content="https://t\.me/([^"]+)"',
                    r'<link rel="canonical" href="https://t\.me/([^"]+)"',
                    r'"https://t\.me/([^"]+)"',
                ]
                
                for pattern in patterns:
                    match = re.search(pattern, html)
                    if match:
                        username = match.group(1)
                        # Skip kalo masih berupa nomor
                        if not username.replace('+', '').replace(' ', '').isdigit():
                            return {
                                "registered": True,
                                "username": username,
                                "profile_url": f"https://t.me/{username}",
                                "direct_link": url
                            }
            
            return {"registered": False, "username": None}
        except Exception as e:
            return {"error": str(e), "registered": False}

# ==================== ENGINE WHATSAPP ====================
class WhatsAppEngine:
    """Cek registrasi WhatsApp"""
    
    @staticmethod
    def check_registration(phone_number):
        """Cek apakah nomor terdaftar di WhatsApp"""
        try:
            clean_number = phone_number.replace('+', '').replace(' ', '')
            url = f"https://wa.me/{clean_number}"
            
            # Cek dengan HEAD request
            response = requests.head(url, timeout=10, allow_redirects=True)
            
            return {
                "registered": response.status_code == 200,
                "link": f"https://wa.me/{clean_number}",
                "api_link": f"https://api.whatsapp.com/send?phone={clean_number}",
                "intent_link": f"intent://send?phone={clean_number}#Intent;package=com.whatsapp;scheme=smsto;end"
            }
        except:
            return {"registered": False, "link": None}

# ==================== ENGINE INSTAGRAM ====================
class InstagramEngine:
    """Generate username Instagram dari nomor"""
    
    @staticmethod
    def search_by_phone(phone_info):
        """Generate kemungkinan username Instagram"""
        national = phone_info.get('national', '').replace(' ', '')
        e164 = phone_info.get('e164', '').replace('+', '')
        
        usernames = []
        variants = [
            national,
            e164,
            f"0{national}" if not national.startswith('0') else national,
            f"+{e164}",
            f"62{national[-9:]}" if len(national) > 9 else national,
            f"08{national[-9:]}" if len(national) > 9 else national,
            f"user{national[-6:]}",
            f"id{national[-6:]}",
            f"member{national[-6:]}",
            f"phone{national[-8:]}",
        ]
        
        for var in list(set(variants))[:10]:
            usernames.append({
                "username": var,
                "search_url": f"https://www.instagram.com/{var}/",
                "web_search": f"https://www.instagram.com/web/search/topsearch/?query={var}"
            })
        
        return usernames

# ==================== ENGINE FACEBOOK ====================
class FacebookEngine:
    """Generate link pencarian Facebook"""
    
    @staticmethod
    def search_by_phone(phone_number):
        """Generate link pencarian di Facebook"""
        clean = phone_number.replace('+', '').replace(' ', '')
        return {
            "search_url": f"https://www.facebook.com/search/top/?q={clean}",
            "people_search": f"https://www.facebook.com/search/people/?q={clean}",
            "mobile_deep_link": f"fb://search/?q={clean}"
        }

# ==================== ENGINE SIGNAL ====================
class SignalEngine:
    """Generate link Signal"""
    
    @staticmethod
    def check_registration(phone_number):
        """Generate link untuk cek Signal"""
        clean = phone_number.replace('+', '').replace(' ', '')
        return {
            "link": f"https://signal.me/#p/{clean}",
            "note": "Buka link di browser. Jika redirect ke app Signal, nomor terdaftar."
        }

# ==================== ENGINE EMAIL ====================
class EmailEngine:
    """Generate kemungkinan email dari nomor"""
    
    @staticmethod
    def generate_emails(phone_info, name_hint=None):
        """Generate email candidates"""
        national = phone_info.get('national', '').replace(' ', '')
        e164 = phone_info.get('e164', '').replace('+', '')
        
        emails = []
        domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com', 'icloud.com']
        
        # Format dari nomor
        for domain in domains:
            emails.append(f"{national}@{domain}")
            emails.append(f"{e164}@{domain}")
            emails.append(f"0{national}@{domain}")
            emails.append(f"62{national[-9:]}@{domain}")
            emails.append(f"+{e164}@{domain}")
            emails.append(f"phone{national[-8:]}@{domain}")
        
        # Format dari nama (kalo ada)
        if name_hint and isinstance(name_hint, str):
            name_parts = name_hint.lower().split()
            if len(name_parts) >= 1:
                first = name_parts[0]
                emails.append(f"{first}@{domains[0]}")
                emails.append(f"{first}{national[-6:]}@{domains[0]}")
                
            if len(name_parts) >= 2:
                first, last = name_parts[0], name_parts[-1]
                emails.append(f"{first}.{last}@{domains[0]}")
                emails.append(f"{first}{last}@{domains[0]}")
                emails.append(f"{first}_{last}@{domains[0]}")
                emails.append(f"{last}.{first}@{domains[0]}")
        
        # Hapus duplikat, limit 15
        return list(set(emails))[:15]

# ==================== ENGINE BREACH CHECKER ====================
class BreachEngine:
    """Cek kebocoran data via HIBP"""
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def check_email(self, email):
        """Cek email di database breach"""
        if not self.api_key or len(self.api_key) < 10:
            return []
        
        try:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {
                "hibp-api-key": self.api_key,
                "user-agent": "Quantum-Phone-Diver"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                return [{
                    "name": b.get("Name", "Unknown"),
                    "date": b.get("BreachDate", "Unknown"),
                    "description": b.get("Description", "")[:100] + "...",
                    "domain": b.get("Domain", "Unknown")
                } for b in breaches[:5]]
            return []
        except:
            return []

# ==================== ENGINE USERNAME ====================
class UsernameEngine:
    """Generate berbagai varian username"""
    
    @staticmethod
    def generate_all(phone_info):
        """Generate semua kemungkinan username"""
        national = phone_info.get('national', '').replace(' ', '')
        e164 = phone_info.get('e164', '').replace('+', '')
        
        usernames = []
        
        # Format pendek
        variants = [
            national,
            national[-9:],  # 9 digit belakang
            national[-8:],  # 8 digit belakang
            national[-7:],  # 7 digit belakang
            national[-6:],  # 6 digit belakang
            f"0{national}",
            f"62{national[-9:]}",
            f"+62{national[-9:]}",
            f"08{national[-9:]}",
            f"user{national[-6:]}",
            f"id{national[-6:]}",
            f"member{national[-6:]}",
            f"phone{national[-8:]}",
            f"mobile{national[-8:]}",
            f"contact{national[-8:]}",
            f"hp{national[-8:]}",
        ]
        
        return list(set(variants))[:15]

# ==================== ENGINE SOSIAL MEDIA ====================
class SocialMediaEngine:
    """Pencarian di berbagai platform sosial media"""
    
    @staticmethod
    def search_all_platforms(phone_number, username_variants):
        """Generate link pencarian di semua platform"""
        
        platforms = {
            "Twitter/X": "https://twitter.com/search?q={}&src=typed_query",
            "TikTok": "https://www.tiktok.com/search?q={}",
            "Instagram": "https://www.instagram.com/{}/",
            "Facebook": "https://www.facebook.com/search/top/?q={}",
            "LinkedIn": "https://www.linkedin.com/search/results/all/?keywords={}",
            "YouTube": "https://www.youtube.com/results?search_query={}",
            "Pinterest": "https://www.pinterest.com/search/pins/?q={}",
            "Tumblr": "https://{}.tumblr.com",
            "Snapchat": "https://www.snapchat.com/add/{}",
            "Discord": "https://discord.com/search?q={}",
            "Telegram": "https://t.me/{}",
            "WhatsApp": "https://wa.me/{}",
            "Signal": "https://signal.me/#p/{}",
            "Viber": "viber://add?number={}",
            "Line": "https://line.me/R/home/public/profile?id={}",
            "Skype": "skype:{}?chat",
            "Spotify": "https://open.spotify.com/search/{}",
            "GitHub": "https://github.com/{}",
            "Medium": "https://medium.com/@{}",
            "Reddit": "https://www.reddit.com/user/{}",
            "Twitch": "https://www.twitch.tv/{}",
            "Steam": "https://steamcommunity.com/id/{}",
            "PayPal": "https://www.paypal.com/paypalme/{}",
            "Tinder": "https://tinder.com/@{}",
            "Badoo": "https://badoo.com/en/{}",
            "Snapchat": "https://www.snapchat.com/add/{}",
            "WeChat": "https://weixin.qq.com/r/{}",
        }
        
        results = []
        clean_number = phone_number.replace('+', '').replace(' ', '')
        
        # Cari pake nomor langsung
        results.append({
            "platform": "WhatsApp Direct",
            "search_url": f"https://wa.me/{clean_number}",
            "type": "direct"
        })
        
        results.append({
            "platform": "Telegram Direct",
            "search_url": f"https://t.me/+{clean_number}",
            "type": "direct"
        })
        
        # Cari pake username variants
        for username in username_variants[:5]:
            for platform, url_template in platforms.items():
                if "{}" in url_template and len(username) > 3:
                    url = url_template.format(username)
                    results.append({
                        "platform": platform,
                        "username": username,
                        "search_url": url,
                        "type": "search"
                    })
        
        return results[:25]  # Limit 25 hasil

# ==================== ENGINE ANALISIS RISIKO ====================
class RiskAnalysisEngine:
    """Analisis tingkat eksposur nomor"""
    
    @staticmethod
    def analyze(phone_info, telegram_data, whatsapp_data, social_results, email_count):
        """Analisis risiko privasi"""
        
        risk_score = 0
        risk_factors = []
        recommendations = []
        
        # Faktor 1: Nomor mobile
        if phone_info.get('is_mobile'):
            risk_score += 10
            risk_factors.append("Nomor mobile lebih mudah dilacak")
        
        # Faktor 2: Telegram terdaftar
        if telegram_data.get('registered'):
            risk_score += 25
            risk_factors.append("Telegram terdaftar dengan username publik")
            recommendations.append("Setel username Telegram ke private")
        
        # Faktor 3: WhatsApp
        if whatsapp_data.get('registered'):
            risk_score += 15
            risk_factors.append("WhatsApp aktif")
            recommendations.append("Atur privasi foto profil ke 'Kontak Saja'")
        
        # Faktor 4: Banyak platform
        platforms_found = set()
        for result in social_results[:20]:
            platforms_found.add(result['platform'])
        
        platform_count = len(platforms_found)
        if platform_count > 10:
            risk_score += 30
            risk_factors.append(f"Terdeteksi di {platform_count} platform sosial media")
            recommendations.append("Nomor terlalu terekspos - pertimbangkan ganti nomor")
        elif platform_count > 5:
            risk_score += 20
            risk_factors.append(f"Terdeteksi di {platform_count} platform sosial media")
        
        # Faktor 5: Email terasosiasi
        if email_count > 5:
            risk_score += 15
            risk_factors.append(f"{email_count} kemungkinan email terasosiasi")
            recommendations.append("Cek email di haveibeenpwned.com secara berkala")
        
        # Tentukan level risiko
        if risk_score >= 60:
            risk_level = "🔴 TINGGI"
        elif risk_score >= 30:
            risk_level = "🟡 SEDANG"
        else:
            risk_level = "🟢 RENDAH"
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risk_factors": risk_factors[:5],
            "recommendations": recommendations[:5],
            "platforms_detected": list(platforms_found)[:10]
        }

# ==================== ENGINE CUACA (OPSIONAL) ====================
class WeatherEngine:
    """Informasi cuaca di lokasi nomor (PUBLIC API)"""
    
    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_weather(self, city_name):
        """Dapatkan cuaca terkini di kota"""
        if not self.api_key:
            return {"error": "Weather API key kosong"}
        
        try:
            # OpenWeatherMap API
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                "q": city_name,
                "appid": self.api_key,
                "units": "metric",
                "lang": "id"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "city": data.get("name", city_name),
                    "temperature": f"{data['main']['temp']}°C",
                    "feels_like": f"{data['main']['feels_like']}°C",
                    "humidity": f"{data['main']['humidity']}%",
                    "pressure": f"{data['main']['pressure']} hPa",
                    "weather": data['weather'][0]['description'],
                    "wind_speed": f"{data['wind']['speed']} m/s",
                    "icon": data['weather'][0]['icon'],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "note": "Informasi cuaca publik untuk kota, BUKAN data individu"
                }
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

# ==================== ENGINE UTAMA ====================
class QuantumPhoneDiver:
    """Main OSINT Engine"""
    
    def __init__(self):
        self.phone_info = {}
        self.numlookup_data = {}
        self.telegram_data = {}
        self.whatsapp_data = {}
        self.instagram_usernames = []
        self.facebook_data = {}
        self.signal_data = {}
        self.email_candidates = []
        self.breach_results = []
        self.username_variants = []
        self.social_results = []
        self.risk_analysis = {}
        self.location_info = {}
        self.carrier_details = {}
        self.weather_info = {}
        self.start_time = datetime.now()
        
        # Init engines
        self.validator = PhoneValidator()
        self.carrier_engine = CarrierInfoEngine()
        self.location_engine = LocationInfoEngine()
        self.numlookup = NumLookupEngine(CONFIG["NUMLOOKUP_API_KEY"])
        self.telegram = TelegramEngine()
        self.whatsapp = WhatsAppEngine()
        self.instagram = InstagramEngine()
        self.facebook = FacebookEngine()
        self.signal = SignalEngine()
        self.email = EmailEngine()
        self.breach = BreachEngine(CONFIG["HIBP_API_KEY"])
        self.username = UsernameEngine()
        self.social = SocialMediaEngine()
        self.risk = RiskAnalysisEngine()
        self.weather = WeatherEngine(CONFIG["WEATHER_API_KEY"])
    
    def dive(self, phone_number):
        """Eksekusi semua modul OSINT"""
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}🔍 OSINT DEEP SCAN: {phone_number}{Colors.END}")
        print(f"{Colors.BLUE}{'='*70}{Colors.END}\n")
        
        # STEP 1: Validasi nomor
        print(f"{Colors.BOLD}[1/10] Validasi nomor...{Colors.END}")
        parsed, info = self.validator.validate(phone_number)
        if not parsed:
            print(f"{Colors.RED}❌ {info}{Colors.END}")
            return None
        
        self.phone_info = info
        print(f"{Colors.GREEN}✅ Nomor valid: {info['international']}{Colors.END}")
        
        # STEP 2: Informasi operator detail
        print(f"\n{Colors.BOLD}[2/10] Informasi operator...{Colors.END}")
        self.carrier_details = self.carrier_engine.get_carrier_details(info['e164'])
        
        # STEP 3: NumLookup API (nama pemilik)
        print(f"\n{Colors.BOLD}[3/10] NumLookup API...{Colors.END}")
        self.numlookup_data = self.numlookup.lookup(info['e164'])
        
        # STEP 4: Telegram
        print(f"\n{Colors.BOLD}[4/10] Telegram...{Colors.END}")
        self.telegram_data = self.telegram.get_username(info['e164'])
        
        # STEP 5: WhatsApp
        print(f"\n{Colors.BOLD}[5/10] WhatsApp...{Colors.END}")
        self.whatsapp_data = self.whatsapp.check_registration(info['e164'])
        
        # STEP 6: Instagram username candidates
        print(f"\n{Colors.BOLD}[6/10] Instagram...{Colors.END}")
        self.instagram_usernames = self.instagram.search_by_phone(self.phone_info)
        
        # STEP 7: Facebook & Signal
        print(f"\n{Colors.BOLD}[7/10] Facebook & Signal...{Colors.END}")
        self.facebook_data = self.facebook.search_by_phone(info['e164'])
        self.signal_data = self.signal.check_registration(info['e164'])
        
        # STEP 8: Email candidates
        print(f"\n{Colors.BOLD}[8/10] Email correlation...{Colors.END}")
        name_hint = self.numlookup_data.get('name') if "error" not in self.numlookup_data else None
        self.email_candidates = self.email.generate_emails(self.phone_info, name_hint)
        
        # STEP 9: Breach check
        print(f"\n{Colors.BOLD}[9/10] Breach check...{Colors.END}")
        if CONFIG["HIBP_API_KEY"] and len(CONFIG["HIBP_API_KEY"]) > 10:
            for email in self.email_candidates[:3]:
                breaches = self.breach.check_email(email)
                if breaches:
                    self.breach_results.extend(breaches)
        
        # STEP 10: Username variants & social search
        print(f"\n{Colors.BOLD}[10/10] Username & social media...{Colors.END}")
        self.username_variants = self.username.generate_all(self.phone_info)
        self.social_results = self.social.search_all_platforms(info['e164'], self.username_variants)
        
        # Informasi lokasi
        self.location_info = self.location_engine.get_location_info(info['e164'], info['location'])
        
        # Analisis risiko
        self.risk_analysis = self.risk.analyze(
            self.phone_info,
            self.telegram_data,
            self.whatsapp_data,
            self.social_results,
            len(self.email_candidates)
        )
        
        # Cuaca (opsional)
        if CONFIG["WEATHER_API_KEY"] and self.location_info.get('city'):
            self.weather_info = self.weather.get_weather(self.location_info['city'])
        
        # Tampilkan hasil
        self.display_results()
        
        return self.get_results()
    
    def display_results(self):
        """Tampilkan semua hasil scan"""
        
        print(f"\n{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}            📊 LAPORAN OSINT LENGKAP{Colors.END}")
        print(f"{Colors.BOLD}{Colors.MAGENTA}{'='*70}{Colors.END}\n")
        
        # SECTION 1: INFORMASI DASAR
        print(f"{Colors.BOLD}{Colors.CYAN}[📱 INFORMASI NOMOR]{Colors.END}")
        print(f"  📞 International : {self.phone_info.get('international', 'N/A')}")
        print(f"  📞 Nasional      : {self.phone_info.get('national', 'N/A')}")
        print(f"  📞 E.164         : {self.phone_info.get('e164', 'N/A')}")
        print(f"  📍 Lokasi        : {self.phone_info.get('location', 'N/A')}")
        print(f"  🕒 Zona Waktu    : {self.phone_info.get('timezone', 'N/A')}")
        print(f"  📱 Tipe Nomor    : {'Mobile' if self.phone_info.get('is_mobile') else 'Fixed/VOIP'}")
        
        # SECTION 2: INFORMASI OPERATOR
        print(f"\n{Colors.BOLD}{Colors.CYAN}[📡 INFORMASI OPERATOR]{Colors.END}")
        print(f"  🏢 Provider      : {self.carrier_details.get('carrier', 'N/A')}")
        print(f"  📶 Jenis Jaringan: {self.carrier_details.get('type', 'N/A')}")
        print(f"  🚀 Generasi      : {self.carrier_details.get('generation', 'N/A')}")
        print(f"  📡 Teknologi     : {self.carrier_details.get('technology', 'N/A')}")
        
        # SECTION 3: DATA PEMILIK (NUMLOOKUP)
        print(f"\n{Colors.BOLD}{Colors.CYAN}[👤 DATA PEMILIK]{Colors.END}")
        if "error" not in self.numlookup_data:
            if self.numlookup_data.get('name'):
                print(f"  👤 Nama          : {Colors.BOLD}{self.numlookup_data['name']}{Colors.END}")
            if self.numlookup_data.get('gender'):
                gender_display = "Laki-laki" if self.numlookup_data['gender'].lower() == 'male' else "Perempuan"
                print(f"  ⚤ Gender        : {gender_display}")
            if self.numlookup_data.get('city'):
                print(f"  🏙️ Kota          : {self.numlookup_data['city']}")
            if self.numlookup_data.get('province'):
                print(f"  🗺️ Provinsi      : {self.numlookup_data['province']}")
            print(f"  📡 Carrier       : {self.numlookup_data.get('carrier', 'N/A')}")
            print(f"  📞 Tipe Line     : {self.numlookup_data.get('line_type', 'N/A')}")
        else:
            print(f"  {Colors.YELLOW}⚠️  {self.numlookup_data.get('error', 'Data tidak tersedia')}{Colors.END}")
            print(f"  {Colors.DIM}   Daftar API key di numlookupapi.com untuk fitur lengkap{Colors.END}")
        
        # SECTION 4: INFORMASI LOKASI (KOORDINAT KOTA)
        print(f"\n{Colors.BOLD}{Colors.CYAN}[🗺️ INFORMASI LOKASI - REFERENSI]{Colors.END}")
        print(f"  🏙️ Kota          : {self.location_info.get('city', 'N/A')}")
        print(f"  🗺️ Provinsi      : {self.location_info.get('province', 'N/A')}")
        print(f"  🕒 Zona Waktu    : {self.location_info.get('timezone', 'N/A')}")
        
        if self.location_info.get('coordinates') and self.location_info['coordinates'].get('lat'):
            coords = self.location_info['coordinates']
            print(f"  🌍 Koordinat     : {coords['lat']}, {coords['lon']} (PUSAT KOTA)")
            print(f"  🗺️ Google Maps   : {coords['google_maps']}")
            print(f"  {Colors.DIM}  ℹ️  Koordinat PUSAT KOTA, BUKAN lokasi individu!{Colors.END}")
        
        # SECTION 5: INFORMASI CUACA (OPSIONAL)
        if self.weather_info and "error" not in self.weather_info:
            print(f"\n{Colors.BOLD}{Colors.CYAN}[☁️ INFORMASI CUACA - PUBLIK]{Colors.END}")
            print(f"  🌡️ Suhu          : {self.weather_info.get('temperature', 'N/A')}")
            print(f"  🌡️ Terasa seperti: {self.weather_info.get('feels_like', 'N/A')}")
            print(f"  💧 Kelembaban   : {self.weather_info.get('humidity', 'N/A')}")
            print(f"  🌀 Cuaca        : {self.weather_info.get('weather', 'N/A')}")
            print(f"  💨 Angin        : {self.weather_info.get('wind_speed', 'N/A')}")
            print(f"  {Colors.DIM}  ℹ️  Data cuaca publik untuk kota, BUKAN data individu{Colors.END}")
        
        # SECTION 6: TELEGRAM
        print(f"\n{Colors.BOLD}{Colors.CYAN}[📨 TELEGRAM]{Colors.END}")
        if self.telegram_data.get('registered'):
            print(f"  ✅ Status        : {Colors.GREEN}TERDAFTAR{Colors.END}")
            print(f"  🆔 Username      : @{Colors.BOLD}{self.telegram_data['username']}{Colors.END}")
            print(f"  🔗 Profile       : {self.telegram_data['profile_url']}")
            print(f"  🔗 Direct Link   : {self.telegram_data['direct_link']}")
        else:
            print(f"  ❌ Status        : {Colors.YELLOW}Tidak terdeteksi atau private{Colors.END}")
            print(f"  🔗 Cek manual    : https://t.me/+{self.phone_info.get('e164', '').replace('+', '')}")
        
        # SECTION 7: WHATSAPP
        print(f"\n{Colors.BOLD}{Colors.CYAN}[💬 WHATSAPP]{Colors.END}")
        if self.whatsapp_data.get('registered'):
            print(f"  ✅ Status        : {Colors.GREEN}TERDAFTAR{Colors.END}")
        else:
            print(f"  ⚠️  Status        : {Colors.YELLOW}Tidak terdeteksi (bisa tetap terdaftar){Colors.END}")
        print(f"  🔗 Link Chat     : {self.whatsapp_data.get('link', 'N/A')}")
        print(f"  🔗 API Link      : {self.whatsapp_data.get('api_link', 'N/A')}")
        
        # SECTION 8: INSTAGRAM
        print(f"\n{Colors.BOLD}{Colors.CYAN}[📸 INSTAGRAM - KEMUNGKINAN USERNAME]{Colors.END}")
        if self.instagram_usernames:
            for i, ig in enumerate(self.instagram_usernames[:7], 1):
                print(f"  {i}. {ig['username']}")
                print(f"     🔗 {ig['search_url']}")
        else:
            print(f"  Tidak ada username yang dihasilkan")
        
        # SECTION 9: FACEBOOK & SIGNAL
        print(f"\n{Colors.BOLD}{Colors.CYAN}[👥 FACEBOOK & SIGNAL]{Colors.END}")
        print(f"  🔍 Facebook Search : {self.facebook_data.get('search_url', 'N/A')}")
        print(f"  🔍 Facebook People : {self.facebook_data.get('people_search', 'N/A')}")
        print(f"  🛡️ Signal Link     : {self.signal_data.get('link', 'N/A')}")
        print(f"  ℹ️  Signal Note     : {self.signal_data.get('note', 'N/A')}")
        
        # SECTION 10: EMAIL CANDIDATES
        print(f"\n{Colors.BOLD}{Colors.CYAN}[📧 EMAIL CANDIDATES]{Colors.END}")
        if self.email_candidates:
            for i, email in enumerate(self.email_candidates[:10], 1):
                print(f"  {i}. {email}")
        else:
            print(f"  Tidak ada email yang dihasilkan")
        
        # SECTION 11: BREACH CHECK
        print(f"\n{Colors.BOLD}{Colors.CYAN}[💀 DATA BREACH CHECK]{Colors.END}")
        if self.breach_results:
            print(f"  {Colors.RED}⚠️  Ditemukan {len(self.breach_results)} kebocoran data!{Colors.END}")
            for i, breach in enumerate(self.breach_results[:5], 1):
                print(f"  {i}. {breach['name']} ({breach['date']})")
                print(f"     {breach['description'][:80]}...")
        else:
            if CONFIG["HIBP_API_KEY"]:
                print(f"  ✅ Tidak ditemukan kebocoran data di HIBP")
            else:
                print(f"  {Colors.YELLOW}⚠️  HIBP API key kosong. Daftar di haveibeenpwned.com/API/Key{Colors.END}")
        
        # SECTION 12: USERNAME VARIANTS
        print(f"\n{Colors.BOLD}{Colors.CYAN}[🔑 USERNAME VARIANTS]{Colors.END}")
        print(f"  {Colors.DIM}Coba cari username ini di Twitter, TikTok, dll:{Colors.END}")
        if self.username_variants:
            for i, uname in enumerate(self.username_variants[:10], 1):
                print(f"  {i}. {uname}")
        
        # SECTION 13: PENCARIAN SOSIAL MEDIA
        print(f"\n{Colors.BOLD}{Colors.CYAN}[🌐 LINK PENCARIAN SOSIAL MEDIA]{Colors.END}")
        platforms_shown = {}
        for result in self.social_results[:20]:
            platform = result['platform']
            if platform not in platforms_shown:
                platforms_shown[platform] = True
                if result['type'] == 'direct':
                    print(f"  {platform:15}: {result['search_url']}")
                else:
                    print(f"  {platform:15}: {result['search_url']}")
        
        # SECTION 14: ANALISIS RISIKO
        print(f"\n{Colors.BOLD}{Colors.CYAN}[⚠️ ANALISIS RISIKO PRIVASI]{Colors.END}")
        print(f"  Level Risiko    : {self.risk_analysis.get('risk_level', 'N/A')}")
        print(f"  Skor Risiko     : {self.risk_analysis.get('risk_score', 0)}/100")
        
        if self.risk_analysis.get('risk_factors'):
            print(f"  Faktor Risiko   :")
            for factor in self.risk_analysis['risk_factors']:
                print(f"    • {factor}")
        
        if self.risk_analysis.get('recommendations'):
            print(f"  Rekomendasi     :")
            for rec in self.risk_analysis['recommendations']:
                print(f"    • {rec}")
        
        if self.risk_analysis.get('platforms_detected'):
            print(f"  Platform Terdeteksi: {', '.join(self.risk_analysis['platforms_detected'][:7])}")
        
        # FOOTER
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"\n{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}  ✅ SCAN SELESAI! Waktu: {elapsed:.2f} detik{Colors.END}")
        print(f"{Colors.BOLD}  🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB{Colors.END}")
        print(f"{Colors.BOLD}  👑 Author: mrx-n15 (Zamxyz){Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}{'='*70}{Colors.END}")
        
        # PERINGATAN
        print(f"\n{Colors.BOLD}{Colors.YELLOW}═══════════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}  ⚠️  PERINGATAN: Gunakan untuk edukasi & authorized testing!{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}  ⚠️  DILARANG untuk doxing, stalking, atau kejahatan lainnya!{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}  ⚠️  Allah SWT Maha Melihat!{Colors.END}")
        print(f"{Colors.BOLD}{Colors.YELLOW}═══════════════════════════════════════════════════════════{Colors.END}\n")
    
    def get_results(self):
        """Kumpulkan semua hasil untuk export"""
        return {
            "phone_info": self.phone_info,
            "carrier_details": self.carrier_details,
            "numlookup": self.numlookup_data,
            "location_info": self.location_info,
            "weather_info": self.weather_info,
            "telegram": self.telegram_data,
            "whatsapp": self.whatsapp_data,
            "instagram": self.instagram_usernames,
            "facebook": self.facebook_data,
            "signal": self.signal_data,
            "emails": self.email_candidates,
            "breaches": self.breach_results,
            "usernames": self.username_variants,
            "social_links": self.social_results,
            "risk_analysis": self.risk_analysis,
            "scan_time": self.start_time.isoformat(),
            "duration": (datetime.now() - self.start_time).total_seconds()
        }
    
    def export_csv(self, filename=None):
        """Export hasil ke CSV"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/quantum_report_{timestamp}.csv"
        
        os.makedirs('output', exist_ok=True)
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            
            writer.writerow(['=== QUANTUM PHONE DIVER REPORT ==='])
            writer.writerow(['Target', self.phone_info.get('e164', 'N/A')])
            writer.writerow(['Waktu', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow([])
            
            writer.writerow(['📱 INFORMASI NOMOR'])
            writer.writerow(['International', self.phone_info.get('international', 'N/A')])
            writer.writerow(['Nasional', self.phone_info.get('national', 'N/A')])
            writer.writerow(['Lokasi', self.phone_info.get('location', 'N/A')])
            writer.writerow(['Operator', self.phone_info.get('carrier', 'N/A')])
            writer.writerow([])
            
            writer.writerow(['📡 INFORMASI OPERATOR'])
            writer.writerow(['Provider', self.carrier_details.get('carrier', 'N/A')])
            writer.writerow(['Jaringan', self.carrier_details.get('type', 'N/A')])
            writer.writerow(['Generasi', self.carrier_details.get('generation', 'N/A')])
            writer.writerow([])
            
            writer.writerow(['👤 DATA PEMILIK'])
            if "error" not in self.numlookup_data:
                writer.writerow(['Nama', self.numlookup_data.get('name', 'N/A')])
                writer.writerow(['Gender', self.numlookup_data.get('gender', 'N/A')])
                writer.writerow(['Kota', self.numlookup_data.get('city', 'N/A')])
                writer.writerow(['Provinsi', self.numlookup_data.get('province', 'N/A')])
            writer.writerow([])
            
            writer.writerow(['📨 TELEGRAM'])
            writer.writerow(['Status', 'Terdaftar' if self.telegram_data.get('registered') else 'Tidak terdeteksi'])
            writer.writerow(['Username', self.telegram_data.get('username', 'N/A')])
            writer.writerow(['Profile', self.telegram_data.get('profile_url', 'N/A')])
            writer.writerow([])
            
            writer.writerow(['📧 EMAIL CANDIDATES'])
            for email in self.email_candidates[:15]:
                writer.writerow(['Email', email])
            writer.writerow([])
            
            writer.writerow(['🔑 USERNAME VARIANTS'])
            for uname in self.username_variants[:15]:
                writer.writerow(['Username', uname])
        
        print(f"{Colors.GREEN}✅ CSV report: {filename}{Colors.END}")
        return filename
    
    def export_html(self, filename=None):
        """Export hasil ke HTML"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"output/quantum_report_{timestamp}.html"
        
        os.makedirs('output', exist_ok=True)
        
        # HTML template
        html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Phone Diver Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            background: linear-gradient(135deg, #0a0f1e 0%, #1a1f2e 100%);
            color: #00ff9d;
            font-family: 'Courier New', monospace;
            padding: 30px 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(10, 15, 30, 0.8);
            border: 2px solid #00ff9d;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 0 30px rgba(0, 255, 157, 0.2);
            backdrop-filter: blur(5px);
        }}
        
        h1 {{
            color: #ff00c1;
            text-align: center;
            font-size: 28px;
            margin-bottom: 10px;
            text-shadow: 0 0 10px rgba(255, 0, 193, 0.5);
            border-bottom: 2px solid #00ff9d;
            padding-bottom: 20px;
        }}
        
        h2 {{
            color: #00ff9d;
            font-size: 20px;
            margin: 25px 0 15px;
            padding-left: 10px;
            border-left: 5px solid #ff00c1;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        
        .info-box {{
            background: rgba(0, 255, 157, 0.05);
            border: 1px solid #00ff9d;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s ease;
        }}
        
        .info-box:hover {{
            background: rgba(0, 255, 157, 0.1);
            box-shadow: 0 0 20px rgba(0, 255, 157, 0.3);
            transform: translateY(-2px);
        }}
        
        .info-label {{
            color: #ff00c1;
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .info-value {{
            color: #00ff9d;
            font-size: 16px;
            word-break: break-word;
        }}
        
        .risk-high {{
            color: #ff4444;
            font-weight: bold;
            padding: 5px 10px;
            background: rgba(255, 68, 68, 0.2);
            border-radius: 5px;
        }}
        
        .risk-medium {{
            color: #ffaa00;
            font-weight: bold;
            padding: 5px 10px;
            background: rgba(255, 170, 0, 0.2);
            border-radius: 5px;
        }}
        
        .risk-low {{
            color: #00ff9d;
            font-weight: bold;
            padding: 5px 10px;
            background: rgba(0, 255, 157, 0.2);
            border-radius: 5px;
        }}
        
        .table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        
        .table td {{
            padding: 10px;
            border: 1px solid #00ff9d;
            color: #00ff9d;
        }}
        
        .table tr:hover {{
            background: rgba(0, 255, 157, 0.1);
        }}
        
        .footer {{
            margin-top: 40px;
            text-align: center;
            color: #666;
            border-top: 1px solid #00ff9d;
            padding-top: 20px;
            font-size: 12px;
        }}
        
        .warning {{
            background: rgba(255, 0, 0, 0.1);
            border: 1px solid #ff4444;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            color: #ff8888;
            text-align: center;
        }}
        
        .timestamp {{
            color: #888;
            text-align: right;
            font-size: 12px;
            margin-bottom: 20px;
        }}
        
        a {{
            color: #ff00c1;
            text-decoration: none;
            border-bottom: 1px dashed #ff00c1;
        }}
        
        a:hover {{
            color: #00ff9d;
            border-bottom: 1px solid #00ff9d;
        }}
        
        .glitch {{
            animation: glitch 3s infinite;
        }}
        
        @keyframes glitch {{
            0%, 100% {{ text-shadow: 2px 0 0 rgba(255, 0, 193, 0.3), -2px 0 0 rgba(0, 255, 157, 0.3); }}
            25% {{ text-shadow: -2px 0 0 rgba(255, 0, 193, 0.3), 2px 0 0 rgba(0, 255, 157, 0.3); }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1 class="glitch">🔍 QUANTUM PHONE DIVER v4.0</h1>
        <h1 style="font-size: 18px; color: #00ff9d;">DEEP OSINT LEGAL EDITION</h1>
        
        <div class="timestamp">
            📅 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WIB<br>
            ⏱️ Duration: {self.get_results()['duration']:.2f} seconds
        </div>
        
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">📱 TARGET</div>
                <div class="info-value">{self.phone_info.get('international', 'N/A')}</div>
                <div class="info-value" style="font-size: 12px; color: #888;">{self.phone_info.get('national', 'N/A')}</div>
            </div>
            
            <div class="info-box">
                <div class="info-label">📍 LOKASI</div>
                <div class="info-value">{self.phone_info.get('location', 'N/A')}</div>
                <div class="info-value" style="font-size: 12px; color: #888;">{self.phone_info.get('timezone', 'N/A')}</div>
            </div>
            
            <div class="info-box">
                <div class="info-label">📡 OPERATOR</div>
                <div class="info-value">{self.carrier_details.get('carrier', 'N/A')}</div>
                <div class="info-value" style="font-size: 12px; color: #888;">{self.carrier_details.get('generation', 'N/A')}</div>
            </div>
        </div>
        
        <h2>👤 DATA PEMILIK</h2>
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">Nama</div>
                <div class="info-value">{self.numlookup_data.get('name', 'Tidak tersedia') if 'error' not in self.numlookup_data else 'API key required'}</div>
            </div>
            <div class="info-box">
                <div class="info-label">Gender</div>
                <div class="info-value">{self.numlookup_data.get('gender', '-') if 'error' not in self.numlookup_data else '-'}</div>
            </div>
            <div class="info-box">
                <div class="info-label">Kota</div>
                <div class="info-value">{self.numlookup_data.get('city', '-') if 'error' not in self.numlookup_data else '-'}</div>
            </div>
        </div>
        
        <h2>🗺️ INFORMASI LOKASI (REFERENSI)</h2>
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">Kota</div>
                <div class="info-value">{self.location_info.get('city', 'N/A')}</div>
            </div>
            <div class="info-box">
                <div class="info-label">Provinsi</div>
                <div class="info-value">{self.location_info.get('province', 'N/A')}</div>
            </div>
            <div class="info-box">
                <div class="info-label">Zona Waktu</div>
                <div class="info-value">{self.location_info.get('timezone', 'N/A')}</div>
            </div>
        </div>
        
        {f'''
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">🌍 Koordinat (PUSAT KOTA)</div>
                <div class="info-value">{self.location_info['coordinates']['lat']}, {self.location_info['coordinates']['lon']}</div>
                <div class="info-value" style="font-size: 12px; margin-top: 10px;">
                    <a href="{self.location_info['coordinates']['google_maps']}" target="_blank">🔗 Buka di Google Maps</a>
                </div>
                <div style="color: #888; font-size: 11px; margin-top: 10px;">
                    ⚠️ Koordinat PUSAT KOTA, BUKAN lokasi individu!
                </div>
            </div>
        </div>
        ''' if self.location_info.get('coordinates') and self.location_info['coordinates'].get('lat') else ''}
        
        {f'''
        <h2>☁️ INFORMASI CUACA - {self.location_info.get('city', '')}</h2>
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">🌡️ Suhu</div>
                <div class="info-value">{self.weather_info.get('temperature', 'N/A')}</div>
            </div>
            <div class="info-box">
                <div class="info-label">🌡️ Terasa</div>
                <div class="info-value">{self.weather_info.get('feels_like', 'N/A')}</div>
            </div>
            <div class="info-box">
                <div class="info-label">💧 Kelembaban</div>
                <div class="info-value">{self.weather_info.get('humidity', 'N/A')}</div>
            </div>
            <div class="info-box">
                <div class="info-label">🌀 Cuaca</div>
                <div class="info-value">{self.weather_info.get('weather', 'N/A')}</div>
            </div>
        </div>
        <div style="color: #888; font-size: 11px; text-align: right; margin-top: 5px;">
            Data cuaca publik dari OpenWeatherMap
        </div>
        ''' if self.weather_info and 'error' not in self.weather_info else ''}
        
        <h2>📨 TELEGRAM</h2>
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">Status</div>
                <div class="info-value">{'✅ TERDAFTAR' if self.telegram_data.get('registered') else '❌ Tidak terdeteksi'}</div>
            </div>
            {f'''
            <div class="info-box">
                <div class="info-label">🆔 Username</div>
                <div class="info-value">@{self.telegram_data.get('username', '')}</div>
            </div>
            <div class="info-box">
                <div class="info-label">🔗 Profile</div>
                <div class="info-value"><a href="{self.telegram_data.get('profile_url', '#')}" target="_blank">Buka Telegram</a></div>
            </div>
            ''' if self.telegram_data.get('registered') else ''}
        </div>
        
        <h2>💬 WHATSAPP</h2>
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">Status</div>
                <div class="info-value">{'✅ Terdaftar' if self.whatsapp_data.get('registered') else '⚠️ Tidak terdeteksi'}</div>
            </div>
            <div class="info-box">
                <div class="info-label">🔗 Link Chat</div>
                <div class="info-value"><a href="{self.whatsapp_data.get('link', '#')}" target="_blank">Buka WhatsApp</a></div>
            </div>
        </div>
        
        <h2>📧 EMAIL CANDIDATES</h2>
        <table class="table">
            {''.join([f'<tr><td>{i}.</td><td>{email}</td></tr>' for i, email in enumerate(self.email_candidates[:10], 1)])}
        </table>
        
        <h2>🔑 USERNAME VARIANTS</h2>
        <table class="table">
            {''.join([f'<tr><td>{i}.</td><td>{uname}</td><td style="color: #888;">🔍 Cari di sosial media</td></tr>' for i, uname in enumerate(self.username_variants[:10], 1)])}
        </table>
        
        <h2>⚠️ ANALISIS RISIKO PRIVASI</h2>
        <div class="info-grid">
            <div class="info-box">
                <div class="info-label">Level Risiko</div>
                <div class="info-value">
                    <span class="{'risk-high' if 'TINGGI' in self.risk_analysis.get('risk_level', '') else 'risk-medium' if 'SEDANG' in self.risk_analysis.get('risk_level', '') else 'risk-low'}">
                        {self.risk_analysis.get('risk_level', 'N/A')}
                    </span>
                </div>
            </div>
            <div class="info-box">
                <div class="info-label">Skor Risiko</div>
                <div class="info-value">{self.risk_analysis.get('risk_score', 0)}/100</div>
            </div>
        </div>
        
        {f'''
        <div class="info-box" style="margin-top: 15px;">
            <div class="info-label">⚠️ Faktor Risiko</div>
            <ul style="color: #ff8888; margin-left: 20px;">
                {''.join([f'<li style="margin: 5px 0;">{factor}</li>' for factor in self.risk_analysis.get('risk_factors', [])])}
            </ul>
        </div>
        
        <div class="info-box" style="margin-top: 15px;">
            <div class="info-label">💡 Rekomendasi</div>
            <ul style="color: #00ff9d; margin-left: 20px;">
                {''.join([f'<li style="margin: 5px 0;">{rec}</li>' for rec in self.risk_analysis.get('recommendations', [])])}
            </ul>
        </div>
        ''' if self.risk_analysis.get('risk_factors') else ''}
        
        <div class="warning">
            ⚠️ PERINGATAN: Tools ini untuk EDUKASI dan AUTHORIZED TESTING saja!<br>
            DILARANG digunakan untuk doxing, stalking, atau kejahatan siber lainnya!<br>
            Allah SWT Maha Melihat lagi Maha Mengetahui.
        </div>
        
        <div class="footer">
            <p>© 2026 mrx-n15 (Zamxyz) - Islamic MIT License</p>
            <p>Anonymous Cyber Muslim Indonesia | Lillahi Ta'ala</p>
            <p style="margin-top: 10px;">"Dan janganlah kamu mencari-cari kesalahan orang lain" (QS. Al-Hujurat: 12)</p>
        </div>
    </div>
</body>
</html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"{Colors.GREEN}✅ HTML report: {filename}{Colors.END}")
        return filename

# ==================== VALIDASI API KEY ====================
def validate_api_keys():
    """Validasi API key dan kasih peringatan"""
    
    print(f"{Colors.BOLD}{Colors.YELLOW}🔑 Validasi API Keys...{Colors.END}")
    
    valid = True
    
    if not CONFIG["NUMLOOKUP_API_KEY"]:
        print(f"{Colors.YELLOW}  ⚠️  NumLookup API key: KOSONG{Colors.END}")
        print(f"{Colors.DIM}     → Fitur nama pemilik & data lengkap TIDAK AKTIF{Colors.END}")
        print(f"{Colors.DIM}     → Daftar gratis: https://numlookupapi.com{Colors.END}")
        valid = False
    else:
        print(f"{Colors.GREEN}  ✅ NumLookup API key: TERISI{Colors.END}")
    
    if not CONFIG["HIBP_API_KEY"]:
        print(f"{Colors.YELLOW}  ⚠️  HIBP API key: KOSONG{Colors.END}")
        print(f"{Colors.DIM}     → Fitur breach checker TIDAK AKTIF{Colors.END}")
        print(f"{Colors.DIM}     → Daftar gratis: https://haveibeenpwned.com/API/Key{Colors.END}")
        valid = False
    else:
        print(f"{Colors.GREEN}  ✅ HIBP API key: TERISI{Colors.END}")
    
    if not CONFIG["WEATHER_API_KEY"]:
        print(f"{Colors.DIM}  ℹ️  Weather API key: KOSONG (opsional){Colors.END}")
    else:
        print(f"{Colors.GREEN}  ✅ Weather API key: TERISI{Colors.END}")
    
    print()
    return valid

# ==================== KONFIGURASI INTERAKTIF ====================
def interactive_config():
    """Menu konfigurasi API key interaktif"""
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}🔧 KONFIGURASI API KEY{Colors.END}")
    print(f"{'='*50}")
    
    print(f"\n{Colors.BOLD}1. NUMLOOKUP API (WAJIB untuk fitur lengkap){Colors.END}")
    print(f"   Daftar: https://numlookupapi.com")
    api_key = input(f"   Paste API key: ").strip()
    if api_key:
        CONFIG["NUMLOOKUP_API_KEY"] = api_key
    
    print(f"\n{Colors.BOLD}2. HIBP API (WAJIB untuk cek breach){Colors.END}")
    print(f"   Daftar: https://haveibeenpwned.com/API/Key")
    api_key = input(f"   Paste API key: ").strip()
    if api_key:
        CONFIG["HIBP_API_KEY"] = api_key
    
    print(f"\n{Colors.BOLD}3. WEATHER API (OPSIONAL - untuk info cuaca){Colors.END}")
    print(f"   Daftar: https://openweathermap.org/api")
    api_key = input(f"   Paste API key (Enter untuk skip): ").strip()
    if api_key:
        CONFIG["WEATHER_API_KEY"] = api_key
    
    # Simpan ke file
    save_config()
    
    print(f"\n{Colors.GREEN}✅ Konfigurasi berhasil disimpan!{Colors.END}")

def save_config():
    """Simpan konfigurasi ke file config.py"""
    try:
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(f'''# QUANTUM PHONE DIVER - KONFIGURASI API
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
# DILARANG SHARE FILE INI!

CONFIG = {{
    # NumLookup API - https://numlookupapi.com
    "NUMLOOKUP_API_KEY": "{CONFIG['NUMLOOKUP_API_KEY']}",
    
    # HIBP API - https://haveibeenpwned.com/API/Key
    "HIBP_API_KEY": "{CONFIG['HIBP_API_KEY']}",
    
    # OpenWeatherMap API - https://openweathermap.org/api
    "WEATHER_API_KEY": "{CONFIG['WEATHER_API_KEY']}",
}}
''')
        return True
    except:
        return False

# ==================== FUNGSI UTAMA ====================
def main():
    """Main function"""
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Tampilkan banner
    print(BANNER)
    
    # Validasi API key
    validate_api_keys()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='Quantum Phone Diver v4.0 - OSINT Telephone Tool')
    parser.add_argument('-p', '--phone', help='Nomor telepon target (format: +62812xxxx)')
    parser.add_argument('-o', '--output', choices=['csv', 'html', 'both'], help='Format export laporan')
    parser.add_argument('--config', action='store_true', help='Mode konfigurasi API key')
    
    args = parser.parse_args()
    
    # Mode konfigurasi
    if args.config:
        interactive_config()
        return
    
    # Mode scan
    if args.phone:
        # Validasi nomor
        if not args.phone.startswith('+'):
            print(f"{Colors.RED}❌ ERROR: Nomor harus dalam format internasional (contoh: +62812xxxx){Colors.END}")
            return
        
        # Mulai scan
        diver = QuantumPhoneDiver()
        results = diver.dive(args.phone)
        
        # Export jika diminta
        if results and args.output:
            print(f"\n{Colors.CYAN}📁 Exporting reports...{Colors.END}")
            if args.output in ['csv', 'both']:
                diver.export_csv()
            if args.output in ['html', 'both']:
                diver.export_html()
    
    else:
        # Tampilkan help
        print(f"{Colors.BOLD}{Colors.CYAN}📌 CARA PAKAI:{Colors.END}")
        print(f"  python quantum-phone-diver.py -p \"+6281234567890\"")
        print(f"  python quantum-phone-diver.py -p \"+6281234567890\" -o both")
        print(f"  python quantum-phone-diver.py --config")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Interrupted by user{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error: {e}{Colors.END}")
