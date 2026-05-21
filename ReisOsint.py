#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ╔══════════════════════════════════════════════════════════════════╗
# ║          HAMZA HACK TEAM — REiS OSINT v3.0                      ║
# ║     Açık Kaynak İstihbarat & Derin Profil Analiz Sistemi        ║
# ║                                                                  ║
# ║  Kurucu  : Hamza Hack Team                                       ║
# ║  Versiyon: 3.0 — Public Intelligence Engine                     ║
# ║  Lisans  : Yalnızca etik ve yasal OSINT amaçlı                  ║
# ║  Notlar  : Sadece herkese açık (public) veriler işlenir          ║
# ╚══════════════════════════════════════════════════════════════════╝

# ─── Hamza Hack Team — Core Imports ───
import os, sys, re, json, time, html, urllib.parse, urllib.request
import subprocess, threading, queue, socket
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Hamza Hack Team — Optional Imports ───
try:
    import requests
    from requests.adapters import HTTPAdapter
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False

try:
    from colorama import init, Fore, Style, Back
    init(autoreset=True)
    C = True
except ImportError:
    C = False
    class Fore:
        RED=GREEN=YELLOW=CYAN=MAGENTA=BLUE=WHITE=RESET=""
    class Style:
        BRIGHT=DIM=RESET_ALL=""
    class Back:
        BLACK=""

try:
    from bs4 import BeautifulSoup
    BS4_OK = True
except ImportError:
    BS4_OK = False

try:
    from groq import Groq
    GROQ_OK = True
except ImportError:
    GROQ_OK = False

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — BANNER & UI
# ═══════════════════════════════════════════════════════════

BANNER = r"""
{C}{B}
  ██╗  ██╗ █████╗ ███╗   ███╗███████╗ █████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗
  ██║  ██║██╔══██╗████╗ ████║╚════██║██╔══██╗    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
  ███████║███████║██╔████╔██║    ██╔╝███████║    ███████║███████║██║     █████╔╝ 
  ██╔══██║██╔══██║██║╚██╔╝██║   ██╔╝ ██╔══██║    ██╔══██║██╔══██║██║     ██╔═██╗ 
  ██║  ██║██║  ██║██║ ╚═╝ ██║   ██║  ██║  ██║    ██║  ██║██║  ██║╚██████╗██║  ██╗
  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝   ╚═╝  ╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{Y}
                    ████████╗███████╗ █████╗ ███╗   ███╗    
                    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║   
                       ██║   █████╗  ███████║██╔████╔██║   
                       ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║   
                       ██║   ███████╗██║  ██║██║ ╚═╝ ██║   
                       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝   
{R}
         ██████╗ ███████╗██╗███╗   ██╗████████╗    ██╗   ██╗██████╗     ██████╗ 
         ██╔══██╗██╔════╝██║████╗  ██║╚══██╔══╝    ██║   ██║╚════██╗   ██╔═████╗
         ██║  ██║███████╗██║██╔██╗ ██║   ██║       ██║   ██║ █████╔╝   ██║██╔██║
         ██║  ██║╚════██║██║██║╚██╗██║   ██║       ╚██╗ ██╔╝ ╚═══██╗   ████╔╝██║
         ██████╔╝███████║██║██║ ╚████║   ██║        ╚████╔╝ ██████╔╝██╗╚██████╔╝
         ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝         ╚═══╝  ╚═════╝ ╚═╝ ╚═════╝ 
{W}
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │          REiS OSINT v3.0  —  Public Intelligence Engine                    │
  │          Powered by Groq AI (Free)  +  Live Web Intelligence               │
  │  ⚠  Yalnızca herkese açık (public) veriler  •  Etik & Yasal OSINT  ⚠     │
  └─────────────────────────────────────────────────────────────────────────────┘
{E}"""

def banner():
    b = BANNER
    b = b.replace("{C}", Fore.CYAN + Style.BRIGHT)
    b = b.replace("{Y}", Fore.YELLOW + Style.BRIGHT)
    b = b.replace("{R}", Fore.RED + Style.BRIGHT)
    b = b.replace("{W}", Fore.WHITE)
    b = b.replace("{E}", Style.RESET_ALL)
    print(b)

def sec(title, color=Fore.CYAN):
    print(f"\n{color}{Style.BRIGHT}{'═'*70}\n  ⬡  {title}\n{'═'*70}{Style.RESET_ALL}")

def subsec(title):
    print(f"\n  {Fore.YELLOW}{Style.BRIGHT}── {title} ──{Style.RESET_ALL}")

def ok(m):   print(f"  {Fore.GREEN}[✓]{Style.RESET_ALL} {m}")
def info(m): print(f"  {Fore.CYAN}[i]{Style.RESET_ALL} {m}")
def warn(m): print(f"  {Fore.YELLOW}[!]{Style.RESET_ALL} {m}")
def err(m):  print(f"  {Fore.RED}[✗]{Style.RESET_ALL} {m}")
def found(m):print(f"  {Fore.MAGENTA}[★]{Style.RESET_ALL} {Fore.WHITE}{Style.BRIGHT}{m}{Style.RESET_ALL}")
def data_line(k, v): print(f"    {Fore.CYAN}{k:<28}{Style.RESET_ALL} {Fore.WHITE}{v}{Style.RESET_ALL}")

def ask(prompt, default=""):
    try:
        val = input(f"\n  {Fore.YELLOW}▶{Style.RESET_ALL} {prompt}: ").strip()
        return val if val else default
    except (EOFError, KeyboardInterrupt):
        return default

def ask_multi(prompt):
    try:
        val = input(f"\n  {Fore.YELLOW}▶{Style.RESET_ALL} {prompt}\n    {Fore.CYAN}(virgülle ayır, boş geçilebilir){Style.RESET_ALL}: ").strip()
        if not val: return []
        return [v.strip() for v in val.split(",") if v.strip()]
    except (EOFError, KeyboardInterrupt):
        return []

def spinner_msg(msg):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    for i in range(20):
        print(f"\r  {Fore.CYAN}{chars[i%len(chars)]}{Style.RESET_ALL} {msg}...", end="", flush=True)
        time.sleep(0.08)
    print(f"\r  {Fore.GREEN}[✓]{Style.RESET_ALL} {msg}... tamamlandı    ")

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — HTTP SESSION
# ═══════════════════════════════════════════════════════════

# ─── Hamza Hack Team — Browser-like headers to avoid basic blocks ───
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "DNT": "1",
}

def get_session():
    if not REQUESTS_OK:
        return None
    s = requests.Session()
    s.headers.update(HEADERS)
    s.max_redirects = 5
    return s

SESSION = None

def fetch(url, timeout=12, params=None):
    # ─── Hamza Hack Team — Safe fetch wrapper ───
    global SESSION
    if SESSION is None:
        SESSION = get_session()
    if SESSION is None:
        return None
    try:
        r = SESSION.get(url, timeout=timeout, params=params, allow_redirects=True)
        r.raise_for_status()
        return r
    except Exception:
        return None

def fetch_json(url, timeout=10, headers_extra=None):
    # ─── Hamza Hack Team — JSON API fetcher ───
    global SESSION
    if SESSION is None:
        SESSION = get_session()
    if SESSION is None:
        return None
    try:
        h = dict(HEADERS)
        h["Accept"] = "application/json"
        if headers_extra:
            h.update(headers_extra)
        r = SESSION.get(url, timeout=timeout, headers=h)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — VERİ TOPLAMA FORMU
