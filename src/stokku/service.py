"""Logika bisnis manajemen stok."""
from typing import List, Optional

from .models import Item
from .storage import JsonStorage
from .validators import (
    ValidationError,
    validate_harga,
    validate_jumlah,
    validate_nama,
    validate_sku,
)


class StokService:
    def __init__(self, storage: JsonStorage):
        self.storage = storage
        self.items: List[Item] = storage.load()

    def cari(self, sku: str) -> Optional[Item]:
        sku = validate_sku(sku)
        return next((i for i in self.items if i.sku == sku), None)

    def tambah(self, sku: str, nama: str, jumlah: int, harga: float) -> Item:
        sku = validate_sku(sku)
        if self.cari(sku):
            raise ValidationError(f"SKU {sku} sudah terdaftar.")
        item = Item(sku, validate_nama(nama), validate_jumlah(jumlah), validate_harga(harga))
        self.items.append(item)
        self.storage.save(self.items)
        return item

    def ubah_jumlah(self, sku: str, delta: int) -> Item:
        item = self.cari(sku)
        if item is None:
            raise ValidationError("SKU tidak ditemukan.")
        item.jumlah = validate_jumlah(item.jumlah + delta)
        self.storage.save(self.items)
        return item

    def hapus(self, sku: str) -> None:
        item = self.cari(sku)
        if item is None:
            raise ValidationError("SKU tidak ditemukan.")
        self.items.remove(item)
        self.storage.save(self.items)

    def daftar(self) -> List[Item]:
        return sorted(self.items, key=lambda i: i.sku)