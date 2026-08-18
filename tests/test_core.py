import argparse
from contextlib import redirect_stdout
import io
from os import terminal_size
import unittest
from unittest.mock import patch

from holehe import core


class TestPrintResult(unittest.TestCase):
    def test_clearing_results_preserves_terminal_history(self):
        args = argparse.Namespace(
            noclear=False,
            nocolor=True,
            onlyused=False,
        )
        output = io.StringIO()

        with patch.object(
            core,
            "get_terminal_size",
            return_value=terminal_size((80, 24)),
        ), redirect_stdout(output):
            core.print_result([], args, "user@example.com", 0, [])

        self.assertTrue(
            output.getvalue().startswith("\n" * 24 + "\033[H"),
            "The existing screen should scroll into the terminal history "
            "before the viewport is cleared.",
        )
        self.assertNotIn("\033[3J", output.getvalue())


if __name__ == "__main__":
    unittest.main()
