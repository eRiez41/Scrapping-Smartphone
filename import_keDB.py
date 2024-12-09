import pandas as pd
from sqlalchemy import create_engine, text

# Konfigurasi koneksi database
DATABASE_TYPE = 'mysql'
DBAPI = 'pymysql'  # Menggunakan pymysql sebagai driver
ENDPOINT = 'localhost'  # Biasanya localhost jika menggunakan XAMPP
USER = 'root'  # Username default untuk XAMPP
PASSWORD = ''  # Password default untuk XAMPP biasanya kosong
DATABASE = 'produk_hp'  # Nama database

# Membuat koneksi ke database
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}/{DATABASE}")

# Nama tabel
table_name = 'spek_hp'

# Membaca file CSV
csv_file_path = 'Csv/list_spek.csv'  # Pastikan path sesuai

# Fungsi untuk menghapus tabel jika sudah ada
def drop_table_if_exists(engine, table_name):
    with engine.connect() as connection:
        # Menggunakan SQL untuk menghapus tabel jika ada
        connection.execute(text(f"DROP TABLE IF EXISTS {table_name}"))

# Menghapus tabel jika sudah ada
drop_table_if_exists(engine, table_name)

# Menyimpan data ke tabel 'spek_hp'
try:
    # Menyesuaikan separator
    df = pd.read_csv(csv_file_path, sep='|', on_bad_lines='skip', engine='python')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)
    print("Data telah berhasil diimpor ke dalam tabel 'spek_hp' di database 'produk_hp'.")
except pd.errors.ParserError as e:
    print(f"Terjadi error saat membaca file CSV: {e}")
except Exception as e:
    print(f"Terjadi error: {e}")
