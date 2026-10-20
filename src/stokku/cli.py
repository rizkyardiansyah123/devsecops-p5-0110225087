"""Antarmuka command line StokKu."""
import argparse
import sys

from .report import format_laporan, stok_menipis
from .service import StokService
from .storage import JsonStorage
from .validators import ValidationError


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="stokku", description="Manajemen stok barang sederhana")
    p.add_argument("--data", default="stok.json", help="lokasi berkas data JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("tambah", help="tambah barang baru")
    a.add_argument("sku")
    a.add_argument("nama")
    a.add_argument("jumlah", type=int)
    a.add_argument("harga", type=float)

    u = sub.add_parser("ubah", help="tambah/kurangi jumlah stok")
    u.add_argument("sku")
    u.add_argument("delta", type=int)

    h = sub.add_parser("hapus", help="hapus barang")
    h.add_argument("sku")

    sub.add_parser("daftar", help="tampilkan laporan stok")
    sub.add_parser("menipis", help="tampilkan barang dengan stok menipis")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    service = StokService(JsonStorage(args.data))
    try:
        if args.cmd == "tambah":
            item = service.tambah(args.sku, args.nama, args.jumlah, args.harga)
            print(f"Ditambahkan: {item.sku} - {item.nama}")
        elif args.cmd == "ubah":
            item = service.ubah_jumlah(args.sku, args.delta)
            print(f"Stok {item.sku} sekarang {item.jumlah}")
        elif args.cmd == "hapus":
            service.hapus(args.sku)
            print("Barang dihapus.")
        elif args.cmd == "daftar":
            print(format_laporan(service.daftar()))
        elif args.cmd == "menipis":
            for i in stok_menipis(service.daftar()):
                print(f"{i.sku}: {i.jumlah}")
    except ValidationError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())