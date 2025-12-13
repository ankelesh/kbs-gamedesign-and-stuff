#!/usr/bin/env python3
"""
Convert all .docx files to .md (Markdown) format in the current directory and subdirectories.
Skips temporary Word files (starting with ~$).
"""

import os
import sys
from pathlib import Path

try:
    import pypandoc
except ImportError:
    print("Error: pypandoc is not installed.")
    print("Please install it with: pip install pypandoc")
    sys.exit(1)

# Ensure pandoc is installed
try:
    pypandoc.get_pandoc_version()
except OSError:
    print("Pandoc not found. Downloading pandoc...")
    try:
        pypandoc.download_pandoc()
        print("Pandoc downloaded successfully!")
    except Exception as e:
        print(f"Error downloading pandoc: {e}")
        print("Please install pandoc manually from https://pandoc.org/installing.html")
        sys.exit(1)


def convert_docx_to_md(docx_path, md_path):
    """Convert a single .docx file to .md format."""
    try:
        # Use pypandoc to convert
        output = pypandoc.convert_file(
            str(docx_path),
            'md',
            format='docx',
            outputfile=str(md_path),
            extra_args=['--wrap=none']  # Disable line wrapping
        )
        return True
    except Exception as e:
        print(f"Error converting {docx_path}: {e}")
        return False


def main():
    # Get the directory where the script is located
    base_dir = Path(__file__).parent

    # Find all .docx files
    docx_files = list(base_dir.rglob("*.docx"))

    # Filter out temporary files (starting with ~$)
    docx_files = [f for f in docx_files if not f.name.startswith("~$")]

    print(f"Found {len(docx_files)} .docx files to convert\n")

    converted = 0
    failed = 0

    for docx_file in docx_files:
        # Create corresponding .md filename
        md_file = docx_file.with_suffix('.md')

        # Show progress
        rel_path = docx_file.relative_to(base_dir)
        print(f"Converting: {rel_path}")

        # Convert
        if convert_docx_to_md(docx_file, md_file):
            converted += 1
            print(f"  [OK] Created: {md_file.relative_to(base_dir)}")
        else:
            failed += 1
            print(f"  [FAIL] Conversion failed")

        print()

    # Summary
    print("=" * 60)
    print(f"Conversion complete!")
    print(f"Successfully converted: {converted}")
    print(f"Failed: {failed}")
    print(f"Total: {len(docx_files)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
