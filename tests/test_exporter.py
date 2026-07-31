import zipfile
from app.database import Database
from app.exporter import export_leads


def test_export_creates_valid_xlsx_archive(tmp_path):
    db = Database(tmp_path / "db.sqlite")
    output = export_leads(db, tmp_path / "leads.xlsx")
    with zipfile.ZipFile(output) as archive:
        assert "xl/workbook.xml" in archive.namelist()
        assert "意向客户" in archive.read("xl/workbook.xml").decode("utf-8")
