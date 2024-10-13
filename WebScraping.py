from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv  # CSV yazmak için eklenmiştir

def linkedin_scraper(email, password, profile_url):
    # Chrome seçeneklerini ayarla
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Tarayıcıyı tam ekran modunda başlat

    service = Service(r'C:\Users\Ahmet Koca\OneDrive\Masaüstü\chromedriver\chromedriver.exe')
    driver = webdriver.Chrome(service=service, options=options)

    file_name = ""  # Dosya adı için değişkeni başlat

    try:
        driver.get("https://www.linkedin.com/login")

        # Giriş yap
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        email_input.send_keys(email)
        password_input = driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # Giriş sayfasından yönlendirme bekle
        WebDriverWait(driver, 10).until(EC.url_changes("https://www.linkedin.com/login"))

        # Profil URL'sine git
        driver.get(profile_url)

        # Profil öğelerinin yüklenmesini bekle ve verileri çek
        name = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge"))
        ).text

        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-body-medium"))
        ).text

        location = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.text-body-small.inline.t-black--light"))
        ).text

        # Çekilen verileri yazdır
        print("Ad:", name)
        print("Başlık:", title)
        print("Konum:", location)

        # CSV dosyasına yazma (dosya adı kişinin adı olacak)
        file_name = f"{name.replace(' ', '_')}_linkedin_profile_data.csv"  # Boşlukları alt çizgiyle değiştir
        with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Ad', 'Başlık', 'Konum']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow({'Ad': name, 'Başlık': title, 'Konum': location})

        print(f"Veri başarıyla {file_name} dosyasına kaydedildi.")

    except Exception as e:
        print("Veri çekme sırasında hata:", e)
    
    finally:
        driver.quit()

    return file_name  # Dosya adını döndür

def print_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print("Ad:", row['Ad'])
                print("Başlık:", row['Başlık'])
                print("Konum:", row['Konum'])
                print("-------------------")  # Her kayıt arasına bir ayırıcı ekleyin
    except Exception as e:
        print("CSV dosyasını okuma sırasında hata:", e)

# Kullanıcı bilgileri ve profil URL'si
email = os.getenv("LINKEDIN_EMAIL", "kocaa5356@gmail.com")  # E-posta ortam değişkeni olarak ayarlanmış olmalı
password = os.getenv("LINKEDIN_PASSWORD", "243a243a243")  # Şifre ortam değişkeni olarak ayarlanmış olmalı
profile_url = "https://www.linkedin.com/in/ahmetkocaa/"  # Profil URL'si

file_name = linkedin_scraper(email, password, profile_url)  # Dosya adını al

# CSV dosyasını yazdır
print_csv(file_name)