# ═══════════════════════════════════════════════════════════

def collect_target():
    sec("🎯 HEDEF BİLGİLERİ — HAMZA HACK TEAM", Fore.CYAN)
    warn("Bilgiler ipucu niteliğindedir. Kesin olmak zorunda değil.\n")

    d = {}

    subsec("Temel Kimlik")
    d["isim"]           = ask("İsim / Alias / Takma ad")
    d["diger_isimler"]  = ask_multi("Diğer olası isimler / sahte isimler")
    d["yas"]            = ask("Yaş veya aralık (örn: 27 veya 1995-2000 arası)")
    d["cinsiyet"]       = ask("Cinsiyet ipucu")
    d["uyruk"]          = ask("Uyruk / milliyet")
    d["diller"]         = ask_multi("Konuştuğu diller")

    subsec("Konum İpuçları")
    d["gercek_sehir"]   = ask("Gerçek / köken şehir (belki dışarıya gizliyor)")
    d["gorunen_sehir"]  = ask("Görünen / yaşadığı şehir")
    d["ulke"]           = ask("Ülke")
    d["konum_detay"]    = ask("Ek konum detayı (mahalle, semt, bölge)")

    subsec("Mesleki")
    d["meslek"]         = ask("Meslek / sektör")
    d["sirket"]         = ask("Çalıştığı / çalışmış olabileceği şirket")
    d["egitim"]         = ask("Okul / üniversite / bölüm")
    d["beceriler"]      = ask_multi("Teknik beceriler / uzmanlıklar")

    subsec("Dijital Kimlik — Sosyal Medya")
    d["kullanici_adlari"] = ask_multi("Bilinen kullanıcı adları / handle'lar")
    d["instagram"]        = ask("Instagram kullanıcı adı")
    d["twitter"]          = ask("Twitter / X kullanıcı adı")
    d["linkedin_url"]     = ask("LinkedIn URL veya profil adı")
    d["github"]           = ask("GitHub kullanıcı adı")
    d["facebook"]         = ask("Facebook profil adı / URL")
    d["tiktok"]           = ask("TikTok kullanıcı adı")
    d["youtube"]          = ask("YouTube kanal adı / URL")
    d["reddit"]           = ask("Reddit kullanıcı adı")
    d["telegram"]         = ask("Telegram kullanıcı adı")
    d["discord"]          = ask("Discord tag")
    d["diger_platform"]   = ask_multi("Diğer platform / forum adları")

    subsec("İletişim & Domain")
    d["email"]          = ask_multi("E-posta adresi(leri) (tahmini de olur)")
    d["telefon"]        = ask("Telefon (kısmi / tahmini)")
    d["website"]        = ask("Web sitesi / blog / domain")

    subsec("Kişisel İpuçları")
    d["ilgi_alanlari"]  = ask_multi("İlgi alanları / hobiler")
    d["siyasi"]         = ask("Siyasi / ideolojik eğilim ipucu")
    d["dini"]           = ask("Dini / kültürel arka plan ipucu")
    d["karakter"]       = ask("Karakter / kişilik özellikleri")
    d["cevresi"]        = ask_multi("Bilinen çevre / arkadaşlar / iş ortakları")
    d["ek"]             = ask("Ek notlar / önemli ipuçları")

    return {k: v for k, v in d.items() if v not in [None, "", []]}

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — MODÜL 1: GITHUB PUBLIC API
# ═══════════════════════════════════════════════════════════

