"""Pembuatan ringkasan laporan stok."""
from typing import List

from .models import Item


def total_nilai_stok(items: List[Item]) -> float:
    return sum(i.total_nilai() for i in items)


def stok_menipis(items: List[Item], batas: int = 5) -> List[Item]:
    return [i for i in items if i.jumlah <= batas]


def format_laporan(items: List[Item]) -> str:
    baris = [f"{'SKU':<12}{'Nama':<25}{'Jumlah':>8}{'Harga':>12}"]
    for i in items:
        baris.append(f"{i.sku:<12}{i.nama:<25}{i.jumlah:>8}{i.harga:>12,.0f}")
    baris.append(f"Total nilai stok: Rp{total_nilai_stok(items):,.0f}")
    return "\n".join(baris)