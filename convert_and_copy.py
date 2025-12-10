#!/usr/bin/env python3
import os
import shutil
import mammoth
from pathlib import Path

# Source and destination directories
source_dir = Path(".")
dest_dir = Path("../kbs_copy")

# Create destination directory if it doesn't exist
dest_dir.mkdir(exist_ok=True)

def convert_docx_to_markdown(docx_path, md_path):
    """Convert a docx file to markdown format"""
    try:
        with open(docx_path, "rb") as docx_file:
            result = mammoth.convert_to_markdown(docx_file)
            markdown = result.value

            # Write markdown to file
            md_path.parent.mkdir(parents=True, exist_ok=True)
            with open(md_path, "w", encoding="utf-8") as md_file:
                md_file.write(markdown)

            print(f"Converted: {docx_path} -> {md_path}")

            if result.messages:
                for message in result.messages:
                    print(f"  Warning: {message}")
    except Exception as e:
        print(f"Error converting {docx_path}: {e}")

def copy_file(source_path, dest_path):
    """Copy a file preserving directory structure"""
    try:
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, dest_path)
        print(f"Copied: {source_path} -> {dest_path}")
    except Exception as e:
        print(f"Error copying {source_path}: {e}")

# Process all files
for root, dirs, files in os.walk(source_dir):
    # Skip .git directory
    if '.git' in root:
        continue

    for file in files:
        source_path = Path(root) / file

        # Calculate relative path from source directory
        try:
            relative_path = source_path.relative_to(source_dir)
        except ValueError:
            continue

        if file.endswith('.docx'):
            # Skip temporary Word files (starting with ~$)
            if file.startswith('~$'):
                print(f"Skipping temporary file: {source_path}")
                continue

            # Convert docx to markdown
            md_relative_path = relative_path.with_suffix('.md')
            dest_path = dest_dir / md_relative_path
            convert_docx_to_markdown(source_path, dest_path)
        else:
            # Copy non-docx files as is
            dest_path = dest_dir / relative_path
            copy_file(source_path, dest_path)

print("\nConversion and copying completed!")
