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

    # Try to find separator pattern
    # Pattern 1: 中文名-English-Name (with hyphen separator)
    if '-' in name_line:
        parts = name_line.split('-', 1)
        if len(parts) == 2:
            part1 = parts[0].strip()
            part2 = parts[1].strip()

            # Check which part is Chinese
            has_chinese_1 = bool(re.search(r'[\u4e00-\u9fff]', part1))
            has_chinese_2 = bool(re.search(r'[\u4e00-\u9fff]', part2))

            if has_chinese_1 and not has_chinese_2:
                return part1, part2.lower().replace(' ', '-')
            elif not has_chinese_1 and has_chinese_2:
                return part2, part1.lower().replace(' ', '-')

    # Pattern 2: Mixed without clear separator
    chinese_parts = re.findall(r'[\u4e00-\u9fff]+', name_line)
    chinese = ''.join(chinese_parts)

    # Extract English/alphanumeric parts
    english_parts = []
    temp = re.sub(r'[\u4e00-\u9fff]+', ' ', name_line)
    for part in temp.split():
        if part.strip():
            english_parts.append(part.strip())

    english = '-'.join(english_parts).lower()
    english = re.sub(r'[^a-z0-9-]', '-', english)
    english = re.sub(r'-+', '-', english).strip('-')

    return chinese, english

def generate_new_name(idx, chinese, english):
    """Generate new filename in format: 序号-中文名-英文名.md"""
    seq = f"{idx:03d}"

    # Clean up English part
    english = english.lower()
    english = re.sub(r'[^a-z0-9-]', '-', english)
    english = re.sub(r'-+', '-', english).strip('-')

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

    print(f"\nProcessing {dir_path}")
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
            if idx <= 5:  # Print first 5 for verification
                print(f"  {idx:03d}: {filename[:50]}... -> {new_name[:50]}...")

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

print(f"\n{'='*60}")
print(f"All renaming scripts generated successfully!")
print(f"Total files to rename: {total_renames}")
print(f"{'='*60}")
