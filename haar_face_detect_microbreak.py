"""
microbreak_simple.py
Versi ringan: Form awal -> Jendela deteksi -> Break -> Kembali ke form awal.

Dependencies:
pip install opencv-python Pillow
Tkinter biasanya sudah terpasang bersama Python standar.

Jalankan:
python microbreak_simple.py
"""

import cv2
import time
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# --------------------
# Resolusi & parameter Haar heuristik
# --------------------
RESOLUTIONS = {
    "140p (256x140)": (256, 140),
    "240p (320x240)": (320, 240),
    "480p (640x480)": (640, 480),
    "720p (1280x720)": (1280, 720),
    "1080p (1920x1080)": (1920, 1080),
}

HAAR_PARAMS = {
    "140p (256x140)": {"scale": 1.03, "neighbors": 2},
    "240p (320x240)": {"scale": 1.05, "neighbors": 3},
    "480p (640x480)": {"scale": 1.10, "neighbors": 5},
    "720p (1280x720)": {"scale": 1.12, "neighbors": 6},
    "1080p (1920x1080)": {"scale": 1.15, "neighbors": 7},
}

CASCADE_PATH = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

# --------------------
# Utility parsing safe float (accept comma)
# --------------------
def safe_float_from_str(s, default=0.0):
    try:
        s2 = str(s).strip().replace(",", ".")
        return float(s2)
    except Exception:
        return default

