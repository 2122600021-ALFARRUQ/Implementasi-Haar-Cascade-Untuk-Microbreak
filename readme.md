# 🧠 Microbreak Detector  
**Deteksi Wajah Otomatis untuk Mengatur Waktu Istirahat dan Kerja**

---

## 📘 Deskripsi Proyek  
**Microbreak Detector** adalah aplikasi berbasis Python dan OpenCV yang memantau keberadaan pengguna melalui kamera untuk membantu menjaga kesehatan saat bekerja di depan komputer.  
Program ini secara otomatis menghitung waktu kerja dan waktu istirahat berdasarkan deteksi wajah.

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

## 🧩 Arsitektur Program  

