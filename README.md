# quantum-phone-diver
## 📋 DAFTAR ISI
- [📱 TENTANG TOOLS](#-tentang-tools)
- [✨ FITUR LENGKAP](#-fitur-lengkap)
- [⚡ INSTALASI CEPAT](#-instalasi-cepat)
- [🎯 CARA PENGGUNAAN](#-cara-penggunaan)
- [🔑 API KEY](#-api-key)
- [📊 CONTOH OUTPUT](#-contoh-output)
- [🛠️ STRUKTUR FILE](#️-struktur-file)
- [❓ TROUBLESHOOTING](#-troubleshooting)
- [📜 LISENSI](#-lisensi)
- [👑 KREDIT](#-kredit)

---

## 🎯 CARA PENGGUNAAN

### 🟢 METODE 1: INTERACTIVE MENU (PALING MUDAH)
```bash
python quantum_phone_diver.py
Lalu pilih menu:
[1] Single Scan
[2] Batch Scan
[3] Export Report
[4] Konfigurasi API
# Scan nomor +62
python quantum_phone_diver.py -p "+6281234567890"

# Scan + export CSV
python quantum_phone_diver.py -p "+6281234567890" -o csv

# Scan + export HTML
python quantum_phone_diver.py -p "+6281234567890" -o html

# Buat file targets.txt, isi:
+6281234567890
+6289876543210

# Jalankan batch scan
python quantum_phone_diver.py -f targets.txt -o both

# CSV untuk Excel
-o csv

# HTML untuk presentasi
-o html

# Keduanya
-o both
