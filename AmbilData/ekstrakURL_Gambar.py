import csv
import re
import os

# Fungsi untuk mengekstrak nama seri dari nama produk
def extract_series(product_name):
    # Menggunakan regex untuk menghapus informasi RAM, ROM, dan kapasitas penyimpanan
    cleaned_name = re.sub(r'\s*RAM\s*\d+GB|\s*ROM\s*\d+GB|\s*\d+GB|\s*\d+TB|\s*RAM|\s*ROM', '', product_name, flags=re.IGNORECASE)
    cleaned_name = re.sub(r'\s+', ' ', cleaned_name).strip()  # Menghapus spasi berlebih
    return cleaned_name

# Pastikan folder Csv ada, jika tidak buat folder tersebut
if not os.path.exists('Csv'):
    os.makedirs('Csv')

# Baca data dari list_link_hp.csv di folder Csv
input_file_path = 'Csv/list_link_hp.csv'
output_file_path = 'Csv/url_gambar.csv'

with open(input_file_path, 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    unique_series = {}  # Untuk menyimpan hasil unik

    for row in reader:
        brand = row['Brand']
        product_name = row['Product Name']
        image_url = row['Image URL']
        year = row['Year']

        # Ekstrak seri dari nama produk
        series = extract_series(product_name)

        # Gabungkan brand dan seri untuk keunikan
        key = (brand, series)

        # Simpan hanya jika kombinasi brand dan seri unik
        if key not in unique_series:
            unique_series[key] = {
                "Brand": brand,
                "Series": series,
                "Image URL": image_url,
                "Year": year
            }

# Siapkan file CSV untuk menyimpan hasil ekstraksi
with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)  # Mengaktifkan kutipan untuk semua nilai
    writer.writerow(["Brand", "Product Name", "Image URL", "Year"])  # Header CSV

    # Tulis setiap kombinasi brand dan seri unik ke file CSV
    for item in unique_series.values():
        writer.writerow([item["Brand"], item["Series"], item["Image URL"], item["Year"]])

print("Ekstraksi selesai, hasil disimpan di 'Csv/url_gambar.csv'")
