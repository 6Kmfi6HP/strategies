#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
from pathlib import Path

def extract_strategy_name(filename):
    """Extract Chinese and English names from filename."""
    # Remove .md extension
    name = filename.replace('.md', '')

    # Try to split Chinese and English parts
    chinese = ""
    english = ""

    # Pattern 1: Chinese followed by English (e.g., "策略Strategy")
    match1 = re.search(r'([\u4e00-\u9fff]+)([-\w]+)', name)

    # Pattern 2: Mixed format
    if '策略' in name or '交易' in name or '指标' in name:
        # Extract all Chinese characters
        chinese_parts = re.findall(r'[\u4e00-\u9fff]+', name)
        chinese = ''.join(chinese_parts) if chinese_parts else ""

        # Extract English parts
        english_parts = re.findall(r'[A-Za-z][-A-Za-z0-9]*', name)
        english = '-'.join(english_parts).lower() if english_parts else ""
    else:
        # Mostly English name
        english = name.lower()
        # Try to extract Chinese if any
        chinese_parts = re.findall(r'[\u4e00-\u9fff]+', name)
        chinese = ''.join(chinese_parts) if chinese_parts else ""

    # Clean up
    english = re.sub(r'-+', '-', english).strip('-')

    return chinese, english

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

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"# Renaming script for: {dir_path}\n")
        out.write(f"# Total files: {len(files)}\n\n")
        out.write(f"cd \"{dir_path}\"\n\n")

        for idx, filename in enumerate(files, 1):
            chinese, english = extract_strategy_name(filename)
            new_name = generate_new_name(idx, chinese, english)

            # Only create rename command if name actually changes
            if filename != new_name:
                out.write(f"git mv \"{filename}\" \"{new_name}\"\n")

        out.write(f"\n# Completed: {len(files)} files processed\n")

# Process all four directories
dirs = [
    ("C:/Users/liang/GitHub/strategies/05-技术指标-布林带", "rename_bollinger.sh"),
    ("C:/Users/liang/GitHub/strategies/06-技术指标-ATR", "rename_atr.sh"),
    ("C:/Users/liang/GitHub/strategies/07-技术指标-CCI", "rename_cci.sh"),
    ("C:/Users/liang/GitHub/strategies/08-技术指标-KDJ", "rename_kdj.sh"),
]

for dir_path, output_file in dirs:
    output_path = f"C:/Users/liang/GitHub/strategies/{output_file}"
    process_directory(dir_path, output_path)
    print(f"Generated: {output_path}")

print("\nAll renaming scripts generated successfully!")
