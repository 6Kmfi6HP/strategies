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
    """
    Parse strategy name into Chinese and English parts.

    Handles formats:
    1. "English-Part-Chinese" (e.g., "Bollinger-Bands-Breakout-Strategy-布林带突破策略")
    2. "ChineseEnglish" (e.g., "策略BBB-Strategy")
    3. "Chinese-English" (e.g., "动态布林带突破趋势追踪策略-Dynamic-Bollinger-Bands-Breakout")
    """
    if not name_line:
        return "", ""

    name_line = name_line.strip()

    # Find all Chinese characters
    chinese_parts = re.findall(r'[\u4e00-\u9fff]+', name_line)
    chinese_full = ''.join(chinese_parts)

    # Find all English/alphanumeric parts
    # Remove Chinese characters and split by non-alphanumeric
    english_temp = re.sub(r'[\u4e00-\u9fff]+', ' ', name_line)
    english_parts = re.findall(r'[A-Za-z0-9]+', english_temp)

    # Build English name
    english_full = '-'.join(english_parts).lower() if english_parts else ""

    # Clean up
    english_full = re.sub(r'-+', '-', english_full).strip('-')

    return chinese_full, english_full

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
    print(f"\nProcessing: {dir_name}")
    print(f"Total files: {len(files)}")
    print(f"{'='*80}")

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
                ch_display = chinese[:25] if chinese else 'N/A'
                en_display = english[:45] if english else 'N/A'
                print(f"{idx:03d}. CN: {ch_display:25s} | EN: {en_display:45s}")

    # Write to output file
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"#!/bin/bash\n")
        out.write(f"# Renaming script for: {os.path.basename(dir_path)}\n")
        out.write(f"# Total files: {len(files)}\n")
        out.write(f"# Files to rename: {len(rename_commands)}\n")
        out.write(f"# Generated on: 2025-11-05\n\n")
        out.write(f"cd \"{dir_path}\"\n\n")

        for old_name, new_name in rename_commands:
            out.write(f'git mv "{old_name}" "{new_name}"\n')

        out.write(f"\necho \"Completed: {len(rename_commands)} files renamed\"\n")

    print(f"... (showing first 5 of {len(rename_commands)} renames)")
    print(f"Output: {output_file}")

    return len(rename_commands)

# Main execution
print("="*80)
print("  Markdown File Renaming Script Generator")
print("  Technical Indicators Group B (Bollinger/ATR/CCI/KDJ)")
print("="*80)

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
print(f"SUMMARY:")
print(f"  - Scripts generated: 4")
print(f"  - Total files processed: 399")
print(f"  - Total renames required: {total_renames}")
print(f"{'='*80}")
print(f"\nTo execute the renames, run:")
print(f"  bash rename_bollinger.sh")
print(f"  bash rename_atr.sh")
print(f"  bash rename_cci.sh")
print(f"  bash rename_kdj.sh")
print(f"{'='*80}")
