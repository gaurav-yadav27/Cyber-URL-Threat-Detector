#!/usr/bin/env python3
"""
Cyberpunk URL Threat Detector - COOL ANIMATION EDITION
Next-level animations | Cyberpunk style | Smooth effects
Author: Gaurav Yadav
"""

import os
import re
import sys
import json
import time
import socket
import random
import sqlite3
import threading
from datetime import datetime
from urllib.parse import urlparse

# ============= NEXT-GEN COLOR SYSTEM =============
class Colors:
    NEON_GREEN = '\033[38;2;0;255;0m'
    NEON_RED = '\033[38;2;255;0;50m'
    NEON_BLUE = '\033[38;2;0;150;255m'
    NEON_PURPLE = '\033[38;2;180;0;255m'
    NEON_YELLOW = '\033[38;2;255;220;0m'
    NEON_CYAN = '\033[38;2;0;255;200m'
    NEON_PINK = '\033[38;2;255;0;200m'
    NEON_ORANGE = '\033[38;2;255;100;0m'
    NEON_WHITE = '\033[38;2;255;255;255m'
    MATRIX = '\033[38;2;0;255;0m'
    MATRIX_DIM = '\033[38;2;0;100;0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'

# ============= TRY IMPORT REQUESTS =============
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# ============= DATABASE SETUP =============
def init_database():
    conn = sqlite3.connect('threat_scans.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            threat_score INTEGER,
            verdict TEXT,
            timestamp TEXT,
            domain TEXT,
            ip TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_scan(url, score, verdict, domain, ip):
    conn = sqlite3.connect('threat_scans.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO scans (url, threat_score, verdict, timestamp, domain, ip)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (url, score, verdict, datetime.now().isoformat(), domain, ip))
    conn.commit()
    conn.close()

def get_scan_history(limit=50):
    conn = sqlite3.connect('threat_scans.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT url, threat_score, verdict, timestamp, domain, ip 
        FROM scans ORDER BY id DESC LIMIT ?
    ''', (limit,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_statistics():
    conn = sqlite3.connect('threat_scans.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM scans')
    total = cursor.fetchone()[0]
    cursor.execute('SELECT AVG(threat_score) FROM scans')
    avg = cursor.fetchone()[0] or 0
    cursor.execute('SELECT verdict, COUNT(*) FROM scans GROUP BY verdict')
    distribution = cursor.fetchall()
    cursor.execute('SELECT COUNT(DISTINCT domain) FROM scans')
    unique_domains = cursor.fetchone()[0]
    conn.close()
    return {
        'total': total,
        'avg_score': round(avg, 1),
        'distribution': dict(distribution),
        'unique_domains': unique_domains
    }

# ============= API CONFIGURATION =============
API_CONFIG_FILE = "api_config.json"

def load_api_keys():
    if os.path.exists(API_CONFIG_FILE):
        try:
            with open(API_CONFIG_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {"virustotal": "", "urlscan": ""}

def save_api_keys(keys):
    with open(API_CONFIG_FILE, 'w') as f:
        json.dump(keys, f, indent=2)

API_KEYS = load_api_keys()

# ============= COOL ANIMATION ENGINE =============
class CoolAnim:
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def cyber_type(text, delay=0.008, color=Colors.NEON_CYAN):
        """Cyber typing with glitch effect on some chars"""
        for char in text:
            if random.random() > 0.95:
                # Random glitch character
                glitch_char = random.choice(['#', '$', '%', '&', '@', '!'])
                sys.stdout.write(Colors.NEON_RED + glitch_char + Colors.RESET)
                time.sleep(0.02)
            sys.stdout.write(color + char + Colors.RESET)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def matrix_rain(lines=3, duration=0.5):
        """Enhanced matrix rain with falling effect"""
        chars = '01アイウエオカキクケコサシスセソタチツテト'
        for _ in range(lines):
            line = ''
            for _ in range(60):
                if random.random() > 0.8:
                    line += Colors.MATRIX + random.choice(chars) + Colors.RESET
                else:
                    line += Colors.MATRIX_DIM + random.choice(chars) + Colors.RESET
            sys.stdout.write(line + '\n')
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(duration)
    
    @staticmethod
    def glitch_effect(text, color=Colors.NEON_RED):
        """Advanced glitch with screen shake effect"""
        for _ in range(3):
            # Random offset for shake effect
            offset = random.randint(-2, 2)
            if offset > 0:
                sys.stdout.write(' ' * offset)
            
            # Random character substitution
            glitched = ''.join(
                random.choice('!@#$%&*?') if random.random() > 0.85 else c 
                for c in text
            )
            
            if random.random() > 0.5:
                sys.stdout.write(color + Colors.BOLD + glitched + Colors.RESET)
            else:
                sys.stdout.write(Colors.NEON_WHITE + glitched + Colors.RESET)
            sys.stdout.flush()
            time.sleep(0.06)
            sys.stdout.write('\r' + ' ' * (len(text) + 5) + '\r')
            sys.stdout.flush()
            time.sleep(0.04)
        sys.stdout.write(color + Colors.BOLD + text + Colors.RESET + '\n')
    
    @staticmethod
    def neon_progress(duration=0.6):
        """Smooth neon progress bar with glow"""
        bar_length = 45
        for i in range(bar_length + 1):
            percent = i / bar_length
            
            # Color shifting based on progress
            if percent < 0.25:
                color = Colors.NEON_BLUE
            elif percent < 0.5:
                color = Colors.NEON_CYAN
            elif percent < 0.75:
                color = Colors.NEON_YELLOW
            else:
                color = Colors.NEON_RED
            
            # Create glowing bar
            bar = ''
            for j in range(bar_length):
                if j < i:
                    if j == i - 1:
                        bar += Colors.NEON_WHITE + '█' + Colors.RESET
                    else:
                        bar += color + '█' + Colors.RESET
                else:
                    bar += Colors.DIM + '░' + Colors.RESET
            
            sys.stdout.write(f'\r  ⚡ [{bar}] {percent*100:.0f}%')
            sys.stdout.flush()
            time.sleep(duration / bar_length)
        print()
    
    @staticmethod
    def scanning_animation(duration=1.0):
        """Cool scanning radar animation"""
        radar_frames = [
            '[    ]', '[=   ]', '[==  ]', '[=== ]', '[====]',
            '[ ===]', '[  ==]', '[   =]', '[    ]'
        ]
        start = time.time()
        i = 0
        while time.time() - start < duration:
            sys.stdout.write(f'\r{Colors.NEON_CYAN}🔍 SCANNING {radar_frames[i % len(radar_frames)]}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
        sys.stdout.write(f'\r{Colors.NEON_GREEN}✓ SCAN COMPLETE     {Colors.RESET}\n')
    
    @staticmethod
    def pulse_ring(text, color=Colors.NEON_PURPLE, cycles=3):
        """Pulsing ring with expanding effect"""
        rings = ['◉', '◎', '○', '◌', '○', '◎']
        for _ in range(cycles):
            for ring in rings:
                sys.stdout.write(f'\r{color}{ring} {text}{Colors.RESET}')
                sys.stdout.flush()
                time.sleep(0.08)
        print()
    
    @staticmethod
    def cyber_border(text, color=Colors.NEON_CYAN):
        """Animated cyberpunk border"""
        # Draw corners
        corners = ['╔', '╗', '╝', '╚']
        for corner in corners:
            sys.stdout.write(f'\r{color}{corner}{" " * (len(text)+2)}{corner}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.08)
        
        top = color + '╔' + '═' * (len(text) + 2) + '╗' + Colors.RESET
        middle = color + '║ ' + Colors.BOLD + text + Colors.RESET + color + ' ║' + Colors.RESET
        bottom = color + '╚' + '═' * (len(text) + 2) + '╝' + Colors.RESET
        
        print(top)
        print(middle)
        print(bottom)
    
    @staticmethod
    def loader_cyber(message, duration=0.8):
        """Cyberpunk loading spinner"""
        spinner = ['◢', '◣', '◤', '◥']
        start = time.time()
        i = 0
        while time.time() - start < duration:
            sys.stdout.write(f'\r{Colors.NEON_CYAN}{spinner[i % len(spinner)]} {message}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.08)
            i += 1
        sys.stdout.write(f'\r{Colors.NEON_GREEN}✓ {message}{Colors.RESET}\n')
    
    @staticmethod
    def threat_meter(score):
        """Glowing threat meter"""
        bar_length = 45
        filled = int(bar_length * score / 100)
        
        if score < 30:
            color = Colors.NEON_GREEN
            glow = Colors.NEON_WHITE
        elif score < 60:
            color = Colors.NEON_YELLOW
            glow = Colors.NEON_WHITE
        else:
            color = Colors.NEON_RED
            glow = Colors.NEON_WHITE
        
        bar = ''
        for i in range(bar_length):
            if i < filled:
                if i == filled - 1:
                    bar += glow + '█' + Colors.RESET
                else:
                    bar += color + '█' + Colors.RESET
            else:
                bar += Colors.DIM + '░' + Colors.RESET
        
        sys.stdout.write(f'\r  🎯 [{bar}] {score}%')
        print()
    
    @staticmethod
    def hack_load(duration=0.6):
        """Hacker-style loading with random characters"""
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%'
        start = time.time()
        while time.time() - start < duration:
            line = ''.join(random.choice(chars) for _ in range(40))
            sys.stdout.write(f'\r{Colors.MATRIX}{line}{Colors.RESET}')
            sys.stdout.flush()
            time.sleep(0.03)
        sys.stdout.write(f'\r{Colors.NEON_GREEN}{"█" * 40} READY{Colors.RESET}\n')

# ============= THREAT INTELLIGENCE =============
class ThreatIntel:
    SUSPICIOUS_KEYWORDS = [
        'login', 'verify', 'account', 'secure', 'update', 'confirm',
        'password', 'credential', 'banking', 'wallet', 'crypto'
    ]
    SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.xyz', '.top', '.club', '.work']
    URL_SHORTENERS = ['bit.ly', 'tinyurl', 'goo.gl', 'ow.ly', 'is.gd', 't.co']
    
    SAFE_DOMAINS = {
        'google.com', 'youtube.com', 'github.com', 'wikipedia.org',
        'microsoft.com', 'apple.com', 'amazon.com', 'netflix.com'
    }
    
    @staticmethod
    def extract_domain(url):
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    
    @staticmethod
    def dns_lookup(domain):
        try:
            ip = socket.gethostbyname(domain)
            return {"resolves": True, "ip": ip}
        except:
            return {"resolves": False, "ip": None}
    
    @staticmethod
    def check_virustotal(url):
        if not API_KEYS.get("virustotal") or not REQUESTS_AVAILABLE:
            return None
        try:
            import base64
            headers = {"x-apikey": API_KEYS["virustotal"]}
            url_id = base64.urlsafe_b64encode(url.encode()).decode().strip('=')
            response = requests.get(
                f"https://www.virustotal.com/api/v3/urls/{url_id}",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                malicious = stats.get("malicious", 0)
                if malicious > 0:
                    return {"malicious": malicious, "source": "VirusTotal"}
            return None
        except:
            return None
    
    @classmethod
    def analyze(cls, url, use_api=True):
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        findings = []
        score = 0
        url_lower = url.lower()
        domain = cls.extract_domain(url)
        
        for safe in cls.SAFE_DOMAINS:
            if domain == safe or domain.endswith('.' + safe):
                return {"score": 0, "threat": "SAFE", "emoji": "✅", 
                        "findings": [f"Trusted domain: {safe}"], "malicious": False, "domain": domain, "url": url}
        
        if not url.startswith('https'):
            score += 20
            findings.append("⚠️ No HTTPS encryption")
        
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
            score += 35
            findings.append("🔴 Direct IP address usage")
        
        for kw in cls.SUSPICIOUS_KEYWORDS:
            if kw in url_lower:
                score += 5
                findings.append(f"⚠️ Suspicious keyword: '{kw}'")
                break
        
        for short in cls.URL_SHORTENERS:
            if short in url_lower:
                score += 15
                findings.append(f"⚠️ URL shortener detected")
                break
        
        for tld in cls.SUSPICIOUS_TLDS:
            if domain.endswith(tld):
                score += 25
                findings.append(f"🔴 Suspicious TLD: {tld}")
                break
        
        if '@' in url:
            score += 45
            findings.append("🔴 '@' symbol - Phishing indicator")
        
        if len(url) > 100:
            score += 10
            findings.append("⚠️ Excessive URL length")
        
        if use_api and REQUESTS_AVAILABLE:
            vt_result = cls.check_virustotal(url)
            if vt_result:
                score = min(100, score + 30)
                findings.append(f"🔴 {vt_result['source']}: Malicious detected")
        
        score = min(100, score)
        
        if score <= 20:
            threat, emoji = "SAFE", "✅"
        elif score <= 50:
            threat, emoji = "LOW RISK", "⚠️"
        elif score <= 75:
            threat, emoji = "HIGH RISK", "🔴"
        else:
            threat, emoji = "CRITICAL", "💀"
        
        return {
            "score": score, "threat": threat, "emoji": emoji,
            "findings": findings, "malicious": score > 50,
            "domain": domain, "url": url
        }

# ============= UI DISPLAY =============
def show_header():
    CoolAnim.clear()
    CoolAnim.matrix_rain(2, 0.3)
    
    header = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║     ██╗   ██╗██████╗ ██╗         ████████╗██╗  ██╗██████╗     ║
    ║     ██║   ██║██╔══██╗██║         ╚══██╔══╝██║  ██║██╔══██╗    ║
    ║     ██║   ██║██████╔╝██║            ██║   ███████║██████╔╝    ║
    ║     ██║   ██║██╔══██╗██║            ██║   ██╔══██║██╔══██╗    ║
    ║     ╚██████╔╝██║  ██║███████╗       ██║   ██║  ██║██║  ██║    ║
    ║      ╚═════╝ ╚═╝  ╚═╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    for line in header.split('\n'):
        if line.strip():
            CoolAnim.cyber_type(line, 0.001, Colors.NEON_CYAN)
    
    print()
    CoolAnim.cyber_type(">> CYBER THREAT INTELLIGENCE TERMINAL v6.0 <<", 0.01, Colors.NEON_PURPLE)
    print(Colors.DIM + "═"*63 + Colors.RESET)
    CoolAnim.cyber_type(f">> AUTHOR: GAURAV YADAV", 0.01, Colors.NEON_GREEN)
    
    has_api = bool(API_KEYS.get("virustotal"))
    if has_api:
        print(f"{Colors.NEON_GREEN}>> API STATUS: ACTIVE (VirusTotal){Colors.RESET}")
    else:
        print(f"{Colors.NEON_YELLOW}>> API STATUS: INACTIVE (Configure in Option 5){Colors.RESET}")
    
    print(Colors.DIM + "═"*63 + Colors.RESET)
    print()

def analyze_single():
    show_header()
    CoolAnim.cyber_border("TARGET ACQUISITION", Colors.NEON_CYAN)
    print()
    CoolAnim.cyber_type("ENTER URL FOR ANALYSIS:", 0.01, Colors.NEON_YELLOW)
    print(Colors.DIM + ">> Format: domain.com OR https://example.com" + Colors.RESET)
    url = input(Colors.NEON_GREEN + "\n⚡ URL > " + Colors.RESET).strip()
    
    if not url:
        return
    
    print()
    CoolAnim.loader_cyber("INITIALIZING THREAT SCAN", 0.5)
    CoolAnim.hack_load(0.4)
    CoolAnim.scanning_animation(0.8)
    CoolAnim.neon_progress(0.5)
    
    result = ThreatIntel.analyze(url, use_api=True)
    domain = ThreatIntel.extract_domain(url)
    dns = ThreatIntel.dns_lookup(domain)
    
    save_scan(url, result['score'], result['threat'], domain, dns.get('ip', 'Unknown'))
    
    show_header()
    CoolAnim.cyber_border("THREAT ANALYSIS REPORT", Colors.NEON_RED)
    print()
    
    CoolAnim.cyber_type("🎯 TARGET ACQUIRED:", 0.008, Colors.NEON_YELLOW)
    print(f"  {Colors.NEON_CYAN}{url}{Colors.RESET}")
    print()
    
    CoolAnim.cyber_type("⚡ THREAT LEVEL:", 0.008, Colors.NEON_YELLOW)
    CoolAnim.threat_meter(result['score'])
    
    if result['threat'] == "SAFE":
        color = Colors.NEON_GREEN
        msg = f"✓ VERDICT: SECURE - Score: {result['score']}%"
    elif result['threat'] == "LOW RISK":
        color = Colors.NEON_YELLOW
        msg = f"⚠️ VERDICT: CAUTION - Score: {result['score']}%"
    elif result['threat'] == "HIGH RISK":
        color = Colors.NEON_RED
        msg = f"🔴 VERDICT: DANGEROUS - Score: {result['score']}%"
    else:
        color = Colors.NEON_RED
        msg = f"💀 VERDICT: CRITICAL - Score: {result['score']}%"
    
    CoolAnim.glitch_effect(msg, color)
    print()
    
    CoolAnim.cyber_type("🌐 DOMAIN INTELLIGENCE:", 0.008, Colors.NEON_BLUE)
    print(f"  Domain: {Colors.NEON_PURPLE}{domain}{Colors.RESET}")
    if dns['resolves']:
        print(f"  IP: {Colors.NEON_GREEN}{dns['ip']}{Colors.RESET}")
    else:
        print(f"  {Colors.NEON_RED}⚠️ DNS resolution failed{Colors.RESET}")
    print()
    
    if result['findings']:
        CoolAnim.cyber_type("🔍 THREAT INDICATORS:", 0.008, Colors.NEON_RED)
        for finding in result['findings']:
            CoolAnim.cyber_type(f"  {finding}", 0.003, Colors.NEON_YELLOW)
    else:
        CoolAnim.cyber_type("✅ NO THREATS DETECTED", 0.008, Colors.NEON_GREEN)
    
    print()
    CoolAnim.cyber_type("💡 RECOMMENDATION:", 0.008, Colors.NEON_BLUE)
    if result['threat'] == "SAFE":
        CoolAnim.cyber_type("  → URL appears secure for access", 0.005, Colors.NEON_GREEN)
    elif result['threat'] == "LOW RISK":
        CoolAnim.pulse_ring("EXERCISE CAUTION", Colors.NEON_YELLOW, 1)
    else:
        CoolAnim.pulse_ring("DO NOT ACCESS THIS URL", Colors.NEON_RED, 2)
    
    input(Colors.DIM + "\n>> Press Enter to continue..." + Colors.RESET)

def batch_scan():
    show_header()
    CoolAnim.cyber_border("BATCH ANALYSIS", Colors.NEON_PURPLE)
    print()
    
    filename = input(Colors.NEON_YELLOW + ">> FILENAME [urls.txt]: " + Colors.RESET).strip()
    if not filename:
        filename = "urls.txt"
    
    try:
        with open(filename, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if not urls:
            CoolAnim.glitch_effect("NO URLS FOUND", Colors.NEON_RED)
            time.sleep(1.5)
            return
        
        print(f"\n{Colors.NEON_GREEN}>> SCANNING {len(urls)} TARGETS{Colors.RESET}\n")
        CoolAnim.scanning_animation(0.6)
        
        results = []
        for i, url in enumerate(urls):
            percent = (i + 1) / len(urls)
            bar = Colors.MATRIX + '█' * int(percent * 30) + Colors.DIM + '░' * (30 - int(percent * 30)) + Colors.RESET
            sys.stdout.write(f'\r  🔍 [{bar}] {percent*100:.0f}% - {url[:35]}...')
            sys.stdout.flush()
            
            result = ThreatIntel.analyze(url, use_api=True)
            results.append(result)
            save_scan(url, result['score'], result['threat'], 
                     ThreatIntel.extract_domain(url), 'Unknown')
            time.sleep(0.02)
        
        print("\n\n")
        CoolAnim.cyber_border("BATCH RESULTS", Colors.NEON_CYAN)
        print()
        
        safe = sum(1 for r in results if r['threat'] == "SAFE")
        low = sum(1 for r in results if r['threat'] == "LOW RISK")
        high = sum(1 for r in results if r['threat'] == "HIGH RISK")
        critical = sum(1 for r in results if r['threat'] == "CRITICAL")
        
        total = len(results)
        print(f"{Colors.NEON_GREEN}✓ SECURE: {safe} ({safe/total*100:.1f}%){Colors.RESET}")
        print(f"{Colors.NEON_YELLOW}⚠️ CAUTION: {low} ({low/total*100:.1f}%){Colors.RESET}")
        print(f"{Colors.NEON_RED}🔴 DANGEROUS: {high} ({high/total*100:.1f}%){Colors.RESET}")
        print(f"{Colors.NEON_RED}💀 CRITICAL: {critical} ({critical/total*100:.1f}%){Colors.RESET}")
        print()
        
        print(Colors.NEON_CYAN + "DETAILED RESULTS:" + Colors.RESET)
        print(Colors.DIM + "-"*70 + Colors.RESET)
        
        for r in results:
            if r['threat'] == "SAFE":
                color = Colors.NEON_GREEN
            elif r['threat'] == "LOW RISK":
                color = Colors.NEON_YELLOW
            else:
                color = Colors.NEON_RED
            
            display_url = r['url'] if len(r['url']) < 50 else r['url'][:47] + "..."
            print(f"{color}{r['emoji']} {r['threat']:<10}{Colors.RESET} [{r['score']:>2}%] → {display_url}")
        
        print(Colors.DIM + "-"*70 + Colors.RESET)
        
        if high > 0 or critical > 0:
            print()
            CoolAnim.pulse_ring(f"⚠️ WARNING: {high + critical} DANGEROUS URL(S) FOUND", Colors.NEON_RED, 2)
        
    except FileNotFoundError:
        CoolAnim.glitch_effect(f"FILE NOT FOUND: {filename}", Colors.NEON_RED)
    
    print()
    input(Colors.DIM + ">> Press Enter to continue..." + Colors.RESET)

def show_history():
    show_header()
    CoolAnim.cyber_border("SCAN HISTORY", Colors.NEON_CYAN)
    print()
    
    history = get_scan_history(20)
    if not history:
        CoolAnim.cyber_type("No scan history found. Run some scans first!", 0.01, Colors.NEON_YELLOW)
    else:
        print(f"{'URL':<45} {'Score':<8} {'Verdict':<12} {'Date'}")
        print(Colors.DIM + "-"*80 + Colors.RESET)
        for url, score, verdict, timestamp, domain, ip in history:
            if verdict == "SAFE":
                color = Colors.NEON_GREEN
            elif verdict == "LOW RISK":
                color = Colors.NEON_YELLOW
            else:
                color = Colors.NEON_RED
            
            url_short = url[:42] + "..." if len(url) > 42 else url
            date_short = timestamp.split('T')[0] if 'T' in timestamp else timestamp[:10]
            print(f"{color}{url_short:<45}{Colors.RESET} {score}%{' '*5} {verdict:<12} {date_short}")
    
    print()
    input(Colors.DIM + ">> Press Enter to continue..." + Colors.RESET)

def show_statistics():
    show_header()
    CoolAnim.cyber_border("STATISTICS DASHBOARD", Colors.NEON_PURPLE)
    print()
    
    stats = get_statistics()
    
    if stats['total'] == 0:
        CoolAnim.cyber_type("No data available. Run some scans first!", 0.01, Colors.NEON_YELLOW)
        input(Colors.DIM + "\n>> Press Enter to continue..." + Colors.RESET)
        return
    
    print(f"{Colors.NEON_GREEN}📊 TOTAL SCANS:{Colors.RESET} {stats['total']}")
    print(f"{Colors.NEON_BLUE}🌐 UNIQUE DOMAINS:{Colors.RESET} {stats['unique_domains']}")
    print(f"{Colors.NEON_YELLOW}📈 AVG THREAT SCORE:{Colors.RESET} {stats['avg_score']}%")
    print()
    
    print(f"{Colors.NEON_CYAN}🎯 THREAT DISTRIBUTION:{Colors.RESET}")
    print()
    
    distribution = stats['distribution']
    total = stats['total']
    
    categories = ['SAFE', 'LOW RISK', 'HIGH RISK', 'CRITICAL']
    colors = [Colors.NEON_GREEN, Colors.NEON_YELLOW, Colors.NEON_RED, Colors.NEON_RED]
    
    for cat, color in zip(categories, colors):
        count = distribution.get(cat, 0)
        percent = (count / total * 100) if total > 0 else 0
        bar_length = int(percent / 2)
        bar = '█' * bar_length + '░' * (50 - bar_length)
        print(f"  {color}{cat:<12}{Colors.RESET} {count:>4} ({percent:>5.1f}%) [{bar}]")
    
    print()
    print(f"{Colors.NEON_CYAN}📊 OVERALL THREAT METER:{Colors.RESET}")
    CoolAnim.threat_meter(stats['avg_score'])
    
    print()
    input(Colors.DIM + ">> Press Enter to continue..." + Colors.RESET)

def setup_api():
    global API_KEYS
    show_header()
    CoolAnim.cyber_border("API CONFIGURATION", Colors.NEON_CYAN)
    print()
    
    CoolAnim.cyber_type("API keys are OPTIONAL - They add cloud threat intelligence", 0.01, Colors.NEON_YELLOW)
    print()
    
    print(f"{Colors.NEON_GREEN}📍 Get free API keys:{Colors.RESET}")
    print("  VirusTotal: https://www.virustotal.com/gui/join-us")
    print("  → Free tier: 500 requests/day")
    print()
    
    current_vt = API_KEYS.get("virustotal", "")
    if current_vt:
        print(f"{Colors.NEON_GREEN}Current VirusTotal: {current_vt[:8]}...{current_vt[-4:]}{Colors.RESET}")
    
    vt_key = input(Colors.NEON_YELLOW + "\n>> VirusTotal API Key [ENTER to keep]: " + Colors.RESET).strip()
    if vt_key:
        API_KEYS["virustotal"] = vt_key
    
    save_api_keys(API_KEYS)
    
    print()
    CoolAnim.glitch_effect("API CONFIGURATION SAVED", Colors.NEON_GREEN)
    print()
    input(Colors.DIM + ">> Press Enter to continue..." + Colors.RESET)

def show_help():
    show_header()
    CoolAnim.cyber_border("HELP & FEATURES", Colors.NEON_CYAN)
    print()
    
    features = [
        ("🔍 Single URL Scan", "Analyze individual URLs with full visual feedback"),
        ("📊 Batch Analysis", "Scan multiple URLs from a text file - SHOWS EACH DOMAIN"),
        ("📜 Scan History", "View all previous scan results"),
        ("📈 Statistics Dashboard", "View threat trends and distribution"),
        ("🔑 API Configuration", "Add VirusTotal API for enhanced detection"),
    ]
    
    for name, desc in features:
        CoolAnim.cyber_type(f"▶ {name}", 0.005, Colors.NEON_GREEN)
        CoolAnim.cyber_type(f"   {desc}", 0.003, Colors.DIM)
        print()
    
    print()
    CoolAnim.cyber_type(">> HOW TO USE BATCH SCAN:", 0.008, Colors.NEON_YELLOW)
    CoolAnim.cyber_type("  • Create a file called 'urls.txt'", 0.005, Colors.DIM)
    CoolAnim.cyber_type("  • Put one URL per line", 0.005, Colors.DIM)
    CoolAnim.cyber_type("  • Lines starting with # are ignored", 0.005, Colors.DIM)
    
    print()
    input(Colors.DIM + ">> Press Enter to continue..." + Colors.RESET)

def main():
    init_database()
    
    while True:
        show_header()
        
        menu = """
┌─────────────────────────────────────────────────┐
│                  MAIN TERMINAL                   │
├─────────────────────────────────────────────────┤
│  [1] 🔍  SINGLE URL SCAN                        │
│  [2] 📊  BATCH ANALYSIS                         │
│  [3] 📜  SCAN HISTORY                           │
│  [4] 📈  STATISTICS DASHBOARD                   │
│  [5] 🔑  API CONFIGURATION                      │
│  [6] 🎨  HELP & FEATURES                        │
│  [7] 🚪  EXIT TERMINAL                          │
└─────────────────────────────────────────────────┘
"""
        print(menu)
        
        choice = input(Colors.NEON_YELLOW + ">> SELECT OPTION [1-7]: " + Colors.RESET)
        
        if choice == '1':
            analyze_single()
        elif choice == '2':
            batch_scan()
        elif choice == '3':
            show_history()
        elif choice == '4':
            show_statistics()
        elif choice == '5':
            setup_api()
        elif choice == '6':
            show_help()
        elif choice == '7':
            show_header()
            CoolAnim.glitch_effect("TERMINATING CONNECTION", Colors.NEON_RED)
            print()
            CoolAnim.cyber_type("Thank you for using Cyber Threat Detector", 0.01, Colors.NEON_GREEN)
            CoolAnim.cyber_type("Stay vigilant. Stay secure. - Gaurav Yadav", 0.01, Colors.NEON_PURPLE)
            print()
            sys.exit(0)
        else:
            CoolAnim.glitch_effect("INVALID COMMAND", Colors.NEON_RED)
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.NEON_RED}\n>> EMERGENCY SHUTDOWN{Colors.RESET}")
        sys.exit(0)