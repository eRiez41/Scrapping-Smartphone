import csv
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

# Baca URL dari file linkMerek.txt
with open('linkMerekPricebook.txt', 'r') as file:
    urls = file.readlines()

base_url = "https://www.pricebook.co.id"

# Pastikan folder Csv ada, jika tidak buat folder tersebut
if not os.path.exists('Csv'):
    os.makedirs('Csv')

# Siapkan file CSV untuk menyimpan hasil scraping
with open('Csv/list_link_hp.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)  # Mengaktifkan kutipan untuk semua nilai
    writer.writerow(["Brand", "Product Name", "Link", "Image URL", "Price", "Year"])  # Header CSV

    for url in urls:
        url = url.strip()  # Menghapus whitespace
        print(f"Sedang mengambil data dari: {url}")  # Log proses
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Ambil brand dari URL
        parsed_url = urlparse(url)
        brand = parse_qs(parsed_url.query).get('brand', [''])[0].capitalize()

        products = soup.select('.styles_productPanel__k5Gg1')

        for product in products:
            name = product.select_one('.styles_productName__Kgflp').text.strip()
            link = base_url + product.select_one('.styles_linkReplace__sYhyt')['href']
            image = product.select_one('.styles_productImageWrapper__9keAN img')['src']

            # Cek apakah harga tersedia
            price_element = product.select_one('.styles_price__qC82W')
            price = price_element.text.strip() if price_element else 'Harga tidak tersedia'

            # Ambil tahun rilis
            year_element = product.select_one('.styles_yearReleased__dmE_C span')
            year_released = year_element.text.strip() if year_element else 'Tahun tidak tersedia'

            # Cek apakah tahun rilis adalah 2023 atau 2024
            if year_released in ['2024']:
                # Tulis ke dalam file CSV termasuk tahun rilis
                writer.writerow([brand, name, link, image, price, year_released])

print("Scraping selesai, hasil disimpan di 'Csv/list_link_hp.csv'")
