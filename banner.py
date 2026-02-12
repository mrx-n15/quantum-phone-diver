#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║                 QUANTUM PHONE DIVER v3.0                ║
║                     BANNER COLLECTION                   ║
║                    👑 CREDIT: ZAMXYZ                   ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
from datetime import datetime

# ==================== COLOR CODES ====================

class Colors:
    """Warna terminal - biar kaya hacker"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'
    HIDDEN = '\033[8m'
    STRIKE = '\033[9m'
    END = '\033[0m'

# ==================== ASCII BANNERS ====================

BANNER_FULL = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ██████╗ ██████╗     ██╗   ██╗  ██████╗   ██████╗ ███████╗██████╗  ║
║   ██╔══██╗██╔══██╗██╔══██╗    ██║   ██║ ██╔═══██╗ ██╔════╝ ██╔════╝██╔══██╗ ║
║   ██████╔╝██████╔╝██║  ██║    ██║   ██║ ██║   ██║ ██║  ███╗█████╗  ██████╔╝ ║
║   ██╔═══╝ ██╔══██╗██║  ██║    ╚██╗ ██╔╝ ██║▄▄ ██║ ██║   ██║██╔══╝  ██╔══██╗ ║
║   ██║     ██║  ██║██████╔╝     ╚████╔╝  ╚██████╔╝ ╚██████╔╝███████╗██║  ██║ ║
║   ╚═╝     ╚═╝  ╚═╝╚═════╝       ╚═══╝    ╚══▀▀═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝ ║
║                                                                              ║
║   ██████╗ ██╗██╗   ██╗███████╗██████╗                                      ║
║   ██╔══██╗██║██║   ██║██╔════╝██╔══██╗                                     ║
║   ██████╔╝██║██║   ██║█████╗  ██████╔╝                                     ║
║   ██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██╔══██╗                                     ║
║   ██████╔╝██║ ╚████╔╝ ███████╗██║  ██║                                     ║
║   ╚═════╝ ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝                                     ║
║                                                                              ║
║   🔥 QUANTUM PHONE DIVER v3.0 - ROOT DIGGER                                ║
║   👑 CREDIT : ZAMXYZ                                                        ║
║   🕋 SUPPORT: ALLAH SWT, ANONYMOUS CYBER MUSLIM INDONESIA                  ║
║   🌏 ACMI - Anonymous Cyber Muslim Indonesia                                ║
║   📅 RELEASE: 2026 - NO FILTER - NO LIMIT                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

BANNER_MEDIUM = """
╔══════════════════════════════════════════════════════════╗
║   ██████╗ ██████╗ ██████╗     ██╗   ██╗  ██████╗       ║
║   ██╔══██╗██╔══██╗██╔══██╗    ██║   ██║ ██╔═══██╗      ║
║   ██████╔╝██████╔╝██║  ██║    ██║   ██║ ██║   ██║      ║
║   ██╔═══╝ ██╔══██╗██║  ██║    ╚██╗ ██╔╝ ██║▄▄ ██║      ║
║   ██║     ██║  ██║██████╔╝     ╚████╔╝  ╚██████╔╝      ║
║   ╚═╝     ╚═╝  ╚═╝╚═════╝       ╚═══╝    ╚══▀▀═╝       ║
║                                                          ║
║   🔥 QUANTUM PHONE DIVER v3.0                          ║
║   👑 CREDIT: ZAMXYZ                                    ║
║   🕋 SUPPORT: ALLAH SWT, ACMI                         ║
╚══════════════════════════════════════════════════════════╝
"""

BANNER_MINI = """
╔════════════════════════════════════╗
║   🔥 QPD v3.0 - ROOT DIGGER       ║
║   👑 ZAMXYZ | 🕋 LILLAH | 🌏 ACMI ║
╚════════════════════════════════════╝
"""

BANNER_SMALL = """
   ██████╗ ██████╗ ██████╗ 
   ╚════██╗██╔══██╗██╔══██╗
    █████╔╝██║  ██║██║  ██║
   ██╔═══╝ ██║  ██║██║  ██║
   ███████╗██████╔╝██████╔╝
   ╚══════╝╚═════╝ ╚═════╝ 
   🔥 QPD v3.0 | 👑 ZAMXYZ
