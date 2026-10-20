#!/usr/bin/env python3
# CYBER PHANTOM ULTIMATE — defensive, consent-based information toolkit
import os, sys, socket, ssl, hashlib, secrets, string, re, platform, subprocess, json
from datetime import datetime
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    requests = None
try:
    import phonenumbers
    from phonenumbers import carrier, geocoder, timezone
except ImportError:
    phonenumbers = carrier = geocoder = timezone = None
try:
    import dns.resolver
except ImportError:
    dns = None

R="\033[91m"; G="\033[92m"; Y="\033[93m"; B="\033[94m"
C="\033[96m"; M="\033[95m"; W="\033[97m"; X="\033[0m"; D="\033[2m"
REPORT_DIR="reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def clear():
    os.system("cls" if os.name=="nt" else "clear")

def banner():
    print(R+r"""
     ██████╗██╗   ██╗██████╗ ███████╗██████╗
    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
    ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝
"""+X)
    print(G+"   ╔════════════════════════════════════════════════════╗"+X)
    print(G+"   ║"+R+"      C Y B E R   P H A N T O M   U L T I M A T E   "+G+"║"+X)
    print(G+"   ║"+C+"       MULTI-TOOL INTELLIGENCE • TERMUX • KALI       "+G+"║"+X)
    print(G+"   ╚════════════════════════════════════════════════════╝"+X)
    print(D+"      PHONE • NETWORK • WEB • FILES • SECURITY REPORTS"+X)
    print()

def pause(): input(f"\n{D}Press Enter to return to menu...{X}")
def save_report(title, body):
    stamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    safe=re.sub(r"[^a-zA-Z0-9_-]+","_",title)[:40]
    path=os.path.join(REPORT_DIR,f"{safe}_{stamp}.txt")
    with open(path,"w",encoding="utf-8") as f:
        f.write(f"CYBER PHANTOM ULTIMATE REPORT\n{title}\nCreated: {datetime.now().isoformat()}\n\n{body}\n")
    print(G+f"[+] Saved report: {path}"+X)
def hostclean(v):
    v=v.strip()
    if "://" in v: return urlparse(v).hostname
    return v.split("/")[0].split(":")[0].strip()
def run_cmd(args):
    try:
        return subprocess.check_output(args, stderr=subprocess.DEVNULL, text=True, timeout=4).strip()
    except Exception:
        return ""

def phone_number_info():
    print(C+"\n[ PHONE NUMBER INTELLIGENCE ]"+X)
    if not phonenumbers:
        print(Y+"Phone library missing. Run the install script first."+X); return
    raw=input("Phone number with country code (example +9665XXXXXXXX): ").strip()
    if not raw: return
    try:
        num=phonenumbers.parse(raw, None)
        valid=phonenumbers.is_valid_number(num)
        possible=phonenumbers.is_possible_number(num)
        region=geocoder.description_for_number(num,"en") or "Not available"
        carrier_name=carrier.name_for_number(num,"en") or "Not available"
        zones=", ".join(timezone.time_zones_for_number(num)) or "Not available"
        lines=[
            f"Input: {raw}",f"Formatted international: {phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}",
            f"Formatted national: {phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.NATIONAL)}",
            f"Country calling code: +{num.country_code}",f"Number region metadata: {region}",
            f"Carrier metadata (may be unavailable/outdated): {carrier_name}",
            f"Possible number: {possible}",f"Valid according to numbering plan: {valid}",f"Time zones associated with region: {zones}",
            "", "Privacy note: this does not identify the subscriber, reveal their home address, or locate a phone in real time."
        ]
        print("\n".join(lines)); save_report("phone_number_info","\n".join(lines))
    except Exception as e: print(R+"Could not parse number. Include +country code, e.g. +966..."+X)

def device_info():
    print(C+"\n[ PHONE / DEVICE INFORMATION ]"+X)
    lines=[f"Platform: {platform.platform()}",f"Python: {platform.python_version()}",f"Hostname: {socket.gethostname()}"]
    if "ANDROID_ROOT" in os.environ or "com.termux" in os.environ.get("PREFIX",""):
        lines += [
            "Android release: "+(run_cmd(["getprop","ro.build.version.release"]) or "Not available"),
            "Device model: "+(run_cmd(["getprop","ro.product.model"]) or "Not available"),
            "Manufacturer: "+(run_cmd(["getprop","ro.product.manufacturer"]) or "Not available"),
            "Android SDK: "+(run_cmd(["getprop","ro.build.version.sdk"]) or "Not available"),
            "Battery status: "+(run_cmd(["termux-battery-status"]) or "Install Termux:API for battery info"),
        ]
    try:
        addrs=sorted(set(i[4][0] for i in socket.getaddrinfo(socket.gethostname(),None) if ":" not in i[4][0]))
        lines.append("Local IPv4 addresses: "+(", ".join(addrs) if addrs else "Not detected"))
    except Exception: pass
    for line in lines: print(G+"• "+X+line)
    save_report("device_info","\n".join(lines))