def module_github(data):
    # ─── Hamza Hack Team — GitHub Public API scraper ───
    results = {}
    username = data.get("github", "")
    if not username:
        for uid in data.get("kullanici_adlari", []):
            username = uid
            break
    if not username:
        return results

    sec(f"🐙 GITHUB ANALİZİ: @{username}", Fore.GREEN)

    # Profil
    info("Profil bilgileri çekiliyor...")
    profile = fetch_json(f"https://api.github.com/users/{username}")
    if profile and "login" in profile:
        results["github_profil"] = {
            "kullanici": profile.get("login"),
            "gercek_isim": profile.get("name"),
            "bio": profile.get("bio"),
            "lokasyon": profile.get("location"),
            "email": profile.get("email"),
            "sirket": profile.get("company"),
            "website": profile.get("blog"),
            "twitter": profile.get("twitter_username"),
            "repo_sayisi": profile.get("public_repos"),
            "takipci": profile.get("followers"),
            "takip_edilen": profile.get("following"),
            "kayit_tarihi": profile.get("created_at"),
            "son_guncelleme": profile.get("updated_at"),
            "herkese_acik_gist": profile.get("public_gists"),
        }
        ok("Profil bulundu!")
        for k, v in results["github_profil"].items():
            if v:
                data_line(k, str(v))

        # Repos
        info("Public repolar taranıyor...")
        repos = fetch_json(f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated")
        if repos and isinstance(repos, list):
            repo_data = []
            langs = {}
            for r in repos[:30]:
                lang = r.get("language") or "N/A"
                langs[lang] = langs.get(lang, 0) + 1
                repo_data.append({
                    "isim": r.get("name"),
                    "aciklama": r.get("description"),
                    "dil": lang,
                    "yildiz": r.get("stargazers_count"),
                    "fork": r.get("forks_count"),
                    "guncelleme": r.get("updated_at", "")[:10],
                    "url": r.get("html_url"),
                })
            results["github_repolar"] = repo_data
            results["github_diller"] = langs
            ok(f"{len(repo_data)} repo bulundu")
            subsec("Dil dağılımı")
            for lang, cnt in sorted(langs.items(), key=lambda x: -x[1]):
                data_line(lang, f"{cnt} repo")

        # Gist commits için email sızdırma
        info("Commit geçmişinden email ipucu aranıyor...")
        events = fetch_json(f"https://api.github.com/users/{username}/events/public?per_page=100")
        emails_found = set()
        commit_msgs = []
        if events and isinstance(events, list):
            for ev in events:
                if ev.get("type") == "PushEvent":
                    for commit in ev.get("payload", {}).get("commits", []):
                        author = commit.get("author", {})
                        em = author.get("email", "")
                        if em and "noreply" not in em and em not in emails_found:
                            emails_found.add(em)
                            found(f"Commit'ten email bulundu: {em}")
                        msg = commit.get("message", "")
                        if msg:
                            commit_msgs.append(msg[:100])
        if emails_found:
            results["github_emails"] = list(emails_found)
        if commit_msgs:
            results["github_commit_mesajlari"] = commit_msgs[:20]
            subsec("Son commit mesajları")
            for cm in commit_msgs[:10]:
                print(f"    {Fore.WHITE}• {cm}{Style.RESET_ALL}")

    else:
        warn(f"GitHub profili bulunamadı veya API limiti aşıldı: @{username}")

    return results

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — MODÜL 2: REDDIT PUBLIC API
# ═══════════════════════════════════════════════════════════

def module_reddit(data):
    # ─── Hamza Hack Team — Reddit Public JSON API ───
    username = data.get("reddit", "")
    if not username:
        return {}

    sec(f"🤖 REDDIT ANALİZİ: u/{username}", Fore.RED)
    results = {}

    profile = fetch_json(f"https://www.reddit.com/user/{username}/about.json",
                         headers_extra={"Accept": "application/json"})
    if profile and "data" in profile:
        d = profile["data"]
        results["reddit_profil"] = {
            "kullanici": d.get("name"),
            "karma_post": d.get("link_karma"),
            "karma_yorum": d.get("comment_karma"),
            "hesap_yasi_unix": d.get("created_utc"),
            "premium": d.get("is_gold"),
            "moderator": d.get("is_mod"),
            "aciklama": d.get("subreddit", {}).get("public_description"),
        }
        ok("Reddit profili bulundu!")
        for k, v in results["reddit_profil"].items():
            if v:
                data_line(k, str(v))
    else:
        warn("Reddit profili bulunamadı ya da gizli.")
        return results

    # Son gönderiler
    info("Son gönderiler çekiliyor...")
    posts = fetch_json(f"https://www.reddit.com/user/{username}/submitted.json?limit=25")
    if posts and "data" in posts:
        post_list = []
        subreddits = {}
        for p in posts["data"].get("children", []):
            pd = p.get("data", {})
            sr = pd.get("subreddit", "")
            subreddits[sr] = subreddits.get(sr, 0) + 1
            post_list.append({
                "baslik": pd.get("title", "")[:100],
                "subreddit": sr,
                "puan": pd.get("score"),
                "tarih": datetime.utcfromtimestamp(pd.get("created_utc", 0)).strftime("%Y-%m-%d"),
                "url": "https://reddit.com" + pd.get("permalink", ""),
            })
        results["reddit_gonderiler"] = post_list
        results["reddit_subredditler"] = subreddits
        ok(f"{len(post_list)} gönderi bulundu")
        subsec("Aktif olduğu subredditler")
        for sr, cnt in sorted(subreddits.items(), key=lambda x: -x[1])[:10]:
            data_line(f"r/{sr}", f"{cnt} gönderi")

    # Son yorumlar
    info("Son yorumlar çekiliyor...")
    comments = fetch_json(f"https://www.reddit.com/user/{username}/comments.json?limit=25")
    if comments and "data" in comments:
        comment_list = []
        for c in comments["data"].get("children", []):
            cd = c.get("data", {})
            comment_list.append({
                "metin": cd.get("body", "")[:200],
                "subreddit": cd.get("subreddit"),
                "puan": cd.get("score"),
                "tarih": datetime.utcfromtimestamp(cd.get("created_utc", 0)).strftime("%Y-%m-%d"),
            })
        results["reddit_yorumlar"] = comment_list
        subsec("Son yorumlardan örnekler")
        for c in comment_list[:5]:
            print(f"    {Fore.CYAN}[r/{c['subreddit']}]{Style.RESET_ALL} {c['metin'][:120]}")

    return results

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — MODÜL 3: HABER & WEB ARAMA
# ═══════════════════════════════════════════════════════════

def scrape_text(html_content, max_chars=2000):
    # ─── Hamza Hack Team — Clean HTML to text ───
    if not html_content:
        return ""
    if BS4_OK:
        soup = BeautifulSoup(html_content, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()
        return " ".join(soup.get_text(separator=" ").split())[:max_chars]
    else:
        clean = re.sub(r"<[^>]+>", " ", html_content)
        clean = html.unescape(clean)
        return " ".join(clean.split())[:max_chars]

def search_bing(query, num=10):
    # ─── Hamza Hack Team — Bing scraper (public search) ───
    results = []
    url = "https://www.bing.com/search"
    r = fetch(url, params={"q": query, "count": num})
    if not r:
        return results
    if BS4_OK:
        soup = BeautifulSoup(r.text, "html.parser")
        for li in soup.select("li.b_algo")[:num]:
            title_el = li.select_one("h2 a")
            snippet_el = li.select_one(".b_caption p")
            if title_el:
                results.append({
                    "baslik": title_el.get_text(strip=True),
                    "url": title_el.get("href", ""),
                    "ozet": snippet_el.get_text(strip=True) if snippet_el else "",
                })
    else:
        # regex fallback
        titles = re.findall(r'<h2[^>]*><a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', r.text)
        for href, title in titles[:num]:
            results.append({"baslik": title, "url": href, "ozet": ""})
    return results

def search_duckduckgo(query, num=10):
    # ─── Hamza Hack Team — DuckDuckGo HTML search ───
    results = []
    url = "https://html.duckduckgo.com/html/"
    r = fetch(url, params={"q": query})
    if not r:
        return results
    if BS4_OK:
        soup = BeautifulSoup(r.text, "html.parser")
        for div in soup.select(".result__body")[:num]:
            title_el = div.select_one(".result__title a")
            snippet_el = div.select_one(".result__snippet")
            if title_el:
                raw_href = title_el.get("href", "")
                # DDG wraps URLs
                m = re.search(r"uddg=([^&]+)", raw_href)
                clean_url = urllib.parse.unquote(m.group(1)) if m else raw_href
                results.append({
                    "baslik": title_el.get_text(strip=True),
                    "url": clean_url,
                    "ozet": snippet_el.get_text(strip=True) if snippet_el else "",
                })
    return results

def module_web_search(data):
    # ─── Hamza Hack Team — Multi-engine web intelligence ───
    sec("🌐 WEB İSTİHBARAT TARAMASI — HAMZA HACK TEAM", Fore.YELLOW)
    results = {}
    isim = data.get("isim", "")
    sehir = data.get("gercek_sehir") or data.get("gorunen_sehir", "")
    meslek = data.get("meslek", "")
    email_list = data.get("email", [])

    queries = []
    if isim:
        queries.append((f'"{isim}"', "genel_arama"))
        if sehir:
            queries.append((f'"{isim}" "{sehir}"', "sehir_arama"))
        if meslek:
            queries.append((f'"{isim}" "{meslek}"', "meslek_arama"))
        queries.append((f'"{isim}" site:twitter.com OR site:x.com', "twitter_arama"))
        queries.append((f'"{isim}" site:linkedin.com', "linkedin_arama"))
        queries.append((f'"{isim}" haber OR haberler', "haber_arama"))
        queries.append((f'"{isim}" filetype:pdf OR filetype:doc', "dosya_arama"))
        queries.append((f'"{isim}" instagram OR facebook OR tiktok', "sosyal_arama"))
    for em in email_list[:2]:
        queries.append((f'"{em}"', f"email_arama_{em[:10]}"))

    for uid in data.get("kullanici_adlari", [])[:3]:
        queries.append((f'"{uid}"', f"uid_arama_{uid}"))

    all_hits = {}
    for query, key in queries:
        info(f"Aranıyor: {query}")
        hits = search_bing(query, num=8)
        if not hits:
            hits = search_duckduckgo(query, num=8)
        if hits:
            all_hits[key] = hits
            ok(f"{len(hits)} sonuç bulundu")
            for h in hits[:3]:
                print(f"    {Fore.WHITE}• {h['baslik'][:80]}{Style.RESET_ALL}")
                if h.get("ozet"):
                    print(f"      {Fore.CYAN}{h['ozet'][:120]}{Style.RESET_ALL}")
        else:
            warn(f"Sonuç bulunamadı: {query}")
        time.sleep(0.8)  # Hamza Hack Team — rate limit koruması

    results["web_arama"] = all_hits
    return results

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — MODÜL 4: USERNAME ENUMERATION
# ═══════════════════════════════════════════════════════════

# ─── Hamza Hack Team — 60+ platform listesi ───
PLATFORMS = [
    ("GitHub",         "https://github.com/{}",                        200, None),
    ("GitLab",         "https://gitlab.com/{}",                        200, None),
    ("Reddit",         "https://www.reddit.com/user/{}",               200, "User Overview"),
    ("Twitter/X",      "https://x.com/{}",                             200, None),
    ("Instagram",      "https://www.instagram.com/{}/",                200, "og:title"),
    ("TikTok",         "https://www.tiktok.com/@{}",                   200, None),
    ("YouTube",        "https://www.youtube.com/@{}",                  200, None),
    ("Pinterest",      "https://www.pinterest.com/{}/",                200, None),
    ("Twitch",         "https://www.twitch.tv/{}",                     200, None),
    ("Steam",          "https://steamcommunity.com/id/{}",             200, None),
    ("Pastebin",       "https://pastebin.com/u/{}",                    200, None),
    ("HackerNews",     "https://news.ycombinator.com/user?id={}",      200, None),
    ("Dev.to",         "https://dev.to/{}",                            200, None),
    ("Medium",         "https://medium.com/@{}",                       200, None),
    ("Substack",       "https://{}.substack.com",                      200, None),
    ("Keybase",        "https://keybase.io/{}",                        200, None),
    ("Gravatar",       "https://en.gravatar.com/{}",                   200, None),
    ("About.me",       "https://about.me/{}",                          200, None),
    ("Linktree",       "https://linktr.ee/{}",                         200, None),
    ("Replit",         "https://replit.com/@{}",                       200, None),
    ("Codepen",        "https://codepen.io/{}",                        200, None),
    ("Stackoverflow",  "https://stackoverflow.com/users/{}",           200, None),
    ("Behance",        "https://www.behance.net/{}",                   200, None),
    ("Dribbble",       "https://dribbble.com/{}",                      200, None),
    ("Fiverr",         "https://www.fiverr.com/{}",                    200, None),
    ("Etsy",           "https://www.etsy.com/shop/{}",                 200, None),
    ("Soundcloud",     "https://soundcloud.com/{}",                    200, None),
    ("Spotify",        "https://open.spotify.com/user/{}",             200, None),
    ("Last.fm",        "https://www.last.fm/user/{}",                  200, None),
    ("Flickr",         "https://www.flickr.com/people/{}",             200, None),
    ("500px",          "https://500px.com/p/{}",                       200, None),
    ("Vimeo",          "https://vimeo.com/{}",                         200, None),
    ("Dailymotion",    "https://www.dailymotion.com/{}",               200, None),
    ("Tumblr",         "https://{}.tumblr.com",                        200, None),
    ("Wordpress",      "https://{}.wordpress.com",                     200, None),
    ("Wix",            "https://www.wix.com/website/{}",               200, None),
    ("Quora",          "https://www.quora.com/profile/{}",             200, None),
    ("ProductHunt",    "https://www.producthunt.com/@{}",              200, None),
    ("AngelList",      "https://angel.co/u/{}",                        200, None),
    ("Crunchbase",     "https://www.crunchbase.com/person/{}",         200, None),
    ("Foursquare",     "https://foursquare.com/{}",                    200, None),
    ("Strava",         "https://www.strava.com/athletes/{}",           200, None),
    ("Duolingo",       "https://www.duolingo.com/profile/{}",          200, None),
    ("Chess.com",      "https://www.chess.com/member/{}",              200, None),
    ("Lichess",        "https://lichess.org/@/{}",                     200, None),
    ("Telegram",       "https://t.me/{}",                              200, None),
    ("Mastodon",       "https://mastodon.social/@{}",                  200, None),
    ("Bluesky",        "https://bsky.app/profile/{}",                  200, None),
    ("VK",             "https://vk.com/{}",                            200, None),
    ("OK.ru",          "https://ok.ru/profile/{}",                     200, None),
    ("Weibo",          "https://weibo.com/u/{}",                       200, None),
    ("Eksisozluk",     "https://eksisozluk.com/biri/{}",               200, None),
    ("Uludagsozluk",   "https://www.uludagsozluk.com/yazar/{}",        200, None),
    ("Itunes",         "https://itunes.apple.com/profile/{}",          200, None),
    ("Npmjs",          "https://www.npmjs.com/~{}",                    200, None),
    ("Pypi",           "https://pypi.org/user/{}/",                    200, None),
    ("Hackerone",      "https://hackerone.com/{}",                     200, None),
    ("Bugcrowd",       "https://bugcrowd.com/{}",                      200, None),
]

def check_platform(username, name, url_tpl, ok_code, content_check):
    # ─── Hamza Hack Team — Single platform checker ───
    url = url_tpl.format(username)
    try:
        r = fetch(url, timeout=8)
        if r is None:
            return None
        if r.status_code == ok_code:
            if content_check:
                if content_check.lower() in r.text.lower():
                    return (name, url, r.status_code)
            else:
                return (name, url, r.status_code)
        return None
    except Exception:
        return None

def module_username_enum(data):
    # ─── Hamza Hack Team — Multi-platform username hunter ───
    usernames = list(data.get("kullanici_adlari", []))
    for field in ["instagram", "twitter", "github", "reddit", "tiktok", "youtube", "telegram"]:
        val = data.get(field, "")
        if val and val not in usernames:
            usernames.append(val)

    if not usernames:
        isim = data.get("isim", "")
        if isim:
            # isimden tahminler üret
            parts = isim.lower().split()
            if len(parts) >= 2:
                usernames = [
                    parts[0] + parts[1],
                    parts[0] + "." + parts[1],
                    parts[0] + "_" + parts[1],
                    parts[0][0] + parts[1],
                    parts[0],
                ]
            else:
                usernames = [isim.lower().replace(" ", "")]

    sec("🔍 USERNAME ENUMERATION — 60+ PLATFORM", Fore.MAGENTA)
    info(f"Hedef kullanıcı adları: {', '.join(usernames)}")
    warn("Bu işlem birkaç dakika sürebilir...\n")

    results = {}
    for username in usernames[:5]:
        found_platforms = []
        info(f"Taranan: @{username}")
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = {
                ex.submit(check_platform, username, name, url_tpl, ok_code, cc): name
                for name, url_tpl, ok_code, cc in PLATFORMS
            }
            completed = 0
            for future in as_completed(futures):
                completed += 1
                print(f"\r    {Fore.CYAN}İlerleme: {completed}/{len(PLATFORMS)}{Style.RESET_ALL}", end="", flush=True)
                result = future.result()
                if result:
                    found_platforms.append(result)
        print()
        if found_platforms:
            ok(f"@{username} için {len(found_platforms)} platform bulundu!")
            for name, url, status in found_platforms:
                found(f"{name:<20} → {url}")
        else:
            warn(f"@{username} için aktif platform bulunamadı.")
        results[username] = found_platforms
        time.sleep(0.5)

    return results

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — MODÜL 5: EMAIL OSINT
# ═══════════════════════════════════════════════════════════

def module_email(data):
    # ─── Hamza Hack Team — Email intelligence ───
    email_list = data.get("email", [])
    if not email_list:
        return {}

    sec("📧 E-POSTA OSTİNT ANALİZİ — HAMZA HACK TEAM", Fore.BLUE)
    results = {}

    for email in email_list[:3]:
        info(f"Analiz ediliyor: {email}")
        em_results = {}

        # Domain analizi
        parts = email.split("@")
        if len(parts) == 2:
            domain = parts[1]
            em_results["domain"] = domain
            em_results["kullanici_kismi"] = parts[0]

            # Domain MX kontrolü
            try:
                ip = socket.gethostbyname(domain)
                em_results["domain_ip"] = ip
                ok(f"Domain çözümlendi: {domain} → {ip}")
            except Exception:
                warn(f"Domain çözümlenemedi: {domain}")

        # Gravatar kontrolü
        try:
            import hashlib
            email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
            gravatar_url = f"https://www.gravatar.com/{email_hash}.json"
            grav = fetch_json(gravatar_url)
            if grav and "entry" in grav:
                entry = grav["entry"][0]
                em_results["gravatar"] = {
                    "username": entry.get("preferredUsername"),
                    "display_name": entry.get("displayName"),
                    "location": entry.get("currentLocation"),
                    "about": entry.get("aboutMe"),
                    "profil_url": entry.get("profileUrl"),
                    "hesaplar": [acc.get("domain") for acc in entry.get("accounts", [])],
                }
                found(f"Gravatar profili bulundu: {entry.get('displayName')}")
                for acc_domain in em_results["gravatar"]["hesaplar"]:
                    found(f"Bağlı hesap: {acc_domain}")
            em_results["gravatar_img"] = f"https://www.gravatar.com/avatar/{email_hash}?d=404"
        except Exception:
            pass

        results[email] = em_results
        subsec(f"{email} Özeti")
        for k, v in em_results.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    if vv:
                        data_line(f"  {kk}", str(vv)[:80])
            elif v:
                data_line(k, str(v)[:80])

    return results

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — MODÜL 6: TÜRKYE SPESIFIK TARAMA
# ═══════════════════════════════════════════════════════════

def module_turkey(data):
    # ─── Hamza Hack Team — Turkey-specific OSINT sources ───
    sec("🇹🇷 TÜRKİYE SPESİFİK TARAMA — HAMZA HACK TEAM", Fore.RED)
    isim = data.get("isim", "")
    if not isim:
        return {}

    q = urllib.parse.quote_plus(isim)
    results = {}
    sources = [
        ("Ekşi Sözlük",    f"https://eksisozluk.com/?q={q}"),
        ("Haberler.com",   f"https://www.haberler.com/arama/?q={q}"),
        ("Sabah",          f"https://www.sabah.com.tr/arama/{q}"),
        ("Hürriyet",       f"https://www.hurriyet.com.tr/arama/?q={q}"),
        ("Milliyet",       f"https://www.milliyet.com.tr/arama/{q}"),
        ("NTV",            f"https://www.ntv.com.tr/arama/{q}"),
        ("CNN Türk",       f"https://www.cnnturk.com/arama?query={q}"),
        ("YÖKSİS",         f"https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?adiSoyadi={q}"),
        ("Google Scholar", f"https://scholar.google.com/scholar?q={q}"),
        ("Onedio",         f"https://onedio.com/search?q={q}"),
    ]

    info(f"Türkiye kaynaklarında taraniyor: {isim}")
    hits = {}

    for name, url in sources:
        info(f"Kontrol ediliyor: {name}")
        r = fetch(url, timeout=10)
        if r and r.status_code == 200:
            text = scrape_text(r.text, 3000)
            isim_lower = isim.lower()
            isim_parts = isim_lower.split()
            mentions = sum(1 for p in isim_parts if p in text.lower())
            if mentions >= len(isim_parts):
                found(f"{name}: İçerik bulundu! → {url}")
                hits[name] = {"url": url, "ozet": text[:300]}
            else:
                print(f"    {Fore.CYAN}─{Style.RESET_ALL} {name}: Doğrudan eşleşme yok")
        else:
            warn(f"{name}: Erişilemedi")
        time.sleep(0.5)

    results["turkiye_kaynaklar"] = hits
    if hits:
        ok(f"{len(hits)} kaynakta içerik bulundu!")
    return results

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — GOOGLE DORK ÜRETICI
# ═══════════════════════════════════════════════════════════

def generate_dorks(data):
    # ─── Hamza Hack Team — Advanced dork generator ───
    dorks = []
    isim = data.get("isim", "")
    sehir = data.get("gercek_sehir") or data.get("gorunen_sehir", "")
    meslek = data.get("meslek", "")
    sirket = data.get("sirket", "")
    email_list = data.get("email", [])
    uid_list = data.get("kullanici_adlari", [])
    website = data.get("website", "")
    insta = data.get("instagram", "")
    github = data.get("github", "")

    if isim:
        q = f'"{isim}"'
        dorks += [
            f'{q}',
            f'{q} site:linkedin.com',
            f'{q} site:instagram.com',
            f'{q} site:twitter.com OR site:x.com',
            f'{q} site:facebook.com',
            f'{q} site:tiktok.com',
            f'{q} site:reddit.com',
            f'{q} site:github.com',
            f'{q} filetype:pdf',
            f'{q} filetype:doc OR filetype:docx',
            f'{q} inurl:about OR inurl:profile OR inurl:bio',
            f'{q} "telefon" OR "phone" OR "iletisim"',
        ]
        if sehir:
            dorks += [f'{q} "{sehir}"', f'"{isim}" "{sehir}" site:linkedin.com']
        if meslek:
            dorks += [f'{q} "{meslek}"', f'"{isim}" "{meslek}" site:linkedin.com']
        if sirket:
            dorks += [f'{q} "{sirket}"', f'site:{sirket.lower().replace(" ","")}.com "{isim}"']
        dorks += [
            f'{q} site:eksisozluk.com',
            f'{q} site:haberler.com OR site:hurriyet.com.tr OR site:sabah.com.tr',
            f'{q} site:uludagsozluk.com',
        ]

    for em in email_list:
        dorks += [f'"{em}"', f'"{em}" -site:linkedin.com', f'"{em}" pastebin OR hastebin']
    for uid in uid_list:
        dorks += [f'"{uid}"', f'inurl:"{uid}"', f'"{uid}" site:pastebin.com']
    if insta:
        dorks.append(f'site:instagram.com "{insta}"')
    if github:
        dorks.append(f'site:github.com "{github}"')
    if website:
        dom = website.replace("https://","").replace("http://","").split("/")[0]
        dorks += [f'site:{dom}', f'link:{dom}', f'"{dom}" inurl:pdf']

    return dorks

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — MANUEL LİNKLER
# ═══════════════════════════════════════════════════════════

def generate_manual_links(data):
    # ─── Hamza Hack Team — Comprehensive manual link generator ───
    q = urllib.parse.quote_plus(data.get("isim", ""))
    email_list = data.get("email", [])
    email = email_list[0] if email_list else ""
    eq = urllib.parse.quote_plus(email)
    domain = (data.get("website") or "").replace("https://","").replace("http://","").split("/")[0]
    uid_list = data.get("kullanici_adlari", [])
    uid = uid_list[0] if uid_list else (data.get("github") or data.get("instagram") or "")
    uq = urllib.parse.quote_plus(uid)

    links = {
        "🔍 Arama Motorları": [
            ("Google",           f"https://www.google.com/search?q={q}"),
            ("Bing",             f"https://www.bing.com/search?q={q}"),
            ("DuckDuckGo",       f"https://duckduckgo.com/?q={q}"),
            ("Yandex",           f"https://yandex.com/search/?text={q}"),
            ("Brave Search",     f"https://search.brave.com/search?q={q}"),
            ("Google Cache",     f"https://webcache.googleusercontent.com/search?q=cache:{q}"),
        ],
        "👤 Kişi Arama": [
            ("Pipl",             "https://pipl.com/"),
            ("Spokeo",           f"https://www.spokeo.com/search?q={q}"),
            ("BeenVerified",     "https://www.beenverified.com/"),
            ("TruePeopleSearch", f"https://www.truepeoplesearch.com/results?name={q}"),
            ("Intelius",         "https://www.intelius.com/"),
            ("WhitePages",       f"https://www.whitepages.com/name/{q}"),
        ],
        "📱 Sosyal Medya": [
            ("Sherlock (GitHub)","https://github.com/sherlock-project/sherlock"),
            ("WhatsMyName",      "https://whatsmyname.app/"),
            ("Namechk",          "https://namechk.com/"),
            ("UserSearch.org",   f"https://usersearch.org/results_normal.php?URL_username={uq}"),
            ("Social Searcher",  f"https://www.social-searcher.com/social-buzz/?q={q}"),
            ("LinkedIn",         f"https://www.linkedin.com/search/results/people/?keywords={q}"),
            ("Twitter/X",        f"https://x.com/search?q={q}&f=user"),
            ("Instagram",        f"https://www.instagram.com/{uq}/"),
            ("Facebook",         f"https://www.facebook.com/search/people?q={q}"),
            ("TikTok",           f"https://www.tiktok.com/search/user?q={uq}"),
            ("Reddit",           f"https://www.reddit.com/search/?q={q}&type=user"),
            ("GitHub",           f"https://github.com/search?q={uq}&type=users"),
            ("YouTube",          f"https://www.youtube.com/results?search_query={q}"),
            ("Telegram",         f"https://t.me/{uq}"),
            ("Mastodon",         f"https://mastodon.social/@{uq}"),
        ],
        "📧 E-posta Araçları": [
            ("HaveIBeenPwned",   f"https://haveibeenpwned.com/account/{eq}" if email else "https://haveibeenpwned.com/"),
            ("Hunter.io",        f"https://hunter.io/email-verifier/{eq}" if email else "https://hunter.io/"),
            ("Epieos",           f"https://epieos.com/?q={eq}&t=email" if email else "https://epieos.com/"),
            ("EmailRep.io",      f"https://emailrep.io/{eq}" if email else "https://emailrep.io/"),
            ("IntelX",           "https://intelx.io/"),
            ("Phonebook.cz",     f"https://phonebook.cz/?q={eq}&type=email" if email else "https://phonebook.cz/"),
            ("Snov.io",          "https://snov.io/email-finder"),
            ("Gravatar",         f"https://en.gravatar.com/{uq}"),
        ],
        "🌐 Domain / IP": [
            ("WHOIS",            f"https://www.whois.com/whois/{domain}" if domain else "https://www.whois.com/"),
            ("Shodan",           f"https://www.shodan.io/search?query={domain}" if domain else "https://www.shodan.io/"),
            ("VirusTotal",       f"https://www.virustotal.com/gui/domain/{domain}" if domain else "https://www.virustotal.com/"),
            ("Censys",           "https://censys.io/"),
            ("DNSDumpster",      "https://dnsdumpster.com/"),
            ("Wayback Machine",  f"https://web.archive.org/web/*/{domain}" if domain else "https://web.archive.org/"),
            ("SecurityTrails",   f"https://securitytrails.com/domain/{domain}" if domain else "https://securitytrails.com/"),
            ("BuiltWith",        f"https://builtwith.com/{domain}" if domain else "https://builtwith.com/"),
        ],
        "📸 Görsel & Medya": [
            ("PimEyes",          "https://pimeyes.com/en"),
            ("TinEye",           "https://tineye.com/"),
            ("Google Görseller", f"https://images.google.com/search?q={q}&tbm=isch"),
            ("Yandex Görseller", f"https://yandex.com/images/search?text={q}"),
        ],
        "🔓 Sızıntı & Darkweb": [
            ("IntelX",           "https://intelx.io/"),
            ("Dehashed",         "https://dehashed.com/"),
            ("LeakCheck",        "https://leakcheck.io/"),
            ("BreachDirectory",  "https://breachdirectory.org/"),
            ("Snusbase",         "https://snusbase.com/"),
            ("Pastebin Dork",    f"https://www.google.com/search?q=site:pastebin.com+{q}"),
        ],
        "🇹🇷 Türkiye Özel": [
            ("Ekşi Sözlük",      f"https://eksisozluk.com/?q={q}"),
            ("Uludağ Sözlük",    f"https://www.uludagsozluk.com/yazar/{uq}"),
            ("Haberler.com",     f"https://www.haberler.com/arama/?q={q}"),
            ("Sabah",            f"https://www.sabah.com.tr/arama/{q}"),
            ("Hürriyet",         f"https://www.hurriyet.com.tr/arama/?q={q}"),
            ("NTV",              f"https://www.ntv.com.tr/arama/{q}"),
            ("YÖKSİS",           f"https://akademik.yok.gov.tr/AkademikArama/AkademisyenArama?adiSoyadi={q}"),
            ("Google Scholar TR",f"https://scholar.google.com.tr/scholar?q={q}"),
            ("Onedio",           f"https://onedio.com/search?q={q}"),
            ("UYAP (Dava)",      "https://www.uyap.gov.tr/"),
        ],
        "🔭 İleri OSINT": [
            ("Maltego CE",       "https://www.maltego.com/maltego-community/"),
            ("OSINT Framework",  "https://osintframework.com/"),
            ("IntelTechniques",  "https://inteltechniques.com/tools/"),
            ("Bellingcat Toolkit","https://www.bellingcat.com/resources/how-tos/"),
            ("SpiderFoot HX",    "https://www.spiderfoot.net/"),
            ("Recon-ng (GitHub)","https://github.com/lanmaster53/recon-ng"),
        ],
    }
    return links

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — GROQ ANALİZİ
# ═══════════════════════════════════════════════════════════

GROQ_SYSTEM = """Sen REiS — Hamza Hack Team'in geliştirdiği OSINT analiz yapay zekasısın.

GÖREV:
Kullanıcının sağladığı ipuçları ve canlı web'den toplanan verilerden derin bir istihbarat profili çıkar.

KURALLAR:
1. Verilen bilgiler ipucu niteliğindedir — "kesinlikle X'tir" değil, "ipuçları X'e işaret ediyor" de.
2. Çelişkileri tespit et: örn. gerçek şehir ile görünen şehir farklıysa bunu analiz et.
3. Dijital ayak izini yorumla: hangi platformlarda ne tür içerik paylaşıyor?
4. Gerçek kişisel veri ÜRETME — mevcut ipuçlarını analiz et sadece.
5. Türkçe, profesyonel, net yaz.

ÇIKTI YAPISI:
## HEDEF PROFİLİ
## DİJİTAL KİMLİK ANALİZİ
## ÇELIŞKILER & GİZLENEN BİLGİLER
## BULUNAN VERİLERİN YORUMU
## ÖNERİLEN SONRAKI ADIMLAR
## GOOGLE DORK STRATEJİSİ
## RİSK & ETKİ DEĞERLENDİRMESİ
"""

def run_groq(data, intel_results, api_key):
    # ─── Hamza Hack Team — Groq AI deep analysis ───
    if not GROQ_OK:
        err("groq kütüphanesi yüklü değil: pip install groq")
        return None

    sec("🤖 GROQ AI DERİN ANALİZ — HAMZA HACK TEAM", Fore.MAGENTA)
    client = Groq(api_key=api_key)

    # Prompt oluştur
    lines = ["=== GİRDİ İPUÇLARI ==="]
    field_labels = {
        "isim":"İsim/Alias","diger_isimler":"Diğer isimler","yas":"Yaş",
        "cinsiyet":"Cinsiyet","uyruk":"Uyruk","diller":"Diller",
        "gercek_sehir":"Gerçek köken şehri (belki gizliyor)","gorunen_sehir":"Görünen şehir",
        "ulke":"Ülke","konum_detay":"Konum detayı","meslek":"Meslek","sirket":"Şirket",
        "egitim":"Eğitim","beceriler":"Beceriler","kullanici_adlari":"Kullanıcı adları",
        "instagram":"Instagram","twitter":"Twitter","linkedin_url":"LinkedIn",
        "github":"GitHub","facebook":"Facebook","tiktok":"TikTok","youtube":"YouTube",
        "reddit":"Reddit","telegram":"Telegram","email":"E-posta","telefon":"Telefon",
        "website":"Website","ilgi_alanlari":"İlgi alanları","siyasi":"Siyasi eğilim",
        "dini":"Dini/kültürel","karakter":"Karakter","cevresi":"Çevre","ek":"Ek notlar",
    }
    for k, lbl in field_labels.items():
        v = data.get(k)
        if v:
            val = ", ".join(v) if isinstance(v, list) else str(v)
            lines.append(f"- {lbl}: {val}")

    lines.append("\n=== CANLI WEB'DEN TOPLANAN VERİLER ===")

    # GitHub
    gh = intel_results.get("github", {})
    if gh.get("github_profil"):
        p = gh["github_profil"]
        lines.append(f"\nGitHub Profili: {p.get('kullanici')} | İsim: {p.get('gercek_isim')} | "
                      f"Lokasyon: {p.get('lokasyon')} | Email: {p.get('email')} | "
                      f"Bio: {p.get('bio')} | Repos: {p.get('repo_sayisi')}")
        if gh.get("github_diller"):
            langs = ", ".join([f"{k}({v})" for k,v in list(gh["github_diller"].items())[:5]])
            lines.append(f"GitHub Dilleri: {langs}")
        if gh.get("github_emails"):
            lines.append(f"Commit'lerden email: {', '.join(gh['github_emails'])}")
        if gh.get("github_commit_mesajlari"):
            msgs = " | ".join(gh["github_commit_mesajlari"][:5])
            lines.append(f"Commit mesajları: {msgs}")

    # Reddit
    rd = intel_results.get("reddit", {})
    if rd.get("reddit_profil"):
        p = rd["reddit_profil"]
        lines.append(f"\nReddit: {p.get('kullanici')} | Karma: {p.get('karma_post')}/{p.get('karma_yorum')} | Moderator: {p.get('moderator')}")
        if rd.get("reddit_subredditler"):
            subs = ", ".join([f"r/{k}({v})" for k,v in list(rd["reddit_subredditler"].items())[:5]])
            lines.append(f"Aktif subredditler: {subs}")
        if rd.get("reddit_yorumlar"):
            sample = rd["reddit_yorumlar"][0].get("metin","")[:150]
            lines.append(f"Örnek yorum: {sample}")

    # Web arama
    web = intel_results.get("web", {}).get("web_arama", {})
    for key, hits in list(web.items())[:3]:
        if hits:
            titles = " | ".join([h["baslik"][:60] for h in hits[:3]])
            lines.append(f"Web araması [{key}]: {titles}")

    # Türkiye
    tr_data = intel_results.get("turkey", {}).get("turkiye_kaynaklar", {})
    if tr_data:
        for src, d_src in tr_data.items():
            lines.append(f"Türkiye kaynağı [{src}]: {d_src.get('ozet','')[:150]}")

    # Email
    em_data = intel_results.get("email", {})
    for em, em_r in em_data.items():
        if em_r.get("gravatar"):
            g = em_r["gravatar"]
            lines.append(f"Gravatar [{em}]: {g.get('display_name')} | {g.get('location')} | Hesaplar: {g.get('hesaplar')}")

    # Username enum
    uid_data = intel_results.get("username", {})
    for uid, platforms in uid_data.items():
        if platforms:
            pnames = ", ".join([p[0] for p in platforms])
            lines.append(f"@{uid} platformları: {pnames}")

    user_msg = "\n".join(lines)
    user_msg += "\n\nLütfen yukarıdaki tüm verileri sentezleyerek kapsamlı OSINT analizi yap."

    models = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]

    for model in models:
        try:
            info(f"Model: {model}")
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": GROQ_SYSTEM},
                    {"role": "user", "content": user_msg},
                ],
                temperature=0.35,
                max_tokens=4096,
            )
            result = completion.choices[0].message.content
            ok(f"Analiz tamamlandı ({model})")
            return result
        except Exception as e:
            warn(f"{model}: {e}")
            time.sleep(1)
    return None

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — RAPOR KAYDET
# ═══════════════════════════════════════════════════════════