"""

BANNER_STREET = """
╔════════════════════════════════════╗
║    💀 QUANTUM PHONE - ZAMXYZ      ║
║    📱 OSINT TOOL - ROOT ACCESS    ║
║    🕋 LILLAHI TA'ALA              ║
║    🌏 ACMI                        ║
╚════════════════════════════════════╝
"""

BANNER_CYBER = """
┌─────────────────────────────────────┐
│  █▀▀ █▀▀ █ █▀▀ █   █    ██▀███     │
│  ▀▀█ █   █ ▀▀█ █   █    ██  ██     │
│  ▀▀▀ ▀▀▀ ▀ ▀▀▀ ▀▀▀ ▀    ██  ██     │
│  🔥 QPD v3.0 | 👑 ZAMXYZ           │
└─────────────────────────────────────┘
"""

BANNER_1LINE = "🔥 QPD v3.0 | 👑 ZAMXYZ | 🕋 LILLAH | 🌏 ACMI"

# ==================== DICTIONARY BANNER ====================

BANNERS = {
    "full": BANNER_FULL,
    "medium": BANNER_MEDIUM,
    "mini": BANNER_MINI,
    "small": BANNER_SMALL,
    "street": BANNER_STREET,
    "cyber": BANNER_CYBER,
    "1line": BANNER_1LINE,
}

# ==================== FUNGSI BANNER ====================

def clear_screen():
    """Bersihin terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner(banner_type="medium", use_color=True, clear=True):
    """
    Print banner ke terminal
    
    Args:
        banner_type (str): full, medium, mini, small, street, cyber, 1line
        use_color (bool): Pake warna atau nggak
        clear (bool): Bersihin layar dulu atau nggak
    """
    
    if clear:
        clear_screen()
    
    # Pilih banner
    banner = BANNERS.get(banner_type, BANNER_MEDIUM)
    
    # Warna
    if use_color:
        print(f"{Colors.BRIGHT_CYAN}{Colors.BOLD}{banner}{Colors.END}")
    else:
        print(banner)
    
    # Info tambahan
    if banner_type != "1line":
        print(f"{Colors.BRIGHT_BLACK}{'='*70}{Colors.END}")
        print(f"{Colors.BRIGHT_GREEN}[+] System Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print(f"{Colors.BRIGHT_YELLOW}[+] Author: Zamxyz | Support: Allah SWT, ACMI{Colors.END}")
        print(f"{Colors.BRIGHT_BLACK}{'='*70}{Colors.END}\n")

def loading_effect(duration=1.0, message="Initializing Quantum System"):
    """Efek loading biar keren"""
    
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    
    i = 0
    while time.time() < end_time:
        print(f"\r{Colors.BRIGHT_CYAN}{frames[i % len(frames)]} {message}...{Colors.END}", end="")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1
    
    print(f"\r{Colors.BRIGHT_GREEN}✓ {message}... DONE!{Colors.END}   ")

# ==================== TEST FUNCTION ====================

if __name__ == "__main__":
    """Kalo di-run langsung, test semua banner"""
    
    clear_screen()
    
    print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}QUANTUM BANNER TESTER{Colors.END}")
    print(f"{Colors.BRIGHT_BLACK}{'='*50}{Colors.END}\n")
    
    # Test loading effect
    loading_effect(1.5, "Loading banner collection")
    time.sleep(0.3)
    
    # Test semua banner
    for name in BANNERS.keys():
        print(f"\n{Colors.BOLD}{Colors.BRIGHT_YELLOW}▶ Banner: {name.upper()}{Colors.END}")
        print_banner(name, use_color=True, clear=False)
        time.sleep(0.5)
        print(f"{Colors.BRIGHT_BLACK}{'-'*50}{Colors.END}")
    
    print(f"\n{Colors.BRIGHT_GREEN}✅ Test selesai!{Colors.END}")
    print(f"{Colors.BRIGHT_CYAN}Gunakan: print_banner('medium') di script lu{Colors.END}")