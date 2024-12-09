import requests
import csv
import json
import re
from datetime import datetime
import os

# Function to process a single URL
def process_url(url, price, writer, id_counter):
    # Extract the product ID from the input URL
    match = re.search(r'PD_(\d+)', url)
    if match:
        product_id = match.group(1)
    else:
        print(f"URL tidak valid: {url}")
        return

    # Construct the API URL
    api_url = f'https://portal.pricebook.co.id/new/pb/product/specification?product_id={product_id}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Gagal mengambil data dari {url}: {e}")
        return

    if data.get('success'):
        specifications = data['result'].get('specification', {}).get('categories')

        if specifications is None:
            print(f"Tidak ada spesifikasi untuk URL: {url}")
            return

        # Function to get description with error handling
        def get_description(item_name, sub_title):
            try:
                for item in specifications:
                    if item['name'] == item_name:
                        for sub in item['sub_categories']:
                            if sub['title'] == sub_title:
                                return sub.get('description', None)
            except (KeyError, IndexError):
                return None
            return None

        # Ekstraksi data menggunakan fungsi di atas
        brand = get_description('Basic Info', 'Brand')
        tahun_rilis = get_description('Basic Info', 'Tahun Rilis')
        tahun_rilis = tahun_rilis['sec'] if tahun_rilis else None
        if tahun_rilis:
            tahun_rilis = datetime.fromtimestamp(tahun_rilis).year
        else:
            tahun_rilis = "unknown"

        # Tambahkan "Android" di depan tahun jika hanya angka
        if str(tahun_rilis).isdigit():
            tahun_rilis = f"Android {tahun_rilis}"

        nama_produk = get_description('Basic Info', 'Nama Produk')
        jaringan = get_description('Network', 'Jaringan')
        material = get_description('Design', 'Material') or "unknown"
        sim_slots = get_description('Design', 'SIM Slots') or "unknown"

        # Normalisasi resolusi layar
        def normalize_screen_resolution(resolution):
            if resolution and 'x' in resolution:
                parts = resolution.split('x')
                if len(parts) == 2:
                    width, height = parts[0].strip(), parts[1].strip()
                    if int(width) < int(height):  # Pastikan lebar lebih besar dari tinggi
                        return f"{height} x {width}"
                    return f"{width} x {height}"
            return resolution

        technology = get_description('Screen', 'Technology')
        screen_size = get_description('Screen', 'Ukuran Layar')
        screen_resolution = normalize_screen_resolution(get_description('Screen', 'Screen Resolution'))

        os_version = get_description('Software', 'OS Version')
        version_detail = get_description('Software', 'Version Detail')
        if os_version and str(os_version).isdigit():
            os_version = f"Android {os_version}"
        os_info = f"{os_version}, {version_detail}"

        processor = get_description('Hardware', 'Prosesor')
        processor_detail = get_description('Hardware', 'Detail Prosesor')
        core_count = get_description('Hardware', 'Jumlah Core')

        # Bersihkan data prosesor
        def clean_processor_data(processor, detail, cores):
            if detail:
                # Hapus kode model seperti "SM7450-AB"
                detail = re.sub(r"\bSM\d+[-\w]*", "", detail).strip()
                # Ubah format "Dimensity xxxx+" menjadi "Dimensity xxxx Plus"
                detail = re.sub(r"\bDimensity (\d+)\+", r"Dimensity \1 Plus", detail)
            if cores:
                # Ubah nama jumlah core seperti "Hendeca" menjadi "Deca"
                core_mappings = {
                    "Hendeca": "Deca",
                    "Hendecacore": "Deca",
                }
                cores = core_mappings.get(cores, cores)
            return f"{processor}, {detail}, {cores}".strip(", ")

        processor_info = clean_processor_data(processor, processor_detail, core_count)

        gpu = get_description('Hardware', 'GPU')
        ram = get_description('Memory', 'RAM')
        memory_internal = get_description('Memory', 'Memori Internal')

        # Konversi RAM dan memori internal ke GB
        # Convert RAM and Internal Memory from MB to GB and format as "RAM/Internal Memory"
        def convert_to_gb(value):
            if isinstance(value, str):
                if 'MB' in value:
                    try:
                        # Extract numeric value from the string and convert to integer
                        mb_value = int(value.replace(' MB', '').strip())
                        return f"{mb_value / 1024:.0f} GB"
                    except ValueError:
                        return "-"
                elif 'GB' in value:
                    return value.strip()  # Return as is if already in GB
            elif isinstance(value, int):
                return f"{value / 1024:.0f} GB"
            return "-"

        ram = convert_to_gb(ram)
        memory_internal = convert_to_gb(memory_internal)

        nfc = get_description('Connectivity', 'NFC') or "No"
        usb = get_description('Connectivity', 'USB')
        battery_capacity = get_description('Battery', 'Kapasitas Baterai') or "unknown"
        fast_charging = get_description('Battery', 'Daya Fast Charging') or "unknown"

        if fast_charging != "-":
            fast_charging = fast_charging.replace(' W W', 'W')

        waterproof = get_description('Other Features', 'Waterproof') or "No"
        sensor = get_description('Other Features', 'Sensor') or "No"
        jack = get_description('Other Features', '3.5mm Jack') or "No"

        resolusi_kamera_belakang = get_description('Camera', 'Resolusi Kamera Belakang') or "unknown"
        resolusi_kamera_lainnya = get_description('Camera', 'Resolusi Kamera Utama Lainnya') or "unknown"
        dual_kamera_belakang = get_description('Camera', 'Dual Kamera Belakang') or "No"
        jumlah_kamera_belakang = get_description('Camera', 'Jumlah Kamera Belakang') or "unknown"
        resolusi_kamera_depan = get_description('Camera', 'Resolusi Kamera Depan') or "unknown"
        dual_kamera_depan = get_description('Camera', 'Dual Kamera Depan') or "No"
        flash = get_description('Camera', 'Flash') or "No"
        dual_flash = get_description('Camera', 'Dual Flash') or "No"
        video = get_description('Camera', 'Video') or "unknown"

        # Tulis data ke CSV dengan kolom RAM dan Memori Internal terpisah
        writer.writerow([
            id_counter, brand, tahun_rilis, nama_produk, jaringan, material, sim_slots,
            technology, screen_size, screen_resolution, os_info, processor_info,
            gpu, ram, memory_internal, nfc, usb, battery_capacity, fast_charging,
            waterproof, sensor, jack, resolusi_kamera_belakang, resolusi_kamera_lainnya,
            dual_kamera_belakang, jumlah_kamera_belakang, resolusi_kamera_depan,
            dual_kamera_depan, flash, dual_flash, video, price
        ])

        print(f"Data untuk {nama_produk} telah disimpan ke 'Csv/list_spek.csv'.")
    else:
        print(f"Gagal mendapatkan data untuk URL: {url}")

# Pastikan folder Csv ada, jika tidak buat folder tersebut
if not os.path.exists('Csv'):
    os.makedirs('Csv')

# Membuka file output dan menulis header baru
with open('Csv/list_spek.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|', quoting=csv.QUOTE_ALL)
    writer.writerow([
        "id", "Brand", "Tahun Rilis", "Nama Produk", "Jaringan", "Material", "SIM Slots",
        "Technology", "Ukuran Layar", "Screen Resolution", "OS Version & Version Detail",
        "Prosesor", "GPU", "RAM (GB)", "Memori Internal (GB)", "NFC", "USB",
        "Kapasitas Baterai", "Daya Fast Charging", "Waterproof", "Sensor", "3.5mm Jack",
        "Resolusi Kamera Belakang", "Resolusi Kamera Utama Lainnya", "Dual Kamera Belakang",
        "Jumlah Kamera Belakang", "Resolusi Kamera Depan", "Dual Kamera Depan",
        "Flash", "Dual Flash", "Video", "Harga"
    ])

    id_counter = 1
    with open('Csv/list_link_hp.csv', mode='r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            url = row['Link']
            price = row['Price']
            process_url(url, price, writer, id_counter)
            id_counter += 1