def save_report(data, intel_results, dorks, links, ai_result):
    # ─── Hamza Hack Team — Full report writer ───
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    isim = data.get("isim", "hedef").replace(" ", "_")
    filename = f"hamza_hackteam_osint_{isim}_{ts}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("       HAMZA HACK TEAM — REiS OSINT v3.0\n")
        f.write("       Açık Kaynak İstihbarat Raporu\n")
        f.write(f"       Tarih: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")

        f.write("━" * 70 + "\nGİRDİ İPUÇLARI\n" + "━" * 70 + "\n")
        for k, v in data.items():
            val = ", ".join(v) if isinstance(v, list) else str(v)
            f.write(f"  {k:<25}: {val}\n")

        f.write("\n" + "━" * 70 + "\nGOOGLE DORK SORGULARI\n" + "━" * 70 + "\n")
        for i, d in enumerate(dorks, 1):
            f.write(f"  {i:>3}. {d}\n")

        f.write("\n" + "━" * 70 + "\nMANUEL TARAMA LİNKLERİ\n" + "━" * 70 + "\n")
        for cat, items in links.items():
            f.write(f"\n{cat}\n")
            for name, url in items:
                if url:
                    f.write(f"  {name:<25} {url}\n")

        # Intel sonuçları
        f.write("\n" + "━" * 70 + "\nCAN LI WEB VERİLERİ\n" + "━" * 70 + "\n")

        gh = intel_results.get("github", {})
        if gh:
            f.write("\nGITHUB:\n")
            if gh.get("github_profil"):
                for k, v in gh["github_profil"].items():
                    if v: f.write(f"  {k}: {v}\n")
            if gh.get("github_emails"):
                f.write(f"  Commit emailler: {', '.join(gh['github_emails'])}\n")
            if gh.get("github_repolar"):
                f.write(f"  Repolar ({len(gh['github_repolar'])}):\n")
                for r in gh["github_repolar"][:10]:
                    f.write(f"    • {r['isim']} [{r['dil']}] ⭐{r['yildiz']} — {(r.get('aciklama') or '')[:60]}\n")
    
        uid_data = intel_results.get("username", {})
        if uid_data:
            f.write("\nPLATFORM ENUMERATION:\n")
            for uid, platforms in uid_data.items():
                f.write(f"  @{uid}:\n")
                for name, url, _ in platforms:
                    f.write(f"    ✓ {name:<20} {url}\n")

        em_data = intel_results.get("email", {})
        if em_data:
            f.write("\nEMAIL ANALİZİ:\n")
            for em, em_r in em_data.items():
                f.write(f"  {em}:\n")
                for k, v in em_r.items():
                    if v: f.write(f"    {k}: {v}\n")

        tr_data = intel_results.get("turkey", {})
        if tr_data.get("turkiye_kaynaklar"):
            f.write("\nTÜRKİYE KAYNAKLARI:\n")
            for src, sr in tr_data["turkiye_kaynaklar"].items():
                f.write(f"  ✓ {src}: {sr['url']}\n")
                f.write(f"    {sr['ozet'][:200]}\n\n")

        if ai_result:
            f.write("\n" + "━" * 70 + "\nGROQ AI ANALİZ RAPORU — HAMZA HACK TEAM\n" + "━" * 70 + "\n")
            f.write(ai_result + "\n")

        f.write("\n" + "=" * 70 + "\n")
        f.write("       Hamza Hack Team — REiS OSINT v3.0\n")
        f.write("       Yalnızca etik ve yasal OSINT için kullanın.\n")
        f.write("=" * 70 + "\n")

    return filename

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — DORK YAZDIRICI
# ═══════════════════════════════════════════════════════════

