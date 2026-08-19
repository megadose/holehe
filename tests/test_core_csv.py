import csv
import os
import unittest
from types import SimpleNamespace
from unittest import mock

from holehe.core import export_csv


class ExportCsvTests(unittest.TestCase):
    def test_csv_includes_fields_from_later_error_rows(self):
        rows = [
            {
                "name": "example",
                "domain": "example.com",
                "rateLimit": False,
                "exists": True,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None,
            },
            {
                "name": "broken",
                "domain": "broken.example",
                "rateLimit": False,
                "error": True,
                "exists": False,
                "emailrecovery": None,
                "phoneNumber": None,
                "others": None,
            },
        ]
        args = SimpleNamespace(csvoutput=True)

        with mock.patch("holehe.core.exit") as exit_mock:
            export_csv(rows, args, "user@example.com")
            try:
                exit_mock.assert_called_once()
                output_name = exit_mock.call_args.args[0].split()[-1]
                self.assertTrue(output_name.endswith("user@example.com_results.csv"))
                with open(output_name, encoding="utf8", newline="") as output_file:
                    reader = csv.DictReader(output_file)
                    self.assertIn("error", reader.fieldnames)
                    self.assertEqual(len(list(reader)), 2)
            finally:
                if "output_name" in locals():
                    os.remove(output_name)



if __name__ == "__main__":
    unittest.main()
