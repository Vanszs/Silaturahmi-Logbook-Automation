import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
import time
from datetime import datetime

# --------------------
# Konfigurasi
# --------------------
json_file = "E:\Code\silaturahmi\logbook.json"  # File JSON tunggal
username = "-"
password = "-"

# Fake UserAgent
ua = UserAgent()
user_agent = ua.random

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
session_path = "E:/Selenium"
chrome_options.add_argument(f"user-data-dir={session_path}")
chrome_options.add_argument("--log-level=3")
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument(f"user-agent={user_agent}")

# Baca data JSON (array tunggal)
with open(json_file, "r", encoding="utf-8") as file:
    data_logbook = json.load(file)  # List of { 'tanggal': ..., 'deskripsi': ... }

# Inisialisasi WebDriver
driver = webdriver.Chrome(options=chrome_options)

try:
    # 1) Login
    driver.get("https://silaturahmi.upnjatim.ac.id/login")
    time.sleep(2)

    # Isi username
    username_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div/main/div/div[3]/div[1]/div/div/div/div/div[2]/div/form/div/div/div[1]/div/div[1]/div/input')
    username_input.send_keys(username)

    # Isi password
    password_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div/main/div/div[3]/div[1]/div/div/div/div/div[2]/div/form/div/div/div[2]/div/div[1]/div[1]/input')
    password_input.send_keys(password)

    # Klik tombol login
    login_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div/main/div/div[3]/div[1]/div/div/div/div/div[2]/div/form/div/div/button')
    login_button.click()
    time.sleep(3)

    # 2) Buka halaman form log
    driver.get("https://silaturahmi.upnjatim.ac.id/magang/log-kegiatan/form/log")
    time.sleep(2)

    # 3) Proses satu entri (jika ada)
    for i in range(40):
        log = data_logbook[0]  # Ambil entri pertama
        try:
            time.sleep(1)
            tanggal_input = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/div/div/div/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div/div/div[2]/input')
            tanggal_input.click()
            time.sleep(1)

            target_date = datetime.strptime(log['tanggal'], "%d %B %Y")
            month, year, day = target_date.strftime("%B"), target_date.year, target_date.day

            while True:
                header_element = driver.find_element(By.CSS_SELECTOR, '.v-date-picker-header__value button')
                header_text = header_element.text 

                if f"{month} {year}" in header_text:
                    date_buttons = driver.find_elements(By.CSS_SELECTOR, ".v-date-picker-table button")
                    for btn in date_buttons:
                        if btn.text == str(day):
                            btn.click()
                            break
                    break
                else:
                    # Asumsi next month
                    next_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Previous month"]')
                    next_button.click()
                    time.sleep(0.5)

            # Isi deskripsi
            deskripsi_textarea = driver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/main/div/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/textarea')
            deskripsi_textarea.click()
            deskripsi_textarea.clear()
            deskripsi_textarea.send_keys(log['deskripsi'])

            # Klik tombol submit
            submit_button = driver.find_element(By.XPATH, '/html/body/div/div/div/div/main/div/div/div/div/div/div[2]/div/div/div[4]/div[2]/button[2]')
            submit_button.click()
            time.sleep(2)

            print(f"Sukses input log untuk tanggal: {log['tanggal']}")

            # Jika berhasil, hapus entri ini dari data_logbook
            data_logbook.remove(log)
            with open(json_file, "w", encoding="utf-8") as file:
                json.dump(data_logbook, file, indent=4, ensure_ascii=False)
            time.sleep(1)
            driver.get("https://silaturahmi.upnjatim.ac.id/magang/log-kegiatan/form/log")



        except Exception as e:
            print(f"Gagal input log {log['tanggal']}: {e}")

finally:
    driver.quit()
