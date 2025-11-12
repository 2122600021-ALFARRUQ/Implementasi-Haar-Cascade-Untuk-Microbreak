## Implementasi Haar Cascade untuk Microbreak
Proyek ini dibuat untuk mencegah kelelahan fisik dan mental, seperti bagi para pekerja yang berhubungan dengan komputer dalam cakupan waktu yang cukup lama. Pengguna dapat mengetahui waktu yang ideal untuk bekerja maupun mengambil istirahat kecil selama pekerjaan, yang mana penting untuk menjaga fokus dan kesehatan fisik dan mental berdasarkan rutinitas pekerjaan.

## Support By :
Dosen Pengampu : Akhmad Hendriawan ST., MT. (NIP.197501272002121003)
Mata kuliah : Pengolahan Citra
Program Studi : D4 Teknik Elektronika
Politeknik Elektronika Negeri Surabaya

Anggota kelompok:  
Kelompok 6 :  
Al Farruq Rodhiyatul A.    (2122600021)  
Yunanta Adi Wijaya         (2122600035)  
Dewangga Pratama Ikko P.   (2122600052)  
Dewa Gede Angkasa A.       (2122600059)

## 📘 Deskripsi Proyek  
**Microbreak Detection** adalah aplikasi berbasis Python dan OpenCV yang memantau keberadaan pengguna melalui kamera untuk membantu menjaga kesehatan saat bekerja di depan komputer.  
Program ini secara otomatis menghitung waktu kerja dan waktu istirahat berdasarkan deteksi wajah.

---

## 🎯 Tujuan Proyek

1. Mengembangkan sistem deteksi pengguna berbasis kamera untuk memantau aktivitas kerja.  
2. Mengimplementasikan timer break yang **otomatis berhenti dan melanjutkan** sesuai deteksi wajah.  
3. Menyediakan antarmuka sederhana yang menampilkan **status kerja dan waktu istirahat**.  
4. Mendukung peningkatan kesadaran ergonomi kerja melalui pendekatan berbasis teknologi.

---

## ⚙️ Fitur Utama  

### 1️⃣ Konfigurasi Waktu  
- Input durasi kerja, istirahat, dan timeout dalam **menit** (mendukung nilai desimal, contoh: 1.5 menit).  
- Timeout digunakan untuk menentukan kapan wajah dianggap hilang dan break dimulai.

### 2️⃣ Deteksi Wajah Real-Time  
- Menggunakan **OpenCV Haar Cascade**.  
- **Work Timer** aktif saat wajah terdeteksi.  
- Timer otomatis **berhenti** bila wajah tidak terlihat.

### 3️⃣ Manajemen Waktu Otomatis  
- Masuk mode **istirahat otomatis** bila wajah hilang melebihi timeout.  
- Timer istirahat berhenti bila wajah kembali terlihat.  
- Terdapat pop-up pengingat "Waktunya Istirahat" dengan opsi **Mulai Break** atau **Tunda 5 Menit (Snooze)**.

### 4️⃣ Mode Selesai & Reset  
- Setelah waktu istirahat selesai, kamera dimatikan otomatis.  
- Program kembali ke menu konfigurasi awal untuk sesi berikutnya.

---

## 🧩 Teknologi & Library yang Digunakan

### Teknologi

| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| **Python** | 3.x | Bahasa pemrograman utama |
| **OpenCV (cv2)** | Latest | Computer vision & deteksi wajah |
| **Tkinter** | Built-in | Framework GUI |
| **PIL/Pillow** | Latest | Manipulasi & rendering gambar |

### Komponen Computer Vision

| Komponen | Deskripsi | File |
|----------|-----------|------|
| **Haar Cascade Classifier** | Algoritma deteksi wajah berbasis fitur Haar | `haarcascade_frontalface_default.xml` |
| **Face Detection** | Real-time face tracking | OpenCV built-in |
| **Histogram Equalization** | Meningkatkan akurasi deteksi | `cv2.equalizeHist()` |

### Parameter Deteksi Berdasarkan Resolusi

| Resolusi | Dimensi | Scale Factor | Min Neighbors | Min Face Size |
|----------|---------|--------------|---------------|---------------|
| **140p** | 256 × 140 | 1.03 | 2 | 13px |
| **240p** | 320 × 240 | 1.05 | 3 | 16px |
| **480p** | 640 × 480 | 1.10 | 5 | 32px |
| **720p** | 1280 × 720 | 1.12 | 6 | 64px |
| **1080p** | 1920 × 1080 | 1.15 | 7 | 96px |

---
## 🧭 Alur Kerja Sistem
![Alt text](https://github.com/2122600021-ALFARRUQ/Implementasi-Haar-Cascade-Untuk-Microbreak/blob/ec81bc419444c6c91b2ffa09badbded1ef665f36/Alur_Program_Deteksi_Wajah.png)

## 🧭 Flowchart Sistem
![Alt text](https://github.com/2122600021-ALFARRUQ/Implementasi-Haar-Cascade-Untuk-Microbreak/blob/c83b80360666de98103237fae1214d8836fc99b6/Flowchart%20Microbreak.jpeg)

## Dokumentasi 
Link video: https://youtu.be/0EhADgEiu3U

## Analisis Hasil 

## Kesimpulan

## Saran Update


