# StokKu - Manajemen Stok Barang (DevSecOps Pipeline)

![DevSecOps Pipeline](https://github.com/rizkyardiansyah123/devsecops-p5-0110225087/actions/workflows/devsecops.yml/badge.svg)

## 1. Nama Aplikasi dan Fungsi
**StokKu** adalah aplikasi command line untuk mengelola stok barang: menambah barang, mengubah jumlah stok, menghapus barang, menampilkan laporan stok beserta total nilainya, dan menampilkan barang yang stoknya menipis. Data disimpan dalam berkas JSON.

## 2. Bahasa dan Framework
- Python 3.12 (hanya pustaka standar untuk aplikasi)
- pytest dan pytest-cov untuk unit test dan coverage
- Bandit sebagai SAST tool

Struktur kode: `models.py`, `validators.py`, `storage.py`, `service.py`, `report.py`, `cli.py` (dalam `src/stokku/`), serta test di `tests/`.

## 3. Cara Menjalankan
```bash
git clone https://github.com/rizkyardiansyah123/devsecops-p5-0110225087.git
cd devsecops-p5-0110225087
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export PYTHONPATH=src                                # Windows PowerShell: $env:PYTHONPATH="src"
python -m stokku tambah PEN-01 "Pulpen Hitam" 20 3500
python -m stokku ubah PEN-01 -5
python -m stokku daftar
python -m stokku menipis
python -m stokku hapus PEN-01

pytest --cov=src/stokku                              # menjalankan unit test
```

## 4. Overview Pipeline CI/CD
Workflow: `.github/workflows/devsecops.yml`, berjalan pada **push** dan **pull_request** ke branch `main` di runner `ubuntu-latest`.

| Job | Fungsi |
|-----|--------|
| `build` | Checkout, setup Python, install dependencies, jalankan unit test. **Quality Gate 1:** coverage minimal 80%. |
| `sast-scan` (`needs: build`) | Menjalankan Bandit pada `src/`, mengunggah laporan JSON sebagai artifact. **Quality Gate 2:** job gagal jika ada temuan severity MEDIUM atau HIGH. |

Jika salah satu gate gagal, pipeline berstatus merah sehingga kode tidak lolos ke tahap berikutnya.