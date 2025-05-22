#!/usr/bin/env python3
"""Script to check test file naming conventions."""

import sys
from pathlib import Path


def is_test_file(file: Path) -> bool:
    """Determine if a file is a test file that should follow our naming convention."""
    # Ignore __init__.py files
    if file.name == "__init__.py":
        return False

    # Check if this is in the tests directory
    is_in_tests = "tests" in file.parts

    # Check if this is a test file by name (excluding utility files with 'test' in the name)
    has_test_prefix = file.name.startswith("test_")
    has_test_suffix = file.name.endswith("_test.py")

    return is_in_tests and (has_test_prefix or has_test_suffix)


def check_test_files(directory: Path) -> list[Path]:
    """Find test files that don't follow the *_test.py convention."""
    bad_files = []

    for file in directory.rglob("*.py"):
        if is_test_file(file) and not file.name.endswith("_test.py"):
            bad_files.append(file)

    return bad_files


def main() -> None:
    """Main entry point."""
    workspace = Path(__file__).parent.parent
    bad_files = check_test_files(workspace)

    if bad_files:
        print("Found test files not following the *_test.py convention:")
        for file in bad_files:
            print(f"  {file.relative_to(workspace)}")
        sys.exit(1)
    else:
        print("All test files follow the naming convention.")


if __name__ == "__main__":
    main()