def public_ip_info():
    print(C+"\n[ PUBLIC IP INTELLIGENCE ]"+X)
    if not requests: print(Y+"Install requirements first."+X); return
    try:
        r=requests.get("https://ipinfo.io/json",timeout=8,headers={"User-Agent":"CyberPhantomUltimate/1.0"})
        r.raise_for_status(); data=r.json()
        keys=["ip","city","region","country","loc","org","timezone","postal"]
        lines=[f"{k}: {data.get(k,'Not available')}" for k in keys]
        print("\n".join(lines))
        print(Y+"IP-based location is approximate and may describe a VPN/mobile carrier gateway, not a person's exact location."+X)
        save_report("public_ip_info","\n".join(lines)+"\nIP geolocation is approximate.")
    except Exception as e: print(R+"IP lookup failed: "+str(e)+X)

def dns_lookup():
    print(C+"\n[ DNS INTELLIGENCE ]"+X)
    h=hostclean(input("Domain: "))
    if not h:return
    lines=[f"Domain: {h}"]
    try:
        ips=sorted(set(i[4][0] for i in socket.getaddrinfo(h,None)))
        print(G+"A/AAAA addresses: "+X+", ".join(ips)); lines.append("Addresses: "+", ".join(ips))
    except Exception as e: print(R+str(e)+X); lines.append(str(e))
    if dns:
        for typ in ("MX","NS","TXT"):
            try:
                vals=[str(x) for x in dns.resolver.resolve(h,typ,lifetime=5)]
                print(C+typ+": "+X+" | ".join(vals)); lines.append(typ+": "+" | ".join(vals))
            except Exception:
                print(D+typ+": no record or unavailable"+X); lines.append(typ+": no record or unavailable")
    save_report("dns_lookup","\n".join(lines))

def website_audit():
    print(C+"\n[ WEBSITE SECURITY HEADER AUDIT ]"+X)
    u=input("Website URL: ").strip()
    if not u:return
    if not u.startswith(("http://","https://")): u="https://"+u
    if not requests: print(Y+"Install requirements first."+X); return
    try:
        r=requests.get(u,timeout=12,allow_redirects=True,headers={"User-Agent":"CyberPhantomUltimate/1.0"})
        checks={"Strict-Transport-Security":"HSTS","Content-Security-Policy":"CSP","X-Content-Type-Options":"MIME sniffing protection","X-Frame-Options":"Clickjacking protection","Referrer-Policy":"Referrer policy","Permissions-Policy":"Browser permissions policy"}
        lines=[f"Requested URL: {u}",f"Final URL: {r.url}",f"HTTP status: {r.status_code}"]
        print(f"HTTP {r.status_code} — {r.url}")
        for h,label in checks.items():
            v=r.headers.get(h); print((G+"[PRESENT] "+X if v else R+"[MISSING] "+X)+label+(f": {v}" if v else ""))
            lines.append(f"{label} ({h}): {v or 'MISSING'}")
        save_report("website_security_audit","\n".join(lines))
    except Exception as e: print(R+"Request failed: "+str(e)+X)

def tls_check():
    print(C+"\n[ TLS / SSL CERTIFICATE CHECK ]"+X)
    h=hostclean(input("Hostname: "))
    if not h:return
    try:
        port=int(input("Port [443]: ").strip() or "443")
        ctx=ssl.create_default_context()
        with socket.create_connection((h,port),timeout=8) as s:
            with ctx.wrap_socket(s,server_hostname=h) as t:
                cert=t.getpeercert()
                lines=[f"Host: {h}:{port}",f"TLS version: {t.version()}",f"Cipher: {t.cipher()}",f"Subject: {cert.get('subject')}",f"Issuer: {cert.get('issuer')}",f"Valid until: {cert.get('notAfter')}"]
                print("\n".join(lines)); save_report("tls_check","\n".join(lines))
    except Exception as e: print(R+"TLS check failed: "+str(e)+X)

def port_check():
    print(R+"\n[ AUTHORIZED TCP PORT CHECK ]"+X)
    print(Y+"Only check a device/server you own or have explicit permission to test."+X)
    h=hostclean(input("Authorized host/IP: "))
    if not h:return
    try:
        ports=list(dict.fromkeys(int(p.strip()) for p in input("Ports (comma-separated, max 20): ").split(",") if p.strip()))
        if not ports or len(ports)>20 or any(p<1 or p>65535 for p in ports): raise ValueError()
    except ValueError: print(R+"Enter 1–20 ports between 1 and 65535."+X); return
    lines=[f"Host: {h}"]
    for p in ports:
        try:
            with socket.create_connection((h,p),timeout=1.5): print(G+f"[OPEN] {p}"+X); lines.append(f"OPEN {p}")
        except OSError: print(D+f"[closed/filtered] {p}"+X); lines.append(f"CLOSED/FILTERED {p}")
    save_report("authorized_port_check","\n".join(lines))

