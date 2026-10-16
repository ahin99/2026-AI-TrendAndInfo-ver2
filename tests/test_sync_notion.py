import importlib.util
import os
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_notion.py"
spec = importlib.util.spec_from_file_location("sync_notion", SCRIPT)
sync = importlib.util.module_from_spec(spec)
with patch.dict(os.environ, {
    "NOTION_TOKEN": "test-token",
    "NOTION_DATA_SOURCE_ID": "test-source",
    "NOTION_CREATED_DATE_PROPERTY": "생성일",
    "NOTION_TIMEZONE": "Asia/Seoul",
}):
    spec.loader.exec_module(sync)


def make_page(start, page_id="12345678-1234-1234-1234-123456789abc"):
    return {
        "id": page_id,
        "created_time": "2026-09-01T00:00:00.000Z",
        "properties": {
            "이름": {"type": "title", "title": [{"plain_text": "테스트 글"}]},
            "생성일": {"type": "date", "date": {"start": start}},
            "세션": {"type": "select", "select": {"name": "세션01"}},
        },
    }


class WeekGroupingTests(unittest.TestCase):
    def test_week_boundaries(self):
        for value, expected in [
            ("2026-10-12", ("2026-10-12", "2026-10-18")),
            ("2026-10-18", ("2026-10-12", "2026-10-18")),
            ("2026-10-19", ("2026-10-19", "2026-10-25")),
            ("2026-11-01", ("2026-10-26", "2026-11-01")),
            ("2027-01-01", ("2026-12-28", "2027-01-03")),
            ("2028-02-29", ("2028-02-28", "2028-03-05")),
        ]:
            with self.subTest(value=value):
                bounds = sync.get_week_bounds(sync.get_created_date(make_page(value)))
                self.assertEqual(tuple(day.isoformat() for day in bounds), expected)

    def test_timestamp_uses_korean_date(self):
        for value, expected in [
            ("2026-10-18T14:59:59Z", date(2026, 10, 18)),
            ("2026-10-18T15:00:00Z", date(2026, 10, 19)),
            ("2026-10-19T00:00:00+09:00", date(2026, 10, 19)),
        ]:
            with self.subTest(value=value):
                self.assertEqual(sync.get_created_date(make_page(value)), expected)

    def test_named_timezone_and_date_range_start(self):
        page = make_page("2026-10-18T08:00:00")
        page["properties"]["생성일"]["date"].update({
            "end": "2026-10-25T08:00:00",
            "time_zone": "America/Los_Angeles",
        })
        self.assertEqual(sync.get_created_date(page), date(2026, 10, 19))

    def test_created_time_property(self):
        page = make_page(None)
        page["properties"]["생성일"] = {
            "type": "created_time", "created_time": "2026-10-18T15:00:00Z",
        }
        self.assertEqual(sync.get_created_date(page), date(2026, 10, 19))

    def test_missing_or_empty_property_falls_back_to_page_creation(self):
        for properties in [{}, {"생성일": {"type": "date", "date": None}}]:
            with self.subTest(properties=properties):
                page = make_page(None)
                page["properties"] = properties
                page["created_time"] = "2026-10-18T15:00:00Z"
                self.assertEqual(sync.get_created_date(page), date(2026, 10, 19))

    def test_sync_replaces_old_folders_and_is_repeatable(self):
        pages = [
            make_page("2026-10-12", "11111111-1234-1234-1234-123456789abc"),
            make_page("2026-10-18", "22222222-1234-1234-1234-123456789abc"),
            make_page("2026-10-19", "33333333-1234-1234-1234-123456789abc"),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "notion-posts"
            old = output / "세션01" / "old.md"
            old.parent.mkdir(parents=True)
            old.write_text("old", encoding="utf-8")
            with patch.object(sync, "OUTPUT_DIR", output), \
                    patch.object(sync, "query_all_pages", return_value=pages), \
                    patch.object(sync, "retrieve_markdown", return_value="본문\n"):
                sync.main()
                self.assertFalse(old.parent.exists())
                self.assertEqual(len(list((output / "2026-10-12_2026-10-18").glob("*.md"))), 2)
                self.assertEqual(len(list((output / "2026-10-19_2026-10-25").glob("*.md"))), 1)
                before = {p.relative_to(output): p.read_text() for p in output.rglob("*.md")}
                for content in before.values():
                    self.assertNotIn("session:", content)
                    self.assertIn("created_date:", content)
                    self.assertIn("week_start:", content)
                    self.assertIn("week_end:", content)
                    self.assertTrue(content.endswith("본문\n"))
                sync.main()
                self.assertEqual(before, {
                    p.relative_to(output): p.read_text() for p in output.rglob("*.md")
                })
                pages[2]["properties"]["생성일"]["date"]["start"] = "2026-10-18"
                sync.main()
                self.assertFalse((output / "2026-10-19_2026-10-25").exists())
                self.assertEqual(len(list(output.rglob("*.md"))), 3)

    def test_invalid_date_stops_before_deleting_existing_files(self):
        pages = [make_page("not-a-date"), make_page("2026-10-12")]
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp)
            existing = output / "existing.md"
            existing.write_text("keep", encoding="utf-8")
            with patch.object(sync, "OUTPUT_DIR", output), \
                    patch.object(sync, "query_all_pages", return_value=pages):
                with self.assertRaisesRegex(ValueError, "invalid creation date"):
                    sync.main()
            self.assertEqual(existing.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
