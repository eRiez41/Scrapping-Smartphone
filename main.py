import subprocess
import os

# Folder yang berisi file Python
folder_path = 'AmbilData'

# Daftar file yang akan dijalankan
files_to_run = [
    'ambilLinkHP.py',
    'ambilSpekHP.py',
    'ekstrakURL_Gambar.py',
    'filter_isiSpek.py',
]

# Fungsi untuk menjalankan file Python
def run_python_file(file_name):
    try:
        result = subprocess.run(['python3', os.path.join(folder_path, file_name)], check=True)
        print(f'{file_name} berhasil dijalankan.')
    except subprocess.CalledProcessError as e:
        print(f'Error saat menjalankan {file_name}: {e}')

# Jalankan setiap file dalam urutan
for file in files_to_run:
    run_python_file(file)
