"""Model data untuk aplikasi StokKu."""
from dataclasses import dataclass, asdict


@dataclass
class Item:
    sku: str
    nama: str
    jumlah: int
    harga: float

    def total_nilai(self) -> float:
        """Nilai total stok untuk item ini (jumlah x harga)."""
        return self.jumlah * self.harga

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Item":
        return cls(
            sku=data["sku"],
            nama=data["nama"],
            jumlah=int(data["jumlah"]),
            harga=float(data["harga"]),
        )