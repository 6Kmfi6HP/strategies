#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate git mv commands for renaming markdown files in trading method group B
Processes 5 directories with 552 total files
"""

import os
import re
from pathlib import Path

# Directory configurations
DIRECTORIES = {
    "16-交易方法-反转策略": r"C:\Users\liang\GitHub\strategies\16-交易方法-反转策略",
    "17-交易方法-突破策略": r"C:\Users\liang\GitHub\strategies\17-交易方法-突破策略",
    "18-交易方法-定投策略": r"C:\Users\liang\GitHub\strategies\18-交易方法-定投策略",
    "19-交易方法-形态识别": r"C:\Users\liang\GitHub\strategies\19-交易方法-形态识别",
    "20-交易方法-斐波那契": r"C:\Users\liang\GitHub\strategies\20-交易方法-斐波那契"
}

def extract_names_from_filename(filename):
    """
    Extract Chinese and English names from existing filenames.
    Handles various formats like:
    - 中文名English-Name.md
    - Chinese-Name英文名.md
    - Mixed-格式-Names.md
    """
    filename = filename.replace('.md', '')

    # Pattern 1: Already has mixed format
    # Try to split on capital letters or dashes
    parts = re.split(r'(?=[A-Z][a-z])|(?<=[a-z])(?=[A-Z])|[-_]', filename)

    chinese_parts = []
    english_parts = []

    for part in parts:
        if not part:
            continue
        # Check if contains Chinese characters
        if re.search(r'[\u4e00-\u9fff]', part):
            chinese_parts.append(part)
        elif re.search(r'[a-zA-Z]', part):
            english_parts.append(part)

    chinese_name = ''.join(chinese_parts) if chinese_parts else ''
    english_name = '-'.join(english_parts).lower() if english_parts else ''

    # Clean up
    chinese_name = re.sub(r'^[^\u4e00-\u9fff]+', '', chinese_name)
    chinese_name = re.sub(r'[^\u4e00-\u9fff]+$', '', chinese_name)
    english_name = re.sub(r'^-+|-+$', '', english_name)
    english_name = re.sub(r'-+', '-', english_name)

    return chinese_name, english_name

def process_directory(dir_name, dir_path):
    """Process a single directory and generate rename commands."""
    print(f"\n{'='*80}")
    print(f"Processing: {dir_name}")
    print(f"Path: {dir_path}")
    print(f"{'='*80}\n")

    if not os.path.exists(dir_path):
        print(f"ERROR: Directory not found: {dir_path}")
        return []

    # Get all .md files
    md_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.md')])

    if not md_files:
        print(f"WARNING: No markdown files found in {dir_path}")
        return []

    print(f"Found {len(md_files)} markdown files")

    rename_commands = []
    rename_commands.append(f"# Directory: {dir_name}")
    rename_commands.append(f"# Total files: {len(md_files)}")
    rename_commands.append(f"cd \"{dir_path}\"\n")

    for idx, old_filename in enumerate(md_files, 1):
        chinese_name, english_name = extract_names_from_filename(old_filename)

        # Generate sequence number
        seq_num = f"{idx:03d}"

        # Create new filename
        if chinese_name and english_name:
            new_filename = f"{seq_num}-{chinese_name}-{english_name}.md"
        elif chinese_name:
            new_filename = f"{seq_num}-{chinese_name}.md"
        elif english_name:
            new_filename = f"{seq_num}-{english_name}.md"
        else:
            # Fallback: use original name with sequence
            new_filename = f"{seq_num}-{old_filename}"

        # Only add command if names are different
        if old_filename != new_filename:
            rename_commands.append(f'git mv "{old_filename}" "{new_filename}"')

    return rename_commands

def main():
    """Main function to process all directories."""
    print("="*80)
    print("Trading Method Group B - File Renaming Script Generator")
    print("="*80)
    print("\nDirectories to process:")
    for dir_name, dir_path in DIRECTORIES.items():
        print(f"  - {dir_name}")
    print(f"\nTotal directories: {len(DIRECTORIES)}")

    all_commands = []
    total_files = 0

    for dir_name, dir_path in DIRECTORIES.items():
        commands = process_directory(dir_name, dir_path)
        if commands:
            all_commands.extend(commands)
            all_commands.append("")  # Add blank line between directories
            # Count files (subtract header lines)
            file_count = len([c for c in commands if c.startswith('git mv')])
            total_files += file_count

    # Write to output file
    output_file = r"C:\Users\liang\GitHub\strategies\rename_group_b.sh"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\n")
        f.write("# Trading Method Group B - Batch Rename Script\n")
        f.write(f"# Generated for 5 directories\n")
        f.write(f"# Total files to rename: {total_files}\n")
        f.write("#\n")
        f.write("# Usage: bash rename_group_b.sh\n")
        f.write("#\n\n")

        for command in all_commands:
            f.write(command + "\n")

    print(f"\n{'='*80}")
    print(f"SUCCESS! Generated rename script: {output_file}")
    print(f"Total files to be renamed: {total_files}")
    print(f"{'='*80}\n")

    # Also create individual scripts per directory
    for dir_name, dir_path in DIRECTORIES.items():
        commands = process_directory(dir_name, dir_path)
        if commands:
            safe_dir_name = dir_name.replace(':', '-')
            individual_output = os.path.join(
                r"C:\Users\liang\GitHub\strategies",
                f"rename_{safe_dir_name}.sh"
            )

            with open(individual_output, 'w', encoding='utf-8') as f:
                f.write("#!/bin/bash\n")
                f.write(f"# Rename script for: {dir_name}\n\n")
                for command in commands:
                    f.write(command + "\n")

            print(f"Created individual script: {individual_output}")

if __name__ == "__main__":
    main()