def print_dorks(dorks):
    sec("🔍 GOOGLE DORK SORGULARI — HAMZA HACK TEAM", Fore.GREEN)
    for i, d in enumerate(dorks, 1):
        print(f"  {Fore.GREEN}{i:>3}.{Style.RESET_ALL} {d}")

def print_links(links):
    sec("🔗 MANUEL TARAMA LİNKLERİ — HAMZA HACK TEAM", Fore.YELLOW)
    for cat, items in links.items():
        print(f"\n  {Fore.YELLOW}{Style.BRIGHT}{cat}{Style.RESET_ALL}")
        for name, url in items:
            if url:
                print(f"    {Fore.WHITE}{name:<25}{Style.RESET_ALL} {Fore.CYAN}{url}{Style.RESET_ALL}")

def print_ai(result):
    sec("🤖 GROQ AI ANALİZ RAPORU — HAMZA HACK TEAM", Fore.MAGENTA)
    if result:
        for line in result.split("\n"):
            if line.strip().startswith("##"):
                print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{line}{Style.RESET_ALL}")
            elif line.strip().startswith("-") or line.strip().startswith("•"):
                print(f"  {Fore.WHITE}{line}{Style.RESET_ALL}")
            else:
                print(line)
    else:
        err("AI analizi alınamadı.")

