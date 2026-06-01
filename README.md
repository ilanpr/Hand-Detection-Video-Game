# Sword Slash Hunter
# Identitas Pengembang

Nama: Ilan Hawwari Prasojo
NRP: 5025241039

## Deskripsi Proyek

Sword Slash Hunter adalah game berbasis Computer Vision yang dikembangkan menggunakan Python dan OpenCV. Pemain menggunakan gerakan tangan yang terdeteksi oleh webcam sebagai pengendali pedang untuk menghancurkan musuh yang jatuh dari atas layar.

Game ini memanfaatkan teknik deteksi warna kulit (skin detection) pada ruang warna HSV untuk melacak posisi tangan pemain secara real-time. Posisi tangan kemudian digunakan untuk mengendalikan pedang virtual yang dapat digunakan untuk menyerang musuh.

---

## Fitur Utama

### 1. Menu Interaktif

* Level 1 (Easy)
* Level 2 (Medium)
* Level 3 (Hard)
* Exit Game

### 2. Kontrol Menggunakan Tangan

* Menggunakan webcam sebagai input utama.
* Deteksi tangan dilakukan menggunakan segmentasi warna kulit.
* Posisi telapak tangan digunakan untuk menentukan posisi pedang.

### 3. Sistem Pedang

* Pedang mengikuti posisi tangan pemain.
* Efek tebasan muncul saat tangan bergerak cepat.
* Collision detection antara pedang dan musuh.

### 4. Sistem Musuh

* Musuh muncul dari bagian atas layar.
* Kecepatan musuh bergantung pada level yang dipilih.
* Menggunakan sprite PNG transparan dengan animasi frame.

### 5. Sistem Skor

* Skor bertambah setiap kali musuh berhasil dihancurkan.

### 6. Sistem Nyawa

* Pemain memiliki 3 nyawa.
* Nyawa berkurang jika musuh berhasil melewati layar.
* Game Over ketika nyawa habis.

### 7. Audio

* Background music diputar selama permainan berlangsung.

---

## Teknologi yang Digunakan

* Python 3.x
* OpenCV
* NumPy
* Pillow (PIL)
* Winsound (Windows)

---

## Konsep Computer Vision yang Digunakan

### 1. Skin Detection

Deteksi tangan dilakukan menggunakan ruang warna HSV.

```python
lower_skin = np.array([0, 40, 60])
upper_skin = np.array([18, 170, 255])
```

### 2. Morphological Operation

Menggunakan:

* Erosion
* Dilation

untuk mengurangi noise pada hasil segmentasi kulit.

### 3. Contour Detection

Kontur terbesar dianggap sebagai objek tangan pemain.

### 4. Distance Transform

Digunakan untuk mencari pusat telapak tangan yang nantinya menjadi acuan posisi pedang.

### 5. Collision Detection

Pengecekan tabrakan dilakukan dengan membandingkan posisi musuh terhadap bounding box pedang.

---

## Struktur Folder

```text
ProjectPCV/
│
├── ProjectPCV.py
│
├── Assets/
│   ├── title_banner.png
│   ├── btn_lvl1.png
│   ├── btn_lvl2.png
│   ├── btn_lvl3.png
│   ├── btn_exit.png
│   ├── sword.png
│   ├── enemy.png
│   ├── heart.png
│   ├── score_bg.png
│   ├── health_bg.png
│   ├── playing_bg.jpg
│   ├── gameover_bg.jpg
│   ├── menu_vid.mp4
│   ├── backsound.wav
│   └── aAsianNinja.ttf
│
├── screenshots/
│   ├── menu.png
│   ├── gameplay.png
│   └── gameover.png
│
└── README.md
```

---

## Cara Menjalankan Program

### 1. Install Dependencies

```bash
pip install opencv-python
pip install numpy
pip install pillow
```

### 2. Pastikan Webcam Aktif

Program menggunakan webcam default:

```python
cap = cv2.VideoCapture(0)
```

### 3. Jalankan Program

```bash
python ProjectPCV.py
```

---

## Cara Bermain

1. Jalankan program.
2. Pilih tingkat kesulitan.
3. Letakkan tangan pada area deteksi.
4. Gerakkan tangan untuk mengendalikan pedang.
5. Hancurkan musuh yang jatuh.
6. Kumpulkan skor sebanyak mungkin.
7. Hindari membiarkan musuh melewati layar.

---

## Screenshot Game

### Menu Utama

Gambar:

```text
<img width="807" height="644" alt="image" src="https://github.com/user-attachments/assets/9bd149df-4ff0-4bc0-8776-ddebe009b7f3" />

```

### Gameplay

Gambar:

```text
screenshots/gameplay.png
```

### Game Over

Gambar:

```text
screenshots/gameover.png
```

---

## Video Demonstrasi

Link Video:

```text
https://youtu.be/
```

---

