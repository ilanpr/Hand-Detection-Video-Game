# Sword Slash Hunter

**Sword Slash Hunter** adalah game berbasis *Computer Vision* yang dikembangkan menggunakan Python dan OpenCV. Pemain menggunakan gerakan tangan yang terdeteksi oleh webcam sebagai pengendali pedang untuk menghancurkan musuh yang jatuh dari atas layar. 

Game ini memanfaatkan teknik deteksi warna kulit (*skin detection*) pada ruang warna HSV untuk melacak posisi tangan pemain secara *real-time*. Posisi tangan kemudian digunakan untuk mengendalikan pedang virtual yang dapat digunakan untuk menebas musuh.

---

## Identitas Pengembang
- **Nama:** Ilan Hawwari Prasojo
- **NRP:** 5025241039

---

## 📸 Cuplikan Permainan (Screenshots) & Video

### Menu Utama
![Main Menu](https://github.com/user-attachments/assets/9bd149df-4ff0-4bc0-8776-ddebe009b7f3)

### Gameplay
![Gameplay](<img width="1233" height="678" alt="image" src="https://github.com/user-attachments/assets/8434f8d9-12a4-408c-8876-72f81397610e" />
)

### Game Over
![Game Over](<img width="801" height="636" alt="image" src="https://github.com/user-attachments/assets/6c7c40a5-86e8-421e-81d1-62c9dd80569b" />
)

### Video Gameplay Keseluruhan
[![Video Demonstrasi Game](https://img.youtube.com/vi/ID_VIDEO_YOUTUBE/maxresdefault.jpg)](https://youtu.be/ID_VIDEO_YOUTUBE)

## Fitur Utama
1. **Menu Interaktif:** Terdapat tiga tingkat kesulitan (Level 1, Level 2, Level 3) dan tombol keluar. Kecepatan jatuh musuh bervariasi bergantung pada level yang dipilih.
2. **Kontrol Berbasis Visi (Tangan):** Menggunakan webcam sebagai input utama. Deteksi tangan dilakukan menggunakan segmentasi warna kulit. Posisi telapak tangan menjadi acuan utama pergerakan pedang.
3. **Sistem Pedang & Tebasan (Slash):** Pedang secara presisi mengikuti pergerakan tangan pemain. Terdapat fitur deteksi tebasan cepat (*slash*) yang memberikan efek teks dan poin lebih besar (+3 poin) dibandingkan serangan biasa (+1 poin).
4. **Sistem Musuh Beranimasi:** Musuh direpresentasikan dengan *sprite sheet* PNG transparan yang beranimasi (berpindah *frame*) saat jatuh dari atas layar.
5. **Sistem Skor & Nyawa (Health):** Pemain memiliki 3 nyawa. Nyawa akan berkurang jika musuh berhasil menyentuh garis batas merah di bawah layar.
6. **Audio Pendukung:** *Background music* diputar secara dinamis selama di menu, gameplay, dan saat game over (Bekerja secara native untuk sistem operasi Windows).

---

## Konsep Computer Vision yang Digunakan

### 1. Skin Detection (HSV Color Space)
Deteksi kulit/tangan dilakukan dengan melakukan thresholding pada ruang warna HSV untuk mengatasi bayangan dan pencahayaan. Rentang warna yang digunakan pada program:
Code output
File README.md has been generated.

```python
lower_skin = np.array([0, 20, 50], dtype=np.uint8) 
upper_skin = np.array([25, 200, 255], dtype=np.uint8)

```
### 2. Morphological Operations
Digunakan untuk mengurangi noise dan menyempurnakan bentuk mask hasil deteksi:

Erosion (1 iterasi) untuk menghilangkan titik-titik noise (kotoran) di latar belakang.

Dilation (3 iterasi) untuk menebalkan kembali mask area tangan yang terdeteksi sehingga lebih solid.

### 3. Contour Detection
Program (cv2.findContours) mencari garis luar dari mask tangan dan mengambil area kontur terbesar (dengan batas minimum 3000 piksel) sebagai objek tangan pemain.

### 4. Distance Transform
Digunakan cv2.distanceTransform untuk mencari titik pusat tebal (titik paling tengah) dari telapak tangan pemain. Titik ini akan diolah lebih lanjut untuk menjadi poros acuan koordinat jatuhnya pangkal pedang.

### 5. Collision Detection
Pengecekan tabrakan dilakukan dengan dua cara:

Membandingkan kordinat musuh terhadap bounding box pedang untuk mendeteksi serangan biasa.

Mengkalkulasi jarak (Euclidean Distance) dari ujung pedang sebelumnya dan ujung pedang saat ini untuk mendeteksi pergerakan super cepat (Slash Hit).

# Teknologi yang Digunakan
Python 3.

OpenCV (cv2) - Pemrosesan gambar, kamera, dan computer vision.

NumPy - Operasi matriks dan array numerik untuk thresholding.

Pillow (PIL) - Digunakan untuk me-render teks secara custom (mendukung font .ttf khusus).

Winsound - Pemutaran backsound game (Khusus Windows).

# 📂 Struktur Folder
Pastikan file-file aset (gambar, video, font, audio) berada pada satu direktori dengan program utama (Sword Slash Hunter.py):

```
ProjectPCV/
│
├── ProjectPCV.py
│
├── title_banner.png
├── btn_lvl1.png
├── btn_lvl2.png
├── btn_lvl3.png
├── btn_exit.png
├── sword.png
├── enemy.png
├── heart.png
├── score_bg.png
├── health_bg.png
├── playing_bg.jpg
├── gameover_bg.jpg
├── menu_vid.mp4
├── gameover_vid.mp4
├── backsound.wav
├── gameover_bgm.wav
└── aAsianNinja.ttf
```
# 🚀 Cara Menjalankan Program
### 1. Install Dependencies
Buka terminal atau command prompt Anda, lalu instal library Python yang dibutuhkan:

Bash
pip install opencv-python numpy pillow
### 2. Pastikan Webcam Aktif
Program ini membaca input kamera secara real-time dari default device. Pastikan webcam terhubung dan tidak sedang digunakan oleh aplikasi lain.

### 3. Jalankan Game
Eksekusi file Python tersebut:

Bash
python ProjectPCV.py
🎮 Cara Bermain
Buka dan jalankan program.

Klik level kesulitan pada layar Main Menu (Level 1, 2, atau 3).

Akan muncul beberapa window pembantu (seperti Bareface dan Skin Detection Debug) dan jendela Game utama.

Hadapkan area kulit (tangan) ke arah kamera.

Gerakkan tangan Anda, pedang virtual akan mengikutinya.

Ayunkan tangan secara cepat untuk mengenai musuh secara tebasan (Dapat bonus +3 Poin/Slash).

Hancurkan musuh yang berjatuhan sebelum melewati batas merah. Jika lolos, nyawa Anda berkurang.

Permainan berakhir saat nyawa (❤️) habis.
"""
