"""Validasi input pengguna (input validation untuk mencegah data tidak valid)."""
import re

SKU_PATTERN = re.compile(r"^[A-Z0-9-]{3,20}$")


class ValidationError(ValueError):
    """Dilempar ketika input tidak memenuhi aturan validasi."""


def validate_sku(sku: str) -> str:
    sku = sku.strip().upper()
    if not SKU_PATTERN.match(sku):
        raise ValidationError("SKU harus 3-20 karakter: huruf, angka, atau tanda '-'.")
    return sku


def validate_nama(nama: str) -> str:
    nama = nama.strip()
    if not 1 <= len(nama) <= 100:
        raise ValidationError("Nama barang harus 1-100 karakter.")
    return nama


def validate_jumlah(jumlah: int) -> int:
    if not isinstance(jumlah, int) or jumlah < 0:
        raise ValidationError("Jumlah harus bilangan bulat >= 0.")
    return jumlah


def validate_harga(harga: float) -> float:
    if harga < 0:
        raise ValidationError("Harga tidak boleh negatif.")
    return float(harga)