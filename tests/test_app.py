import pytest

from stokku.cli import main
from stokku.models import Item
from stokku.report import format_laporan, stok_menipis, total_nilai_stok
from stokku.service import StokService
from stokku.storage import JsonStorage
from stokku.validators import (
    ValidationError,
    validate_harga,
    validate_jumlah,
    validate_nama,
    validate_sku,
)


@pytest.fixture
def service(tmp_path):
    return StokService(JsonStorage(str(tmp_path / "stok.json")))


def test_model_roundtrip():
    i = Item("A-1", "Pena", 10, 2500)
    assert Item.from_dict(i.to_dict()) == i
    assert i.total_nilai() == 25000


def test_validators():
    assert validate_sku(" abc-1 ") == "ABC-1"
    assert validate_nama(" Buku ") == "Buku"
    assert validate_jumlah(0) == 0
    assert validate_harga(10) == 10.0
    for fn, val in [(validate_sku, "!!"), (validate_nama, ""), (validate_jumlah, -1), (validate_harga, -5)]:
        with pytest.raises(ValidationError):
            fn(val)


def test_tambah_ubah_hapus(service):
    service.tambah("pen-01", "Pena", 10, 2500)
    with pytest.raises(ValidationError):
        service.tambah("PEN-01", "Pena", 1, 1)
    assert service.ubah_jumlah("PEN-01", -4).jumlah == 6
    with pytest.raises(ValidationError):
        service.ubah_jumlah("PEN-01", -100)
    service.hapus("PEN-01")
    assert service.daftar() == []
    with pytest.raises(ValidationError):
        service.hapus("PEN-01")
    with pytest.raises(ValidationError):
        service.ubah_jumlah("NOPE", 1)


def test_persistensi(tmp_path):
    path = str(tmp_path / "s.json")
    StokService(JsonStorage(path)).tambah("BK-01", "Buku", 3, 10000)
    assert StokService(JsonStorage(path)).cari("BK-01").nama == "Buku"


def test_report():
    items = [Item("A-1", "Pena", 2, 1000), Item("B-2", "Buku", 50, 2000)]
    assert total_nilai_stok(items) == 102000
    assert [i.sku for i in stok_menipis(items)] == ["A-1"]
    assert "Total nilai stok" in format_laporan(items)


def test_cli(tmp_path, capsys):
    d = str(tmp_path / "c.json")
    assert main(["--data", d, "tambah", "PN-01", "Pensil", "3", "1500"]) == 0
    assert main(["--data", d, "ubah", "PN-01", "5"]) == 0
    assert main(["--data", d, "daftar"]) == 0
    assert main(["--data", d, "menipis"]) == 0
    assert main(["--data", d, "hapus", "PN-01"]) == 0
    assert main(["--data", d, "hapus", "PN-01"]) == 1
    assert "Error" in capsys.readouterr().err