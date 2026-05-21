<div align="center">

```
██████╗ ███████╗██╗███████╗    ██████╗ ███████╗███╗   ██╗████████╗
██╔══██╗██╔════╝██║╚════██╗   ██╔═══██╗██╔════╝████╗  ██║╚══██╔══╝
██████╔╝█████╗  ██║    ██╔╝   ██║   ██║███████╗██╔██╗ ██║   ██║   
██╔══██╗██╔══╝  ██║   ██╔╝    ██║   ██║╚════██║██║╚██╗██║   ██║   
██║  ██║███████╗██║   ██║     ╚██████╔╝███████║██║ ╚████║   ██║   
╚═╝  ╚═╝╚══════╝╚═╝   ╚═╝      ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝  
```

# REiS OSINT v3.0
### Public Intelligence Engine — Hamza Hack Team

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/Lisans-Etik%20%26%20Yasal%20OSINT-green?style=flat-square)
![Version](https://img.shields.io/badge/Versiyon-3.0-red?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=flat-square)

**Açık kaynak verilerden derin profil analizi yapan, Groq AI destekli OSINT aracı.**

> ⚠️ **Yasal Uyarı:** Bu araç yalnızca **herkese açık (public) veriler** üzerinde çalışır.  
> Yalnızca **etik ve yasal** OSINT amaçları için kullanın. Kötüye kullanımdan kullanıcı sorumludur.

</div>

---

## 🚀 Özellikler

- **🐙 GitHub Analizi** — Profil, repo, dil dağılımı ve commit geçmişinden e-posta sızdırma
- **🤖 Reddit Analizi** — Profil, karma, aktif subredditler, gönderi ve yorum geçmişi
- **🌐 Web / Haber Taraması** — Bing ve DuckDuckGo üzerinden çok motorlu web istihbaratı
- **👤 Username Enumeration** — 60+ platformda kullanıcı adı sorgulaması (GitHub, Twitter, Instagram, TikTok vb.)
- **📧 E-posta Analizi** — Haveibeenpwned, Gravatar, email formatı doğrulama ve MX kaydı sorgusu
- **🇹🇷 Türkiye Kaynakları** — Türkiye'ye özel kaynak ve platform taraması
- **🔍 Google Dork Üretici** — Hedef bilgilerine göre otomatik dork sorguları
- **🤖 Groq AI Rapor** — Toplanan verileri analiz eden ücretsiz yapay zeka raporu
- **💾 Rapor Kaydetme** — Tüm sonuçları `.txt` formatında dışa aktar

---

## 📦 Kurulum

```bash
# Repoyu klonla
git clone https://github.com/KULLANICI_ADIN/reis-osint.git
cd reis-osint

# Bağımlılıkları kur
pip install -r requirements.txt
```

### Bağımlılıklar

| Kütüphane | Zorunlu | Açıklama |
|-----------|---------|----------|
| `requests` | ✅ Evet | HTTP istekleri |
| `colorama` | ✅ Evet | Renkli terminal çıktısı |
| `beautifulsoup4` | ⭐ Önerilen | Web scraping (tam işlevsellik) |
| `groq` | ⭐ Önerilen | Groq AI analiz raporu |

---

## ▶️ Kullanım

```bash
python ReisOsint.py
```

### Adımlar:

1. **API Key** — Groq ücretsiz API anahtarını gir (isteğe bağlı, [console.groq.com](https://console.groq.com/keys))
2. **Modül Seçimi** — Hangi modüllerin çalışacağını seç
3. **Hedef Bilgileri** — İsim, kullanıcı adları, e-posta, şehir vb. bilgileri gir (tahmin yeterli)
4. **Analiz** — Araç tüm modülleri çalıştırır ve sonuçları ekrana yazar
5. **Rapor** — İstersen sonuçları `.txt` dosyasına kaydet

### Groq API Key (Ücretsiz):

```bash
# Çevre değişkeni olarak tanımla (önerilen)
export GROQ_API_KEY="gsk_xxxxxxxxxxxx"

# Veya program başlarken elle gir
python ReisOsint.py
```

---

## 📋 Modüller

### 🐙 GitHub Modülü
GitHub Public API kullanarak:
- Gerçek isim, lokasyon, bio, şirket, e-posta (varsa)
- Public repolar, dil dağılımı, yıldız sayıları
- Commit geçmişinden sızdırılan e-posta adresleri

### 🤖 Reddit Modülü
Reddit JSON API kullanarak:
- Karma puanı, hesap yaşı, moderatörlük durumu
- Aktif olduğu subredditler ve gönderi analizi
- Son yorum geçmişi

### 👤 Username Enumeration (60+ Platform)
Tek bir kullanıcı adını 60'tan fazla platformda sorgular:
- Sosyal medya (Instagram, Twitter, TikTok, YouTube)
- Kod platformları (GitHub, GitLab, HackerNews)
- Forum ve topluluklar (Reddit, Steam, Twitch, vb.)

### 📧 E-posta Analizi
- Haveibeenpwned veri sızıntısı sorgusu
- Gravatar profil kontrolü
- E-posta formatı ve domain doğrulama
- MX kayıt sorgusu

### 🔍 Google Dork Üretici
Girilen bilgilere göre otomatik dork sorguları üretir:
```
"Hedef İsim" site:linkedin.com
"Hedef İsim" filetype:pdf
"Hedef İsim" "@gmail.com"
...
```

### 🤖 Groq AI Analiz
Toplanan tüm verileri Groq'un ücretsiz modeline göndererek:
- Dijital ayak izi özeti
- Risk değerlendirmesi
- Öne çıkan bulgular raporu

---

## 📁 Çıktı Formatı

Rapor dosyası otomatik olarak şu formatta kaydedilir:
```
reis_osint_[isim]_[tarih_saat].txt
```

İçerik:
- Hedef bilgileri özeti
- Google dork sorguları
- Manuel tarama linkleri
- Canlı web verileri (GitHub, Reddit, e-posta, vb.)
- Groq AI analiz raporu

---

## 🖥️ Ekran Görüntüsü

```
  ██╗  ██╗ █████╗ ███╗   ███╗███████╗ █████╗     ██╗  ██╗ █████╗  ██████╗██╗  ██╗
  ...
  REiS OSINT v3.0  —  Public Intelligence Engine
  Powered by Groq AI (Free)  +  Live Web Intelligence
```

---

## ⚙️ Gereksinimler

- Python 3.8 veya üzeri
- İnternet bağlantısı
- (Opsiyonel) Groq ücretsiz hesabı

---

## ⚖️ Yasal ve Etik Kullanım

Bu araç **yalnızca etik ve yasal OSINT** amaçları için geliştirilmiştir:

- ✅ Yalnızca herkese açık (public) veriler işlenir
- ✅ Kendi dijital ayak izini araştırmak
- ✅ Güvenlik araştırmaları ve CTF
- ✅ Kurumsal açık kaynak istihbaratı (yetkili)
- ❌ Kişileri izinsiz takip etmek veya taciz etmek
- ❌ Yasadışı veri toplama veya profilleme
- ❌ Kötü niyetli kullanım

**Kullanıcı, bu aracı nasıl kullandığından tamamen kendisi sorumludur.**

---

## 👨‍💻 Geliştirici

**Hamza Hack Team**  
REiS OSINT v3.0 — Public Intelligence Engine

---

<div align="center">
<sub>⚠️ Yalnızca etik & yasal OSINT için kullanın — Hamza Hack Team</sub>
</div>