# --------------------
# Main App
# --------------------
class MicrobreakApp:
    def __init__(self, root):
        self.root = root
        root.title("Microbreak")
        self.face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        if self.face_cascade.empty():
            messagebox.showerror("Error", "Gagal memuat Haar Cascade. Pastikan OpenCV terinstal.")
            root.destroy()
            return

        # --- Form variables ---
        self.work_minutes_var = tk.StringVar(value="50")    # default 50 menit
        self.timeout_min_var = tk.StringVar(value="0.2")    # default 0.2 menit (~12 detik)
        self.break_minutes_var = tk.StringVar(value="5")    # default 5 menit
        self.resolution_var = tk.StringVar(value=list(RESOLUTIONS.keys())[1])  # default 240p

        # Build form UI
        self.build_form_ui()

        # detection window variables
        self.cap = None
        self.video_panel = None
        self.detect_window = None
        self.running = False

        # timer state
        self.work_limit_s = 0
        self.timeout_s = 0
        self.break_limit_s = 0

    def build_form_ui(self):
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill=tk.BOTH, expand=True)

        # Work time
        ttk.Label(frm, text="Waktu kerja (menit, bisa desimal):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.work_minutes_var, width=12).grid(row=0, column=1, sticky="w")

        # Timeout
        ttk.Label(frm, text="Timeout (menit, bisa desimal):").grid(row=1, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.timeout_min_var, width=12).grid(row=1, column=1, sticky="w")
        ttk.Label(frm, text="(Durasi wajah hilang sebelum dianggap break)").grid(row=1, column=2, sticky="w", padx=(8, 0))

        # Break time
        ttk.Label(frm, text="Waktu break (menit, bisa desimal):").grid(row=2, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.break_minutes_var, width=12).grid(row=2, column=1, sticky="w")

        # Resolution
        ttk.Label(frm, text="Resolusi kamera:").grid(row=3, column=0, sticky="w")
        ttk.OptionMenu(frm, self.resolution_var, self.resolution_var.get(), *RESOLUTIONS.keys()).grid(row=3, column=1, sticky="w")

        # start button
        start_btn = ttk.Button(frm, text="Start", command=self.on_start)
        start_btn.grid(row=4, column=0, columnspan=2, pady=(10,0))

    # -----------------
    # Start detection -> opens new window
    # -----------------
    def on_start(self):
        # ambil nilai input (semuanya dalam menit)
        work_min = safe_float_from_str(self.work_minutes_var.get(), 50.0)
        timeout_min = safe_float_from_str(self.timeout_min_var.get(), 0.2)
        break_min = safe_float_from_str(self.break_minutes_var.get(), 5.0)
        res_key = self.resolution_var.get()

        # konversi ke detik
        self.work_limit_s = work_min * 60
        self.timeout_s = timeout_min * 60
        self.break_limit_s = break_min * 60

        # prepare camera
        w, h = RESOLUTIONS.get(res_key, (640, 480))
        params = HAAR_PARAMS.get(res_key, {"scale": 1.1, "neighbors": 5})
        self.haar_scale = float(params["scale"])
        self.haar_neighbors = int(params["neighbors"])
        self.min_face_size = max(30, int(0.05 * w))

        # open capture
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW if hasattr(cv2, 'CAP_DSHOW') else 0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        if not self.cap.isOpened():
            messagebox.showerror("Error", "Gagal membuka kamera. Periksa koneksi/akses kamera.")
            return

        # build detection window
        self.detect_window = tk.Toplevel(self.root)
        self.detect_window.title("Deteksi Wajah - Microbreak")
        self.detect_window.protocol("WM_DELETE_WINDOW", self.stop_and_close_detection)

        # video panel
        self.video_panel = ttk.Label(self.detect_window)
        self.video_panel.pack()

        # status labels
        self.status_label = ttk.Label(self.detect_window, text="Status: Idle")
        self.status_label.pack()
        self.timer_label = ttk.Label(self.detect_window, text="Work: 00:00 | Break: 00:00 | Absence: 00s")
        self.timer_label.pack()

        # state
        self.work_elapsed = 0.0
        self.break_elapsed = 0.0
        self.absence_start = None
        self.in_break = False
        self.notified = False

        self.running = True
        self.detect_window.after(20, self.capture_loop)

    def capture_loop(self):
        if not self.running:
            return
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.config(text="Status: Kamera gagal membaca")
            self.detect_window.after(200, self.capture_loop)
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=self.haar_scale,
            minNeighbors=self.haar_neighbors,
            minSize=(self.min_face_size, self.min_face_size)
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        dt = 0.03  # interval frame (≈ 30 fps)

        # ============ LOGIKA PERBAIKAN ============
        if len(faces) > 0:
            # Wajah terdeteksi
            if self.in_break:
                # Saat break tapi wajah masih terlihat -> break pause
                status = "Break paused (wajah terdeteksi)"
            else:
                # Sedang kerja normal
                self.work_elapsed += dt
                status = "Bekerja (wajah terdeteksi)"
            self.absence_start = None

        else:
            # Tidak ada wajah terdeteksi
            if self.absence_start is None:
                self.absence_start = time.time()
            absence_elapsed = time.time() - self.absence_start

            if self.in_break:
                # Break time jalan hanya kalau wajah TIDAK terdeteksi
                self.break_elapsed += dt
                status = f"Istirahat (absence {int(absence_elapsed)}s)"
            else:
                # Mode kerja
                if absence_elapsed < self.timeout_s:
                    status = f"Pause ({int(absence_elapsed)}/{int(self.timeout_s)}s)"
                else:
                    # Timeout tercapai, otomatis masuk break
                    self.in_break = True
                    self.break_elapsed = 0.0
                    self.absence_start = time.time()
                    status = "Mulai istirahat (wajah hilang > timeout)"

        # ==========================================

        # Cek waktu kerja selesai → prompt break
        if (not self.in_break) and (self.work_elapsed >= self.work_limit_s) and (not self.notified):
            self.notified = True
            self.detect_window.after(0, self.work_time_reached_popup)

        # Cek waktu break selesai → kembali ke form
        if self.in_break and (self.break_elapsed >= self.break_limit_s):
            self.detect_window.after(0, self.finish_break_and_return)
            return

        # Render video ke Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        max_w = 700
        if img.width > max_w:
            ratio = max_w / img.width
            img = img.resize((int(img.width * ratio), int(img.height * ratio)))
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_panel.imgtk = imgtk
        self.video_panel.config(image=imgtk)

        # Update timer teks
        work_mm = int(self.work_elapsed) // 60
        work_ss = int(self.work_elapsed) % 60
        break_mm = int(self.break_elapsed) // 60
        break_ss = int(self.break_elapsed) % 60
        absence_s = int(time.time() - self.absence_start) if self.absence_start else 0
        self.status_label.config(text=f"Status: {status}")
        self.timer_label.config(
            text=f"Work: {work_mm:02d}:{work_ss:02d} | Break: {break_mm:02d}:{break_ss:02d} | Absence: {absence_s}s"
        )

        self.detect_window.after(30, self.capture_loop)


    def work_time_reached_popup(self):
        res = messagebox.askyesno(
            "Waktunya Istirahat",
            f"Waktu kerja sudah mencapai {self.work_limit_s/60:.1f} menit.\nMulai istirahat sekarang?"
        )
        if res:
            self.in_break = True
            self.break_elapsed = 0.0
            self.absence_start = None
            self.status_label.config(text="Istirahat dimulai (oleh pengguna)")
        else:
            self.work_elapsed = max(0.0, self.work_elapsed - 5 * 60)
            self.notified = False
            self.status_label.config(text="Ditunda 5 menit (snooze)")

    def finish_break_and_return(self):
        self.running = False
        try:
            if self.cap and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass
        try:
            if self.detect_window:
                self.detect_window.destroy()
        except Exception:
            pass
        self.detect_window = None
        self.cap = None
        messagebox.showinfo("Istirahat Selesai", "Waktu istirahat telah selesai. Kembali ke halaman konfigurasi.")
        self.work_elapsed = 0.0
        self.break_elapsed = 0.0
        self.absence_start = None
        self.in_break = False
        self.notified = False

    def stop_and_close_detection(self):
        self.running = False
        try:
            if self.cap and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass
        try:
            if self.detect_window:
                self.detect_window.destroy()
        except Exception:
            pass
        self.detect_window = None
        self.cap = None
        self.work_elapsed = 0.0
        self.break_elapsed = 0.0
        self.absence_start = None
        self.in_break = False
        self.notified = False

# --------------------
# Run app
# --------------------
def main():
    root = tk.Tk()
    app = MicrobreakApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