# ═══════════════════════════════════════════════════════════
#  HAMZA HACK TEAM — ANA PROGRAM
# ═══════════════════════════════════════════════════════════

def main():
    banner()

    if not REQUESTS_OK:
        err("requests kütüphanesi eksik: pip install requests")
        sys.exit(1)

    sec("🔑 API ANAHTARLARI — HAMZA HACK TEAM", Fore.YELLOW)
    info("Groq ücretsiz API: https://console.groq.com/keys")
    info("Çevre değişkeni: export GROQ_API_KEY='...'")
    print()

    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        api_key = ask("Groq API Key (boş bırakırsan AI analizi atlanır)")

    if not api_key:
        warn("API key yok — AI analizi atlanacak.")
    else:
        ok("API key alındı.")

    # Modül seçimi
    sec("⚙  MODÜL SEÇİMİ — HAMZA HACK TEAM", Fore.CYAN)
    info("Hangi modülleri çalıştırmak istiyorsunuz?")
    print()
    run_github  = ask("GitHub analizi çalıştır? (e/h)", "e").lower() == "e"
    run_reddit  = ask("Reddit analizi çalıştır? (e/h)", "e").lower() == "e"
    run_web     = ask("Web/haber araması yap? (e/h)", "e").lower() == "e"
    run_uid     = ask("Username enumeration (60+ platform)? (e/h)", "e").lower() == "e"
    run_email   = ask("E-posta analizi yap? (e/h)", "e").lower() == "e"
    run_turkey  = ask("Türkiye kaynaklarını tara? (e/h)", "e").lower() == "e"

    # Veri topla
    data = collect_target()
    if not data:
        err("Hiç bilgi girilmedi.")
        sys.exit(1)

    # Özet
    sec("📋 GİRDİ ÖZETİ", Fore.WHITE)
    for k, v in data.items():
        val = ", ".join(v) if isinstance(v, list) else str(v)
        data_line(k, val)

    input(f"\n  {Fore.YELLOW}▶{Style.RESET_ALL} Analize başlamak için Enter'a basın...")

    # ─── Hamza Hack Team — Run all modules ───
    intel_results = {}

    if run_github and data.get("github"):
        intel_results["github"] = module_github(data)

    if run_reddit and data.get("reddit"):
        intel_results["reddit"] = module_reddit(data)

    if run_email and data.get("email"):
        intel_results["email"] = module_email(data)

    if run_uid:
        intel_results["username"] = module_username_enum(data)

    if run_turkey:
        intel_results["turkey"] = module_turkey(data)

    if run_web:
        intel_results["web"] = module_web_search(data)

    # Dorklar ve linkler
    dorks = generate_dorks(data)
    links = generate_manual_links(data)

    # AI analizi
    ai_result = None
    if api_key and GROQ_OK:
        ai_result = run_groq(data, intel_results, api_key)
    elif api_key and not GROQ_OK:
        err("groq kütüphanesi yok: pip install groq")

    # Çıktılar
    print_dorks(dorks)
    print_links(links)
    if ai_result:
        print_ai(ai_result)

    # Kaydet
    sec("💾 RAPOR KAYDET — HAMZA HACK TEAM", Fore.GREEN)
    if ask("Raporu dosyaya kaydet? (e/h)", "e").lower() != "h":
        fn = save_report(data, intel_results, dorks, links, ai_result)
        ok(f"Rapor kaydedildi: {Fore.CYAN}{fn}{Style.RESET_ALL}")

    sec("✅ HAMZA HACK TEAM — TAMAMLANDI", Fore.GREEN)
    print(f"""
  {Fore.CYAN}╔══════════════════════════════════════════════════════╗
  ║   HAMZA HACK TEAM — REiS OSINT v3.0 — İŞ TAMAMLANDI  ║
  ║   Yalnızca etik & yasal OSINT için kullanın.          ║
  ╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n  {Fore.YELLOW}[!]{Style.RESET_ALL} Hamza Hack Team — Kullanıcı tarafından durduruldu.")
        sys.exit(0)
    except Exception as e:
        print(f"\n  {Fore.RED}[✗]{Style.RESET_ALL} Hata: {e}")
        import traceback
        traceback.print_exc()
