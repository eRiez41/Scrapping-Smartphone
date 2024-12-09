import csv
import os

# Fungsi untuk memeriksa apakah ada kolom dengan nilai "unknown" atau "Harga tidak tersedia"
def is_valid_row(row):
    # Periksa apakah ada kolom dengan nilai "unknown" atau "Harga tidak tersedia"
    has_unknown = any(value == "unknown" for value in row.values())
    has_unavailable_price = any(value == "Harga tidak tersedia" for value in row.values())

    # Jika ada nilai "unknown" atau "Harga tidak tersedia", baris tidak valid
    if has_unknown or has_unavailable_price:
        return False, has_unknown, has_unavailable_price
    return True, False, False

# Pastikan folder Csv ada, jika tidak buat folder tersebut
if not os.path.exists('Csv'):
    os.makedirs('Csv')

# Baca file CSV lama, filter data, dan simpan hasilnya di file yang sama
input_file_path = 'Csv/list_spek.csv'
output_file_path = 'Csv/list_spek.csv'

with open(input_file_path, mode='r', newline='', encoding='utf-8') as input_file:
    reader = csv.DictReader(input_file, delimiter='|')
    valid_rows = []
    invalid_rows = []

    # Periksa setiap baris apakah valid dan simpan alasan dihapus jika tidak valid
    for row in reader:
        is_valid, has_unknown, has_unavailable_price = is_valid_row(row)
        if is_valid:
            valid_rows.append(row)
        else:
            invalid_rows.append((row, has_unknown, has_unavailable_price))

    # Tulis data yang valid kembali ke file CSV
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames, delimiter='|', quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(valid_rows)

    # Log baris yang dihapus dengan alasan
    if invalid_rows:
        print("Baris dengan nilai 'unknown' atau 'Harga tidak tersedia' telah dihapus:")
        for row, has_unknown, has_unavailable_price in invalid_rows:
            reasons = []
            if has_unknown:
                reasons.append("mengandung 'unknown'")
            if has_unavailable_price:
                reasons.append("mengandung 'Harga tidak tersedia'")
            reason_str = " dan ".join(reasons)
            print(f"Data HP: {row['Nama Produk']} - Harga: {row['Harga']} ({reason_str})")
    else:
        print("Tidak ada baris yang dihapus. Semua data valid.")
