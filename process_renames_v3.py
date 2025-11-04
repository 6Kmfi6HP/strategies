#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys
from pathlib import Path

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def read_strategy_name_from_file(filepath):
    """Read the strategy name from file content (from > Name section)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(500)  # Read first 500 chars

            # Look for pattern: > Name\n\nActual Name
            match = re.search(r'>\s*Name\s*\n\s*\n(.+?)(?:\n|$)', content, re.MULTILINE)
            if match:
                return match.group(1).strip()
    except Exception as e:
        pass

    return None

def parse_strategy_name(name_line):
    """Parse strategy name into Chinese and English parts."""
    if not name_line:
        return "", ""

    # Clean up the name
    name_line = name_line.strip()

    # Pattern 1: "中文名-English-Name" (clearly separated by hyphen)
    if '-' in name_line:
        # Split only on first hyphen that's between Chinese and English
        # Find the position where Chinese ends and English begins with hyphen
        match = re.search(r'([\u4e00-\u9fff].+?)-([A-Z][A-Za-z0-9\-\s]+)', name_line)
        if match:
            chinese = match.group(1).strip()
            english = match.group(2).strip()

            # Clean up English part
            english = english.lower().replace(' ', '-')
            english = re.sub(r'[^a-z0-9-]', '-', english)
            english = re.sub(r'-+', '-', english).strip('-')

            return chinese, english

    # Pattern 2: "中文名EnglishName" (no separator, mixed directly)
    # Find where Chinese ends and English begins
    match = re.search(r'([\u4e00-\u9fff]+)(.*)', name_line)
    if match:
        chinese = match.group(1).strip()
        rest = match.group(2).strip()

        # Extract English parts
        if rest:
            english = rest.lower().replace(' ', '-')
            english = re.sub(r'[^a-z0-9-]', '-', english)
            english = re.sub(r'-+', '-', english).strip('-')
        else:
            english = ""

        return chinese, english

    # Pattern 3: English only
    english = name_line.lower().replace(' ', '-')
    english = re.sub(r'[^a-z0-9-]', '-', english)
    english = re.sub(r'-+', '-', english).strip('-')

    return "", english

def generate_new_name(idx, chinese, english):
    """Generate new filename in format: 序号-中文名-英文名.md"""
    seq = f"{idx:03d}"

    if chinese and english:
        return f"{seq}-{chinese}-{english}.md"
    elif chinese:
        return f"{seq}-{chinese}.md"
    elif english:
        return f"{seq}-{english}.md"
    else:
        return f"{seq}-untitled.md"

def process_directory(dir_path, output_file):
    """Process all MD files in directory and generate rename script."""
    files = sorted([f for f in os.listdir(dir_path) if f.endswith('.md')])

    dir_name = os.path.basename(dir_path)
    print(f"\nProcessing {dir_name}")
    print(f"Found {len(files)} files")

    rename_commands = []

    for idx, filename in enumerate(files, 1):
        filepath = os.path.join(dir_path, filename)

        # Try to read name from file content
        name_from_content = read_strategy_name_from_file(filepath)

        if name_from_content:
            chinese, english = parse_strategy_name(name_from_content)
        else:
            # Fallback: parse from filename
            chinese, english = parse_strategy_name(filename.replace('.md', ''))

        new_name = generate_new_name(idx, chinese, english)

        # Only create rename command if name actually changes
        if filename != new_name:
            rename_commands.append((filename, new_name))
            if idx <= 10:  # Print first 10 for verification
                print(f"  {idx:03d}: [{chinese[:30] if chinese else 'N/A':30s}] [{english[:50] if english else 'N/A':50s}]")

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"#!/bin/bash\n")
        out.write(f"# Renaming script for: {os.path.basename(dir_path)}\n")
        out.write(f"# Total files: {len(files)}\n")
        out.write(f"# Files to rename: {len(rename_commands)}\n\n")
        out.write(f"cd \"{dir_path}\"\n\n")

        for old_name, new_name in rename_commands:
            out.write(f'git mv "{old_name}" "{new_name}"\n')

        out.write(f"\n# Completed: {len(rename_commands)} files renamed\n")

    print(f"  Generated: {output_file} ({len(rename_commands)} renames)")
    return len(rename_commands)

# Process all four directories
dirs = [
    ("C:/Users/liang/GitHub/strategies/05-技术指标-布林带", "rename_bollinger.sh"),
    ("C:/Users/liang/GitHub/strategies/06-技术指标-ATR", "rename_atr.sh"),
    ("C:/Users/liang/GitHub/strategies/07-技术指标-CCI", "rename_cci.sh"),
    ("C:/Users/liang/GitHub/strategies/08-技术指标-KDJ", "rename_kdj.sh"),
]

total_renames = 0
for dir_path, output_file in dirs:
    output_path = f"C:/Users/liang/GitHub/strategies/{output_file}"
    count = process_directory(dir_path, output_path)
    total_renames += count

print(f"\n{'='*80}")
print(f"All renaming scripts generated successfully!")
print(f"Total files to rename: {total_renames}")
print(f"{'='*80}")