def local_network():
    print(C+"\n[ LOCAL NETWORK INFORMATION ]"+X)
    lines=[f"Hostname: {socket.gethostname()}"]
    try:
        lines.append("Local addresses: "+", ".join(sorted(set(i[4][0] for i in socket.getaddrinfo(socket.gethostname(),None)))))
    except Exception as e: lines.append("Address lookup: "+str(e))
    if "ANDROID_ROOT" in os.environ:
        lines.append("Wi-Fi details: Android restricts some Wi-Fi data; use device Settings for SSID/gateway.")
    else:
        route=run_cmd(["ip","route"])
        if route: lines.append("IP route:\n"+route)
        else: lines.append("Route command not available.")
    print("\n".join(lines)); save_report("local_network","\n".join(lines))

def password_generator():
    print(C+"\n[ SECURE PASSWORD GENERATOR ]"+X)
    try:n=int(input("Length (12–128): "))
    except ValueError: print(R+"Invalid length."+X); return
    if not 12<=n<=128: print(R+"Choose 12–128."+X); return
    alphabet=string.ascii_letters+string.digits+"!@#$%^&*()-_=+[]{}?"
    p="".join(secrets.choice(alphabet) for _ in range(n))
    print(G+"\nGenerated password (keep private):\n"+X+p)
    save_report("password_generator","Generated locally. Secret intentionally not written to report.")

def password_strength():
    print(Y+"Do not enter a password you currently use; use a sample."+X)
    p=input("Sample password: ")
    score=sum([len(p)>=12,bool(re.search(r"[a-z]",p)),bool(re.search(r"[A-Z]",p)),bool(re.search(r"\d",p)),bool(re.search(r"[^A-Za-z0-9]",p))])
    labels=["Very weak","Weak","Fair","Good","Strong","Very strong"]
    print("Estimated strength: "+(G if score>=4 else Y if score>=3 else R)+labels[score]+X)
    print(D+"Simple estimate only; not a guarantee against cracking."+X)

def hash_checker():
    print(C+"\n[ FILE SHA-256 CHECKER ]"+X)
    p=input("File path: ").strip().strip('"')
    if not os.path.isfile(p): print(R+"File not found."+X); return
    h=hashlib.sha256()
    try:
        with open(p,"rb") as f:
            for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
        digest=h.hexdigest(); print(G+"SHA-256: "+X+digest); save_report("sha256_file",f"File: {p}\nSHA-256: {digest}")
    except Exception as e: print(R+str(e)+X)

def reports_center():
    fs=sorted(f for f in os.listdir(REPORT_DIR) if f.endswith(".txt"))
    if not fs: print(Y+"No reports yet."+X); return
    for i,f in enumerate(fs[-30:],1): print(f"{G}[{i}]{X} {f}")
    c=input("Report number (Enter to return): ").strip()
    if not c:return
    try:
        with open(os.path.join(REPORT_DIR,fs[-30:][int(c)-1]),encoding="utf-8") as f: print(f.read())
    except Exception: print(R+"Invalid selection."+X)

def help_screen():
    print(C+"\n[ HELP / SAFE USE ]"+X)
    print("• Phone number lookup reports numbering-plan metadata only; it cannot reveal subscriber identity or live GPS.")
    print("• Public IP location is approximate and may point to a carrier/VPN gateway.")
    print("• Website/DNS/TLS checks can fail because of connectivity or server restrictions.")
    print("• Port checks are limited to 20 manually selected ports on authorized systems.")
    print("• Reports are stored locally in ./reports/")
    print("• This toolkit does not perform exploitation, credential theft, Wi-Fi cracking, or stealth activity.")

def main():
    actions={"1":phone_number_info,"2":device_info,"3":public_ip_info,"4":dns_lookup,"5":website_audit,"6":tls_check,"7":port_check,"8":local_network,"9":password_generator,"10":password_strength,"11":hash_checker,"12":reports_center,"h":help_screen}
    while True:
        clear(); banner()
        menu=[
            ("1","Phone Number Intelligence",C),("2","Phone / Device Information",G),
            ("3","Public IP Intelligence",B),("4","DNS Record Lookup",C),
            ("5","Website Security Header Audit",G),("6","TLS / SSL Certificate Check",B),
            ("7","Authorized TCP Port Check",R),("8","Local Network Information",C),
            ("9","Secure Password Generator",G),("10","Password Strength Estimator",Y),
            ("11","File SHA-256 Integrity Checker",B),("12","Reports Center",M),
            ("H","Help / Safe Use Guide",Y),("0","Exit",R)]
        for k,label,col in menu: print(f" {G}[{k:>2}]{X}  {col}{label}{X}")
        choice=input(f"\n{G}PHANTOM {R}>{X} ").strip().lower()
        if choice=="0": print(G+"Phantom signing off. Stay safe."+X); break
        fn=actions.get(choice)
        if fn:
            try: fn()
            except KeyboardInterrupt: print(Y+"\nCancelled."+X)
            pause()
        else: print(R+"Unknown option."+X); pause()

if __name__=="__main__":
    try: main()
    except KeyboardInterrupt: print("\nExiting.")
