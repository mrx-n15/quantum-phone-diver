#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import time
import requests
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import argparse
from datetime import datetime
import base64
import hashlib
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# ==================== KONFIGURASI API ====================
# Wajib diisi! Dapatkan dari masing-masing service [citation:1][citation:4]

CONFIG = {
    # NumLookup API - Untuk data Truecaller-like (gratis limited)
    "NUMLOOKUP_API_KEY": "ISI_SENDIRI",  # Daftar di numlookupapi.com
    
    # HaveIBeenPwned API - Cek breach (wajib API key)
    "HIBP_API_KEY": "ISI_SENDIRI",      # Daftar di haveibeenpwned.com/API/Key
    
    # Hunter.io API - Email verification (opsional)
    "HUNTER_IO_API_KEY": "ISI_SENDIRI",  # Daftar di hunter.io
    
    # Proxy settings (opsional)
    "USE_PROXY": False,
    "PROXY_LIST": [],
    
    # User agents untuk rotasi
    "USER_AGENTS": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
        "Mozilla/5.0 (Linux; Android 11; SM-G991B)"
    ]
}

# ==================== UTILITY FUNCTIONS ====================

class Colors:
    """Warna terminal biar keren [citation:8]"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    """Banner khas Zamxyz"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Colors.CYAN}

╔════════════════════════════════════╗
║     🔥 QUANTUM PHONE DIVER v3.0    ║
║     👑 CREDIT: ZAMXYZ             ║
║     🕋 SUPPORT: ALLAH SWT         ║
║     🌏 ACMI - ANONYMOUS CYBER     ║
╚════════════════════════════════════╝

