
---

## 📋 DAFTAR ISI

- [TENTANG TOOLS](#-tentang-tools)
- [FITUR LENGKAP](#-fitur-lengkap)
- [INSTALASI](#-instalasi)
- [KONFIGURASI API KEY](#-konfigurasi-api-key)
- [CARAPAKAI](#-cara-pakai)
- [CONTOH OUTPUT](#-contoh-output)
- [STRUKTUR FILE](#-struktur-file)
- [TROUBLESHOOTING](#-troubleshooting)
- [LISENSI & KREDIT](#-lisensi--kredit)

---

## 🎯 TENTANG TOOLS

**Quantum Phone Diver v4.0** adalah tools OSINT (Open Source Intelligence) yang dirancang khusus untuk **menganalisis jejak digital nomor telepon**. Tools ini mengumpulkan **data PUBLIK** dari berbagai sumber untuk memberikan informasi seperti:

- Validasi nomor internasional
- Informasi operator & lokasi berdasarkan kode area
- Deteksi registrasi di Telegram, WhatsApp
- Kemungkinan username di Instagram & sosial media
- Link pencarian di 25+ platform
- Email candidates yang terasosiasi
- Cek kebocoran data (breach) via HIBP
- Analisis risiko privasi
- **BUKAN** pelacak lokasi real-time
- **BUKAN** pengambil data NIK/KTP
- **BUKAN** alat hacking ilegal

---

## ✨ FITUR LENGKAP

| **Kategori** | **Fitur** | **Status** | **Keterangan** |
|-------------|----------|------------|----------------|
| 📱 **Validasi** | Format internasional | ✅ | +62xxx, E.164, nasional |
| 📍 **Lokasi** | Kota & provinsi | ✅ | Berdasarkan kode area |
| 🌍 **Koordinat** | PUSAT KOTA | ✅ | ⚠️ BUKAN lokasi individu! |
| 📡 **Operator** | Provider, jaringan | ✅ | Telkomsel, XL, Indosat, dll |
| 👤 **Pemilik** | Nama & gender | ⚠️ | Perlu API NumLookup |
| 📨 **Telegram** | Username & link | ✅ | Deteksi otomatis |
| 💬 **WhatsApp** | Link chat | ✅ | Cek registrasi |
| 📸 **Instagram** | Username candidates | ✅ | 10+ varian |
| 👥 **Facebook** | Link pencarian | ✅ | Search query |
| 🛡️ **Signal** | Link registrasi | ✅ | Cek manual |
| 📧 **Email** | Generate candidates | ✅ | 15+ kemungkinan email |
| 💀 **Breach** | Cek kebocoran data | ⚠️ | Perlu API HIBP |
| 🔑 **Username** | Varian username | ✅ | 15+ varian |
| 🌐 **Sosial Media** | 25+ platform | ✅ | Twitter, TikTok, dll |
| ⚠️ **Risiko** | Analisis privasi | ✅ | Skor & rekomendasi |
| ☁️ **Cuaca** | Info cuaca kota | ⚠️ | Opsional, perlu API |
| 📊 **Export** | CSV & HTML | ✅ | Laporan rapi |

---

## ⚡ INSTALASI

### 📌 PERSYARATAN
- Python 3.8 atau lebih baru
- Pip (Python package manager)
- Koneksi internet
- RAM minimal 256MB (bisa di HP)

### 🪟 WINDOWS
```bash
# 1. Download Python dari python.org (centang "Add to PATH")
# 2. Buka CMD / PowerShell
git clone https://github.com/mrx-n15/quantum-phone-diver.git
cd quantum-phone-diver
pip install -r requirements.txt

█ █
█ 🚨 PERINGATAN KERAS DARI ZAMXYZ 🚨 █
█ █
█ TOOLS INI HANYA UNTUK: █
█ ✅ PENETRATION TESTING DENGAN IZIN █
█ ✅ EDUKASI KEAMANAN DIGITAL █
█ ✅ RESEARCH AKADEMIS █
█ █
█ DILARANG KERAS UNTUK: █
█ ❌ DOXING / STALKING █
█ ❌ NGEHACK MANTAN / TEMEN / MUSUH █
█ ❌ KEJAHATAN SIBER APAPUN █
█ █
█ DOSA TANGGUNG SENDIRI! █
█ ALLAH SWT MAHA MELIHAT! █
█ █
█ "Dan janganlah kamu mencari-cari kesalahan orang █
█ lain." (QS. Al-Hujurat: 12) █
█ █
