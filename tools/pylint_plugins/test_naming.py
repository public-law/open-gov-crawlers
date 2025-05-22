# tools/pylint_plugins/test_naming.py
"""Pylint plugin to enforce test file naming conventions."""

from astroid.nodes import Module
from pathlib import Path
from pylint.checkers import BaseChecker
from pylint.lint import PyLinter
from pylint.typing import MessageDefinitionTuple


class TestNamingChecker(BaseChecker):
    """Checker for test file naming conventions."""

    name = "test-naming"
    msgs: dict[str, MessageDefinitionTuple] = {
        "W9001": (
            "Test file does not follow naming convention *_test.py",
            "invalid-test-filename",
            "Test files should end with _test.py",
        ),
    }

    def process_module(self, node: Module) -> None:
        """Process a module and check if it follows test naming conventions."""
        file_path = Path(str(node.file))

        # Check if this is a test file (either in tests/ directory or has 'test' in name)
        is_in_tests = "tests" in str(file_path.parts)
        has_test_in_name = "test" in file_path.name.lower()

        if (is_in_tests or has_test_in_name) and not file_path.name.endswith("_test.py"):
            self.add_message("W9001", line=1)


def register(linter: PyLinter) -> None:
    """Register the checker with pylint."""
    linter.register_checker(TestNamingChecker(linter))