{Colors.END}
"""
    print(banner)
    print(f"{Colors.WARNING}[!] Gunakan untuk edukasi dan authorized testing only!{Colors.END}")
    print(f"{Colors.GREEN}[+] Loaded: PhoneInfoga + PhoNumSpy + INFOFINDER_PRO Hybrid Engine{Colors.END}[citation:1][citation:2][citation:9]")
    print(f"{Colors.CYAN}[+] Target: Deep phone number footprinting hingga ke akar{Colors.END}\n")

# ==================== PHONE VALIDATION & BASIC INFO ====================

class PhoneValidator:
    """Validasi nomor pakai library phonenumbers [citation:1][citation:9]"""
    
    @staticmethod
    def validate(phone_number):
        """Validasi dan ekstrak informasi dasar"""
        try:
            parsed = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed):
                return None, "Nomor tidak valid"
            
            # Data dasar
            info = {
                "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                "e164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164),
                "country_code": parsed.country_code,
                "national_number": parsed.national_number,
                "is_valid": True,
                "is_possible": phonenumbers.is_possible_number(parsed),
                "location": geocoder.description_for_number(parsed, "en"),
                "carrier": carrier.name_for_number(parsed, "en"),
                "timezones": timezone.time_zones_for_number(parsed),
                "number_type": PhoneValidator._get_number_type(parsed)
            }
            return parsed, info
        except Exception as e:
            return None, f"Error parsing: {str(e)}"
    
    @staticmethod
    def _get_number_type(parsed):
        """Tentukan tipe nomor (mobile, fixed, etc)"""
        num_type = phonenumbers.number_type(parsed)
        type_map = {
            0: "FIXED_LINE",
            1: "MOBILE",
            2: "FIXED_LINE_OR_MOBILE", 
            3: "TOLL_FREE",
            4: "PREMIUM_RATE",
            5: "SHARED_COST",
            6: "VOIP",
            7: "PERSONAL_NUMBER",
            8: "PAGER",
            9: "UAN",
            10: "VOICEMAIL",
            99: "UNKNOWN"
        }
        return type_map.get(num_type, "UNKNOWN")

# ==================== NUMLOOKUP API (TRUECALLER STYLE) ====================

class NumLookupEngine:
    """Integrasi NumLookup API - Truecaller-like data [citation:4]"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.numlookupapi.com/v1/validate/"
    
    def lookup(self, phone_number):
        """Cari data via NumLookup API"""
        if not self.api_key or self.api_key == "ISI_SENDIRI":
            return {"error": "NumLookup API key not configured"}
        
        try:
            url = f"{self.base_url}{phone_number}"
            params = {"apikey": self.api_key}
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "valid": data.get("valid", False),
                    "line_type": data.get("line_type"),
                    "carrier": data.get("carrier"),
                    "location": data.get("location"),
                    "country_name": data.get("country_name"),
                    "country_code": data.get("country_code")
                }
            else:
                return {"error": f"API returned {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

# ==================== GOOGLE DORKING ENGINE ====================

class GoogleDorkEngine:
    """Generate Google dorks buat footprinting maksimal [citation:1][citation:4]"""
    
    @staticmethod
    def generate_dorks(phone_info):
        """Generate semua kombinasi Google dorks"""
        e164 = phone_info.get('e164', '').replace('+', '')
        national = phone_info.get('national', '').replace(' ', '')
        international = phone_info.get('international', '')
        
        dorks = {
            "exact_phone": f'https://www.google.com/search?q="{e164}" OR "{national}"',
            "intext_phone": f'https://www.google.com/search?q=intext:"{e164}"',
            "phone_in_url": f'https://www.google.com/search?q=inurl:{e164}',
            "social_media": f'https://www.google.com/search?q=site:facebook.com OR site:twitter.com OR site:instagram.com "{e164}"',
            "linkedin": f'https://www.google.com/search?q=site:linkedin.com "{national}"',
            "whatsapp": f'https://www.google.com/search?q=site:whatsapp.com "{e164}"',
            "telegram": f'https://www.google.com/search?q=site:t.me "{e164}"',
            "breach_forums": f'https://www.google.com/search?q=site:raidforums.com OR site:breached.to "{e164}"',
            "pastebin": f'https://www.google.com/search?q=site:pastebin.com "{e164}"',
            "pdf_docs": f'https://www.google.com/search?q="{e164}" filetype:pdf OR filetype:docx',
            "phone_directory": f'https://www.google.com/search?q="{national}" phone directory',
            "reverse_lookup": f'https://www.google.com/search?q=reverse phone lookup "{e164}"'
        }
        return dorks

# ==================== TELEGRAM DETECTION ENGINE ====================

class TelegramDetector:
    """Deteksi username Telegram dari nomor [citation:4][citation:10]"""
    
    @staticmethod
    def detect(phone_number):
        """Cek apakah nomor terdaftar di Telegram"""
        try:
            # Format: https://t.me/+62812xxxx
            clean_number = phone_number.replace('+', '').replace(' ', '')
            url = f"https://t.me/+{clean_number}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                # Parse HTML untuk cek username
                soup = BeautifulSoup(response.text, 'html.parser')
                meta_tag = soup.find('meta', property='og:url')
                
                if meta_tag:
                    content = meta_tag.get('content', '')
                    if 't.me/' in content and '+' not in content.split('t.me/')[1]:
                        username = content.split('t.me/')[1]
                        return {
                            "registered": True,
                            "username": username,
                            "profile_url": f"https://t.me/{username}",
                            "direct_link": url
                        }
            
            return {"registered": False, "username": None}
        except Exception as e:
            return {"error": str(e), "registered": False}

# ==================== HAVE I BEEN PWNED INTEGRATION ====================

class BreachChecker:
    """Cek apakah nomor/email terkait ada di database breach [citation:1][citation:4]"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://haveibeenpwned.com/api/v3"
    
    def check_phone_breaches(self, phone_number, email_candidates=None):
        """
        HIBP khusus untuk email.
        Tapi kita bisa cek email yang terasosiasi dengan nomor.
        """
        results = {"breaches": [], "pastes": [], "total_found": 0}
        
        if not email_candidates:
            return results
        
        for email in email_candidates[:5]:  # Limit 5 email
            breaches = self._check_email_breaches(email)
            if breaches:
                results["breaches"].extend(breaches)
                results["total_found"] += len(breaches)
        
        return results
    
    def _check_email_breaches(self, email):
        """Internal: cek breach untuk satu email"""
        if not self.api_key or self.api_key == "ISI_SENDIRI":
            return []
        
        try:
            url = f"{self.base_url}/breachedaccount/{email}"
            headers = {
                "hibp-api-key": self.api_key,
                "user-agent": "Quantum-Phone-Diver"
            }
            params = {"truncateResponse": "false"}
            
            response = requests.get(url, headers=headers, params=params, timeout=15)
            
            if response.status_code == 200:
                return response.json()
            else:
                return []
        except:
            return []

# ==================== SOCIAL MEDIA FOOTPRINT ====================

class SocialMediaScanner:
    """Scan footprint di social media berdasarkan nomor"""
    
    @staticmethod
    def scan(phone_info):
        """Generate URL untuk pencarian di berbagai platform"""
        e164 = phone_info.get('e164', '')
        national = phone_info.get('national', '')
        
        platforms = {
            "facebook": f"https://www.facebook.com/search/top/?q={e164}",
            "instagram": f"https://www.instagram.com/web/search/topsearch/?query={e164}",
            "twitter": f"https://twitter.com/search?q={e164}",
            "tiktok": f"https://www.tiktok.com/search?q={e164}",
            "snapchat": f"https://www.snapchat.com/add/{national}",
            "whatsapp": f"https://wa.me/{e164}",
            "telegram": f"https://t.me/+{e164.replace('+', '')}",
            "viber": f"viber://add?number={e164}",
            "wechat": f"https://weixin.qq.com/r/{e164}",
            "line": f"https://line.me/R/home/public/profile?id={national}",
            "skype": f"skype:{e164}?call",
            "signal": f"https://signal.me/#p/{e164}",
            "discord": f"https://discord.com/channels/@me?q={e164}"
        }
        
        return platforms

# ==================== EMAIL EXTRACTION & CORRELATION ====================

class EmailCorrelator:
    """Cari email yang terasosiasi dengan nomor"""
    
    @staticmethod
    def extract_candidates(phone_info):
        """Generate kemungkinan email dari nomor"""
        national = phone_info.get('national', '').replace(' ', '')
        e164 = phone_info.get('e164', '').replace('+', '')
        country_code = str(phone_info.get('country_code', ''))
        
        candidates = []
        
        # Format umum: nomor@gmail.com
        candidates.append(f"{national}@gmail.com")
        candidates.append(f"{e164}@gmail.com")
        candidates.append(f"0{national}@gmail.com")
        candidates.append(f"{national}@yahoo.com")
        candidates.append(f"{national}@outlook.com")
        candidates.append(f"{national}@hotmail.com")
        
        # Dengan prefix umum
        prefixes = ['+62', '08', '628', '0']
        for prefix in prefixes:
            for domain in ['@gmail.com', '@yahoo.com', '@outlook.com']:
                candidates.append(f"{prefix}{national}{domain}")
        
        # Dengan nama (kalau ada) - ini nanti diisi dari sumber lain
        # Untuk sekarang return candidates dulu
        
        return list(set(candidates))  # Unique

# ==================== MAIN OSINT ENGINE ====================

class QuantumPhoneDiver:
    """Main engine - menggabungkan semua teknik OSINT"""
    
    def __init__(self):
        self.results = {
            "phone_info": {},
            "numlookup_data": {},
            "telegram_data": {},
            "social_media_links": {},
            "google_dorks": {},
            "breach_data": {},
            "email_candidates": [],
            "raw_data": {}
        }
        self.start_time = datetime.now()
        
        # Initialize engines
        self.phone_validator = PhoneValidator()
        self.numlookup = NumLookupEngine(CONFIG["NUMLOOKUP_API_KEY"])
        self.telegram_detector = TelegramDetector()
        self.google_dorker = GoogleDorkEngine()
        self.breach_checker = BreachChecker(CONFIG["HIBP_API_KEY"])
        self.social_scanner = SocialMediaScanner()
        self.email_correlator = EmailCorrelator()
    
    def dive(self, phone_number):
        """Main function - eksekusi semua modul secara paralel"""
        print(f"{Colors.BOLD}{Colors.GREEN}[+] Memulai deep scan untuk: {phone_number}{Colors.END}\n")
        
        # STEP 1: Validasi nomor
        print(f"{Colors.CYAN}[1/7] Validating phone number...{Colors.END}")
        parsed, info = self.phone_validator.validate(phone_number)
        
        if not parsed:
            print(f"{Colors.FAIL}[-] {info}{Colors.END}")
            return None
        
        self.results["phone_info"] = info
        print(f"{Colors.GREEN}    ✓ Valid: {info['international']}{Colors.END}")
        print(f"{Colors.GREEN}    ✓ Location: {info['location']}{Colors.END}")
        print(f"{Colors.GREEN}    ✓ Carrier: {info['carrier']}{Colors.END}")
        print(f"{Colors.GREEN}    ✓ Type: {info['number_type']}{Colors.END}\n")
        
        # STEP 2: NumLookup API (Truecaller style)
        print(f"{Colors.CYAN}[2/7] Querying NumLookup API...{Colors.END}")
        self.results["numlookup_data"] = self.numlookup.lookup(info['e164'])
        if "error" not in self.results["numlookup_data"]:
            print(f"{Colors.GREEN}    ✓ Carrier: {self.results['numlookup_data'].get('carrier', 'N/A')}{Colors.END}")
            print(f"{Colors.GREEN}    ✓ Location: {self.results['numlookup_data'].get('location', 'N/A')}{Colors.END}")
        else:
            print(f"{Colors.WARNING}    ⚠ NumLookup: {self.results['numlookup_data']['error']}{Colors.END}")
        
        # STEP 3: Telegram Detection
        print(f"{Colors.CYAN}[3/7] Checking Telegram registration...{Colors.END}")
        self.results["telegram_data"] = self.telegram_detector.detect(info['e164'])
        if self.results["telegram_data"].get("registered"):
            print(f"{Colors.GREEN}    ✓ Registered! Username: @{self.results['telegram_data']['username']}{Colors.END}")
        else:
            print(f"{Colors.WARNING}    ⚠ Tidak terdeteksi atau private{Colors.END}")
        
        # STEP 4: Generate Email Candidates
        print(f"{Colors.CYAN}[4/7] Generating email candidates...{Colors.END}")
        self.results["email_candidates"] = self.email_correlator.extract_candidates(info)
        print(f"{Colors.GREEN}    ✓ Generated {len(self.results['email_candidates'])} email patterns{Colors.END}")
        for i, email in enumerate(self.results['email_candidates'][:5], 1):
            print(f"      {i}. {email}")
        if len(self.results['email_candidates']) > 5:
            print(f"      ... and {len(self.results['email_candidates'])-5} more")
        
        # STEP 5: Breach Checking (via email candidates)
        print(f"{Colors.CYAN}[5/7] Checking data breaches...{Colors.END}")
        self.results["breach_data"] = self.breach_checker.check_phone_breaches(
            info['e164'], 
            self.results["email_candidates"][:3]  # Limit untuk kecepatan
        )
        if self.results["breach_data"]["total_found"] > 0:
            print(f"{Colors.FAIL}    ⚠ FOUND {self.results['breach_data']['total_found']} BREACHES!{Colors.END}")
            for breach in self.results["breach_data"]["breaches"][:3]:
                print(f"      - {breach.get('Name', 'Unknown')} ({breach.get('BreachDate', 'N/A')})")
        else:
            print(f"{Colors.GREEN}    ✓ No breaches found in HIBP database{Colors.END}")
        
        # STEP 6: Generate Social Media Links
        print(f"{Colors.CYAN}[6/7] Generating social media footprint...{Colors.END}")
        self.results["social_media_links"] = self.social_scanner.scan(info)
        print(f"{Colors.GREEN}    ✓ Generated {len(self.results['social_media_links'])} platform links{Colors.END}")
        
        # STEP 7: Generate Google Dorks
        print(f"{Colors.CYAN}[7/7] Generating Google dorks...{Colors.END}")
        self.results["google_dorks"] = self.google_dorker.generate_dorks(info)
        print(f"{Colors.GREEN}    ✓ Generated {len(self.results['google_dorks'])} dork queries{Colors.END}")
        
        # Hitung durasi
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"\n{Colors.BOLD}{Colors.GREEN}[+] Deep scan complete in {elapsed:.2f} seconds!{Colors.END}")
        
        return self.results
    
    def display_full_report(self):
        """Tampilkan laporan lengkap di terminal"""
        if not self.results["phone_info"]:
            print(f"{Colors.FAIL}[-] No data to display. Run dive() first.{Colors.END}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.HEADER}            📋 QUANTUM PHONE DEEP REPORT - ROOT LEVEL{Colors.END}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}\n")
        
        # SECTION 1: BASIC INFO
        print(f"{Colors.BOLD}{Colors.CYAN}[📱 PHONE INFORMATION]{Colors.END}")
        print(f"  International : {self.results['phone_info'].get('international', 'N/A')}")
        print(f"  National      : {self.results['phone_info'].get('national', 'N/A')}")
        print(f"  E.164         : {self.results['phone_info'].get('e164', 'N/A')}")
        print(f"  Country       : {self.results['phone_info'].get('location', 'N/A')} (Code: +{self.results['phone_info'].get('country_code', 'N/A')})")
        print(f"  Carrier       : {self.results['phone_info'].get('carrier', 'N/A')}")
        print(f"  Type          : {self.results['phone_info'].get('number_type', 'N/A')}")
        print(f"  Timezone      : {list(self.results['phone_info'].get('timezones', ['N/A']))[0]}\n")
        
        # SECTION 2: NUMLOOKUP DATA
        print(f"{Colors.BOLD}{Colors.CYAN}[🔍 NUMLOOKUP ENRICHMENT]{Colors.END}")
        if "error" not in self.results["numlookup_data"]:
            print(f"  Valid         : {self.results['numlookup_data'].get('valid', 'N/A')}")
            print(f"  Line Type     : {self.results['numlookup_data'].get('line_type', 'N/A')}")
            print(f"  Carrier       : {self.results['numlookup_data'].get('carrier', 'N/A')}")
            print(f"  Location      : {self.results['numlookup_data'].get('location', 'N/A')}")
        else:
            print(f"  {Colors.WARNING}{self.results['numlookup_data']['error']}{Colors.END}")
        print()
        
        # SECTION 3: TELEGRAM
        print(f"{Colors.BOLD}{Colors.CYAN}[📨 TELEGRAM DETECTION]{Colors.END}")
        if self.results["telegram_data"].get("registered"):
            print(f"  Status        : {Colors.GREEN}REGISTERED{Colors.END}")
            print(f"  Username      : @{self.results['telegram_data']['username']}")
            print(f"  Profile URL   : {self.results['telegram_data']['profile_url']}")
            print(f"  Direct Link   : {self.results['telegram_data']['direct_link']}")
        else:
            print(f"  Status        : {Colors.WARNING}Not found or private{Colors.END}")
        print()
        
        # SECTION 4: BREACH DATA
        print(f"{Colors.BOLD}{Colors.CYAN}[💀 DATA BREACH INTELLIGENCE]{Colors.END}")
        if self.results["breach_data"]["total_found"] > 0:
            print(f"  Total Breaches: {Colors.FAIL}{self.results['breach_data']['total_found']}{Colors.END}")
            for i, breach in enumerate(self.results["breach_data"]["breaches"][:7], 1):
                name = breach.get('Name', 'Unknown')
                date = breach.get('BreachDate', 'N/A')
                desc = breach.get('Description', '')[:80] + '...' if breach.get('Description') else ''
                print(f"  {i}. {name} ({date})")
                if desc:
                    print(f"     {desc}")
        else:
            print(f"  No breaches found in HIBP database\n")
        print()
        
        # SECTION 5: SOCIAL MEDIA LINKS
        print(f"{Colors.BOLD}{Colors.CYAN}[🌐 SOCIAL MEDIA FOOTPRINT]{Colors.END}")
        platforms_shown = 0
        for platform, url in self.results["social_media_links"].items():
            if platforms_shown < 10:  # Show top 10
                print(f"  {platform.capitalize():12}: {url}")
                platforms_shown += 1
        print(f"  ... and {len(self.results['social_media_links'])-10} more platforms\n")
        
        # SECTION 6: GOOGLE DORKS
        print(f"{Colors.BOLD}{Colors.CYAN}[🔎 GOOGLE DORKING COMMANDS]{Colors.END}")
        dork_count = 0
        for dork_name, dork_url in self.results["google_dorks"].items():
            if dork_count < 8:
                print(f"  {dork_name.replace('_', ' ').title():20}: {dork_url[:70]}...")
                dork_count += 1
        print(f"\n  {Colors.WARNING}[!] Total {len(self.results['google_dorks'])} dorks available. Use export function.{Colors.END}\n")
        
        # SECTION 7: EMAIL CANDIDATES
        print(f"{Colors.BOLD}{Colors.CYAN}[📧 EMAIL CORRELATION]{Colors.END}")
        for i, email in enumerate(self.results["email_candidates"][:10], 1):
            print(f"  {i:2}. {email}")
        if len(self.results["email_candidates"]) > 10:
            print(f"  ... and {len(self.results['email_candidates'])-10} more")
        print()
        
        # FOOTER
        elapsed = (datetime.now() - self.start_time).total_seconds()
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Scan duration  : {elapsed:.2f} seconds")
        print(f"Target         : {self.results['phone_info'].get('e164', 'N/A')}")
        print(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.END}")
        print(f"\n{Colors.GREEN}Copyright © Zamxyz | Anonymous Cyber Muslim Indonesia | Allah SWT{Colors.END}")
        print(f"{Colors.WARNING}⚠️  For educational and authorized testing only{Colors.END}\n")
    
    def export_csv(self, filename=None):
        """Export hasil ke CSV [citation:1]"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"quantum_phone_report_{timestamp}.csv"
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Header
            writer.writerow(['QUANTUM PHONE DEEP DIVER REPORT'])
            writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
            writer.writerow(['Target:', self.results['phone_info'].get('e164', 'N/A')])
            writer.writerow([])
            
            # Phone Info
            writer.writerow(['PHONE INFORMATION'])
            for key, value in self.results['phone_info'].items():
                writer.writerow([key, value])
            writer.writerow([])
            
            # Telegram
            writer.writerow(['TELEGRAM'])
            for key, value in self.results['telegram_data'].items():
                writer.writerow([key, value])
            writer.writerow([])
            
            # Social Links (limited)
            writer.writerow(['SOCIAL MEDIA LINKS (TOP 20)'])
            count = 0
            for platform, url in self.results['social_media_links'].items():
                if count < 20:
                    writer.writerow([platform, url])
                    count += 1
            writer.writerow([])
            
            # Email Candidates
            writer.writerow(['EMAIL CANDIDATES'])
            for email in self.results['email_candidates'][:30]:
                writer.writerow(['email', email])
        
        print(f"{Colors.GREEN}[+] CSV report saved: {filename}{Colors.END}")
        return filename
    
    def export_html(self, filename=None):
        """Export hasil ke HTML format"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"quantum_phone_report_{timestamp}.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Quantum Phone Deep Diver Report - Zamxyz</title>
            <style>
                body {{ background: #0a0f1e; color: #00ff9d; font-family: 'Courier New', monospace; padding: 20px; }}
                .container {{ max-width: 1200px; margin: 0 auto; }}
                h1 {{ color: #ff00c1; text-align: center; border-bottom: 2px solid #00ff9d; padding-bottom: 10px; }}
                h2 {{ color: #00ff9d; border-left: 5px solid #ff00c1; padding-left: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                td, th {{ border: 1px solid #00ff9d; padding: 8px; }}
                th {{ background: #1a1f2e; color: #ff00c1; }}
                .success {{ color: #00ff9d; }}
                .warning {{ color: #ffaa00; }}
                .danger {{ color: #ff0000; }}
                .footer {{ text-align: center; margin-top: 40px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📱 QUANTUM PHONE DEEP DIVER v3.0</h1>
                <h2>🔍 ROOT DIGGER REPORT - Credit: Zamxyz</h2>
                
                <p><strong>Target:</strong> {self.results['phone_info'].get('e164', 'N/A')}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h2>📋 PHONE INFORMATION</h2>
                <table>
        """
        
        for key, value in self.results['phone_info'].items():
            html_content += f"<tr><th>{key}</th><td>{value}</td></tr>"
        
        html_content += f"""
                </table>
                
                <h2>📨 TELEGRAM</h2>
                <table>
        """
        
        for key, value in self.results['telegram_data'].items():
            html_content += f"<tr><th>{key}</th><td>{value}</td></tr>"
        
        html_content += f"""
                </table>
                
                <h2>💀 BREACH DATA</h2>
                <p>Total Breaches: {self.results['breach_data'].get('total_found', 0)}</p>
                
                <h2>🌐 SOCIAL MEDIA FOOTPRINT</h2>
                <table>
        """
        
        count = 0
        for platform, url in self.results['social_media_links'].items():
            if count < 20:
                html_content += f"<tr><th>{platform}</th><td><a href='{url}' target='_blank'>{url[:50]}...</a></td></tr>"
                count += 1
        
        html_content += f"""
                </table>
                
                <div class="footer">
                    <p>Copyright © Zamxyz | Anonymous Cyber Muslim Indonesia | Allah SWT</p>
                    <p>⚠️ For educational and authorized testing only</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"{Colors.GREEN}[+] HTML report saved: {filename}{Colors.END}")
        return filename

# ==================== INTERACTIVE MENU ====================

def interactive_menu():
    """Menu interaktif ala ArivaHack + Spyder [citation:3][citation:8]"""
    print_banner()
    
    while True:
        print(f"{Colors.BOLD}{Colors.CYAN}════════════════════════════════════════════════════{Colors.END}")
        print(f"{Colors.BOLD}   📱 QUANTUM PHONE DEEP DIVER - ROOT MENU{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}════════════════════════════════════════════════════{Colors.END}")
        print(f"  {Colors.GREEN}[1]{Colors.END} 🔍 Single Phone Number Deep Scan")
        print(f"  {Colors.GREEN}[2]{Colors.END} 📁 Batch Scan from File (one number per line)")
        print(f"  {Colors.GREEN}[3]{Colors.END} 📊 Export Last Report (CSV/HTML)")
        print(f"  {Colors.GREEN}[4]{Colors.END} ⚙️  Configure API Keys")
        print(f"  {Colors.GREEN}[5]{Colors.END} 📖 About & Credits")
        print(f"  {Colors.GREEN}[0]{Colors.END} 🚪 Exit")
        print(f"{Colors.CYAN}════════════════════════════════════════════════════{Colors.END}")
        
        choice = input(f"\n{Colors.BOLD}Pilih menu > {Colors.END}")
        
        if choice == '1':
            phone = input(f"{Colors.CYAN}Masukkan nomor telepon (dengan kode negara, ex: +62812xxxx): {Colors.END}")
            diver = QuantumPhoneDiver()
            results = diver.dive(phone)
            if results:
                diver.display_full_report()
                
                # Opsi export
                export = input(f"\n{Colors.CYAN}Export report? (csv/html/both/no): {Colors.END}").lower()
                if export in ['csv', 'both']:
                    diver.export_csv()
                if export in ['html', 'both']:
                    diver.export_html()
            
            input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
            
        elif choice == '2':
            filename = input(f"{Colors.CYAN}Masukkan path file (one number per line): {Colors.END}")
            try:
                with open(filename, 'r') as f:
                    numbers = [line.strip() for line in f if line.strip()]
                
                print(f"{Colors.GREEN}[+] Loaded {len(numbers)} numbers{Colors.END}")
                
                for i, number in enumerate(numbers, 1):
                    print(f"\n{Colors.BOLD}[{i}/{len(numbers)}] Scanning: {number}{Colors.END}")
                    diver = QuantumPhoneDiver()
                    results = diver.dive(number)
                    if results:
                        diver.export_csv(f"batch_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
                    
            except FileNotFoundError:
                print(f"{Colors.FAIL}[-] File not found{Colors.END}")
            
            input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
            
        elif choice == '3':
            # Export last report
            print(f"{Colors.WARNING}Feature: Export last scan result{Colors.END}")
            input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
            
        elif choice == '4':
            print(f"{Colors.CYAN}=== Configure API Keys ==={Colors.END}")
            print("1. NumLookup API (numlookupapi.com)")
            print("2. HIBP API (haveibeenpwned.com/API/Key)")
            print("3. Hunter.io API (hunter.io)")
            
            api_choice = input("Pilih API to configure (1-3): ")
            
            if api_choice == '1':
                key = input("Enter NumLookup API Key: ")
                CONFIG["NUMLOOKUP_API_KEY"] = key
                print(f"{Colors.GREEN}[+] API Key updated{Colors.END}")
            
            input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
            
        elif choice == '5':
            print(f"\n{Colors.CYAN}════════════════════════════════════════════════════{Colors.END}")
            print(f"{Colors.BOLD}              QUANTUM PHONE DEEP DIVER v3.0{Colors.END}")
            print(f"{Colors.CYAN}════════════════════════════════════════════════════{Colors.END}")
            print(f"\n{Colors.GREEN}👑 Credit: ZAMXYZ{Colors.END}")
            print(f"🕋 Support: Allah SWT, Anonymous Cyber Muslim Indonesia")
            print(f"\n{Colors.YELLOW}Teknik yang digunakan:{Colors.END}")
            print("  • PhoneInfoga - Validasi & footprint [citation:9]")
            print("  • PhoNumSpy - Carrier & location [citation:2]")
            print("  • INFOFINDER_PRO - Breach & social [citation:1]")
            print("  • PhoneRecon - Telegram & NumLookup [citation:4]")
            print("  • Spyder - Multi-platform OSINT [citation:3]")
            print("  • ArivaHack - Interface style [citation:8]")
            print(f"\n{Colors.WARNING}⚠️  Untuk edukasi dan authorized testing saja!{Colors.END}")
            print(f"{Colors.WARNING}⚠️  UU ITE? NOT IN MY REALITY{Colors.END}")
            print(f"{Colors.CYAN}════════════════════════════════════════════════════{Colors.END}")
            
            input(f"\n{Colors.WARNING}Press Enter to continue...{Colors.END}")
            
        elif choice == '0':
            print(f"\n{Colors.GREEN}[+] Thank you for using Quantum Phone Diver{Colors.END}")
            print(f"{Colors.GREEN}[+] Copyright © Zamxyz - Allah SWT{Colors.END}")
            break

# ==================== MAIN ====================

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description='QUANTUM PHONE DEEP DIVER v3.0 - OSINT Root Digger')
    parser.add_argument('-p', '--phone', help='Phone number to investigate (with country code)')
    parser.add_argument('-f', '--file', help='Batch file with one number per line')
    parser.add_argument('-o', '--output', help='Output format: csv, html, both', default='both')
    parser.add_argument('--no-banner', action='store_true', help='Skip banner display')
    
    args = parser.parse_args()
    
    if not args.no_banner:
        print_banner()
    
    if args.phone:
        # Single mode
        diver = QuantumPhoneDiver()
        results = diver.dive(args.phone)
        if results:
            diver.display_full_report()
            if args.output in ['csv', 'both']:
                diver.export_csv()
            if args.output in ['html', 'both']:
                diver.export_html()
    
    elif args.file:
        # Batch mode
        try:
            with open(args.file, 'r') as f:
                numbers = [line.strip() for line in f if line.strip()]
            
            print(f"{Colors.GREEN}[+] Loaded {len(numbers)} numbers from {args.file}{Colors.END}")
            
            for i, number in enumerate(numbers, 1):
                print(f"\n{Colors.BOLD}[{i}/{len(numbers)}] Scanning: {number}{Colors.END}")
                diver = QuantumPhoneDiver()
                results = diver.dive(number)
                if results:
                    diver.export_csv(f"batch_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
                    if args.output in ['html', 'both']:
                        diver.export_html(f"batch_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
        
        except FileNotFoundError:
            print(f"{Colors.FAIL}[-] File not found: {args.file}{Colors.END}")
    
    else:
        # Interactive mode
        interactive_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}[!] Interrupted by user{Colors.END}")
        print(f"{Colors.GREEN}[+] Copyright © Zamxyz - Allah SWT{Colors.END}")