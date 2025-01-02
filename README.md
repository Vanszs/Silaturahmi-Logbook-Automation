# Selenium Logbook Automation

Proyek ini bertujuan untuk melakukan **otomatisasi pengisian logbook** di situs tertentu (misalnya: [**silaturahmi.upnjatim.ac.id**](https://silaturahmi.upnjatim.ac.id)) dengan menggunakan **Selenium**, **Python**, dan **JSON** sebagai sumber data kegiatan.

## Daftar Isi

1. [Fitur Utama](#fitur-utama)  
2. [Prasyarat dan Instalasi](#prasyarat-dan-instalasi)  
3. [Struktur Project](#struktur-project)  
4. [Cara Kerja](#cara-kerja)  
5. [Contoh File JSON](#contoh-file-json)  
6. [Contoh Kode](#contoh-kode)  
7. [Cara Menjalankan](#cara-menjalankan)  
8. [Catatan Penting](#catatan-penting)  
9. [Lisensi](#lisensi)

---

## Fitur Utama

- **Login Otomatis**: Script akan login menggunakan kredensial yang telah ditentukan.
- **Baca Data dari JSON**: Data logbook (tanggal dan deskripsi) diambil dari file JSON yang berisi daftar kegiatan.
- **Memasukkan Satu Entri**: Script hanya mengisi satu entri logbook per eksekusi (logika lama yang diinginkan).
- **Hapus Entri yang Berhasil**: Jika sukses memasukkan satu entri, script menghapus entri tersebut dari file JSON agar tidak duplikat di eksekusi selanjutnya.
- **Penggunaan Date Picker**: Script otomatis memilih bulan, tahun, dan tanggal di date picker sesuai data JSON.
- **Mudah Dikembangkan**: Dapat disesuaikan untuk situs lain selama struktur elemen HTML-nya diketahui.

---

## Prasyarat dan Instalasi

1. **Python 3.7+**  
   Pastikan versi Python Anda minimal 3.7 atau lebih baru.

2. **Paket Python**:
   ```bash
   pip install selenium
   pip install fake-useragent
   ```
   - **selenium**: Untuk kontrol browser otomatis.  
   - **fake-useragent**: Untuk memalsukan user agent agar lebih fleksibel.

3. **WebDriver**:
   - Gunakan **ChromeDriver** (atau WebDriver lain) yang **kompatibel** dengan versi browser Anda.  
   - Pastikan **ChromeDriver** sudah ditambahkan ke PATH sistem agar pemanggilan `webdriver.Chrome()` dapat berjalan tanpa `executable_path`.

4. **File JSON**:
   - Sebuah file `logbook.json` yang memuat daftar kegiatan dalam array satu dimensi.

---

## Struktur Project

```
.
├── logbook.json
├── main.py            # File utama (script Selenium)
└── README.md          # Dokumentasi (file ini)
```

- **`logbook.json`**: Berisi data kegiatan (tanggal & deskripsi).  
- **`main.py`**: Script Python yang menjalankan proses otomatisasi.

---

## Cara Kerja

1. **Script Membaca `logbook.json`**  
   Mendapatkan array kegiatan berisi `tanggal` dan `deskripsi`.

2. **Login ke Situs**  
   Script akan login menggunakan kredensial (username & password) yang disediakan.

3. **Mengisi Form Logbook**  
   Script:
   - Memilih tanggal dari date picker berdasarkan `tanggal` di JSON.
   - Mengisi deskripsi ke textarea berdasarkan `deskripsi` di JSON.

4. **Hapus Entri Berhasil**  
   Setelah sukses menginput satu entri, script:
   - Menghapus entri tersebut dari `logbook.json`.
   - Menyimpan perubahan ke file JSON.

---

## Contoh File JSON

```json
[
    {
        "tanggal": "04 October 2024",
        "deskripsi": "Weekly Consultation 3\nTanggal: 4 October 2024\nSesi pemantauan yang membahas tugas-tugas terkini serta sesi tanya jawab mengenai konsep Python lanjutan."
    },
    {
        "tanggal": "11 October 2024",
        "deskripsi": "Weekly Consultation 4\nTanggal: 11 October 2024\nSesi review kemajuan proyek dan pembahasan strategi pembelajaran untuk mempersiapkan deadline mendatang."
    }
]
```

---

## Contoh Kode

```python
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
from datetime import datetime

# Konfigurasi
json_file = "logbook.json"
username = "22081010153"
password = "34302"

# Baca JSON
with open(json_file, "r", encoding="utf-8") as file:
    data_logbook = json.load(file)

# Inisialisasi WebDriver
ua = UserAgent()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={ua.random}")
driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://silaturahmi.upnjatim.ac.id/login")
    time.sleep(2)

    # Login
    driver.find_element(By.XPATH, '...').send_keys(username)
    driver.find_element(By.XPATH, '...').send_keys(password)
    driver.find_element(By.XPATH, '...').click()
    time.sleep(3)

    # Isi Logbook
    log = data_logbook[0]  # Ambil entri pertama
    # (Logika pengisian date picker dan deskripsi di sini)

    # Hapus entri berhasil
    data_logbook.pop(0)
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data_logbook, file, indent=4)

finally:
    driver.quit()
```

---

## Cara Menjalankan

1. Pastikan file `logbook.json` telah diisi sesuai format.  
2. Jalankan script Python:
   ```bash
   python main.py
   ```
3. Script akan otomatis:
   - Login.
   - Membaca entri pertama di JSON.
   - Memasukkan data logbook.
   - Menghapus entri yang berhasil.

---

## Catatan Penting

- **XPath Elemen**: Pastikan XPath elemen sesuai dengan struktur HTML situs yang digunakan.
- **Eksekusi Per Enti**: Script hanya memproses **satu entri** per eksekusi untuk menghindari kesalahan massal.
- **Backup JSON**: Sebaiknya backup file `logbook.json` untuk mencegah kehilangan data akibat penghapusan otomatis.

---

## Lisensi

Proyek ini menggunakan lisensi [MIT](LICENSE). Anda bebas menggunakan dan memodifikasi script ini sesuai kebutuhan.
