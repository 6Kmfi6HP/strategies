#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced script to generate rename commands for 2,453 markdown files
Follows the format: 序号-中文名-英文名.md
Version 2: Better Chinese extraction and name handling
"""

import re
import os
from typing import Tuple, List

def extract_names_from_filename(filename: str) -> Tuple[str, str]:
    """
    Extract Chinese and English names from filename.
    Returns: (chinese_name, english_name)
    """
    # Remove .md extension
    name = filename.replace('.md', '')

    # Strategy 1: Check if there's a clear separation pattern
    # Pattern: Chinese部分English-Part or Chinese-English

    # Extract all Chinese text (keep together in segments)
    chinese_segments = re.findall(r'[\u4e00-\u9fff]+', name)
    chinese_name = ''.join(chinese_segments)

    # Extract English parts by removing Chinese
    english_part = name
    for seg in chinese_segments:
        english_part = english_part.replace(seg, ' ')

    # Clean up English part
    english_part = re.sub(r'[-_]+', '-', english_part)  # Normalize separators
    english_part = re.sub(r'\s+', '-', english_part)     # Spaces to hyphens
    english_part = re.sub(r'[^a-zA-Z0-9-]+', '-', english_part)  # Remove special chars
    english_part = re.sub(r'-+', '-', english_part)      # Multiple hyphens to single
    english_part = english_part.strip('-').lower()       # Clean and lowercase

    # If Chinese name is too long or seems incomplete, try to extract key terms
    if len(chinese_name) > 40:
        # Keep main strategy keywords
        key_terms = ['策略', '交易', '趋势', '动量', '突破', '交叉', '跟踪', '优化', '系统', '方法']
        filtered = ''
        for i, char in enumerate(chinese_name):
            if i < 30 or any(term in chinese_name[i:i+2] for term in key_terms):
                filtered += char
            if len(filtered) >= 30:
                break
        if filtered:
            chinese_name = filtered + '策略'

    # If no Chinese name found, generate descriptive Chinese from English
    if not chinese_name:
        # Map common English terms to Chinese
        term_map = {
            'ema': 'EMA',
            'sma': 'SMA',
            'macd': 'MACD',
            'rsi': 'RSI',
            'atr': 'ATR',
            'bollinger': '布林',
            'trend': '趋势',
            'strategy': '策略',
            'trading': '交易',
            'crossover': '交叉',
            'breakout': '突破',
            'momentum': '动量',
            'volume': '量',
            'moving-average': '均线',
            'exponential': '指数',
            'simple': '简单',
        }

        cn_parts = []
        for eng, cn in term_map.items():
            if eng in english_part.lower():
                if cn not in cn_parts:
                    cn_parts.append(cn)

        chinese_name = ''.join(cn_parts[:5]) + '策略' if cn_parts else '移动平均策略'

    return chinese_name, english_part

def generate_new_filename(seq_num: int, chinese: str, english: str) -> str:
    """
    Generate new filename in format: 001-中文名-english-name.md
    """
    # Ensure Chinese name isn't too long (max 20 chars)
    if len(chinese) > 20:
        chinese = chinese[:20]

    # Ensure English name isn't too long (max 60 chars)
    if len(english) > 60:
        # Try to abbreviate by removing common filler words
        english = re.sub(r'-with-|-based-|-using-', '-', english)
        if len(english) > 60:
            english = english[:60].rsplit('-', 1)[0]  # Cut at last hyphen

    # Construct filename
    new_name = f"{seq_num:03d}-{chinese}-{english}.md"

    return new_name

def read_filenames(filepath: str) -> List[str]:
    """Read all filenames from the sorted file list."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def generate_rename_commands(filenames: List[str]) -> Tuple[List[str], List[str]]:
    """
    Generate git mv commands for all files.
    Returns tuple of (commands, name_mappings).
    """
    commands = []
    name_mapping = []

    # Process each file
    for idx, old_filename in enumerate(filenames, start=1):
        # Extract names
        chinese, english = extract_names_from_filename(old_filename)

        # Generate new filename
        new_filename = generate_new_filename(idx, chinese, english)

        # Escape special characters for bash
        old_escaped = old_filename.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
        new_escaped = new_filename.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')

        # Generate git mv command
        cmd = f'git mv "{old_escaped}" "{new_escaped}"'
        commands.append(cmd)

        # Store mapping for reference
        name_mapping.append(f"# {idx:03d}: {old_filename}")
        name_mapping.append(f"#  ->  {new_filename}")
        name_mapping.append("")

    return commands, name_mapping

def write_rename_script(commands: List[str], mappings: List[str], output_path: str):
    """Write the bash rename script."""
    with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('#!/bin/bash\n')
        f.write('# Rename script for 2,453 markdown files in 01-技术指标-移动平均线\n')
        f.write('# Format: 序号-中文名-英文名.md\n')
        f.write('# Generated automatically - Version 2\n')
        f.write('# Usage: bash rename_script_v2.sh\n\n')

        f.write('# Change to the target directory\n')
        f.write('cd "C:/Users/liang/GitHub/strategies/01-技术指标-移动平均线" || exit 1\n\n')

        f.write('echo "==================================="\n')
        f.write('echo "Starting rename process..."\n')
        f.write('echo "==================================="\n')
        f.write('echo "Total files to rename: {}"\n'.format(len(commands)))
        f.write('echo ""\n\n')

        f.write('# Counter for progress\n')
        f.write('count=0\n\n')

        # Write all commands with progress indicator
        for i, cmd in enumerate(commands, start=1):
            f.write(f'{cmd}\n')

            if i % 100 == 0:
                f.write('((count+=100))\n')
                f.write(f'echo "Progress: $count/{len(commands)} files renamed..."\n\n')

        # Final message
        remaining = len(commands) % 100
        if remaining > 0:
            f.write(f'((count+={remaining}))\n')

        f.write('\necho ""\n')
        f.write('echo "==================================="\n')
        f.write('echo "Rename complete!"\n')
        f.write('echo "Total: {} files processed"\n'.format(len(commands)))
        f.write('echo "==================================="\n')
        f.write('echo ""\n')
        f.write('echo "Next steps:"\n')
        f.write('echo "1. Review changes: git status"\n')
        f.write('echo "2. Check a few files: ls | head -20"\n')
        f.write('echo "3. Commit changes: git commit -m \'Rename strategy files with sequential numbers\'"\n')

def write_mapping_file(mappings: List[str], output_path: str):
    """Write the detailed mapping file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('='*80 + '\n')
        f.write('Complete File Rename Mapping\n')
        f.write('Directory: 01-技术指标-移动平均线\n')
        f.write('Total files: 2,453\n')
        f.write('='*80 + '\n\n')

        for line in mappings:
            f.write(f'{line}\n')

def main():
    """Main function to generate the rename script."""
    print("="*80)
    print("Generating rename script for moving average strategy files")
    print("="*80)

    # Read sorted filenames
    input_file = 'C:/Users/liang/GitHub/strategies/sorted_files.txt'
    filenames = read_filenames(input_file)

    print(f"\nTotal files to process: {len(filenames)}")

    # Generate rename commands
    commands, mappings = generate_rename_commands(filenames)

    # Write the complete bash script
    script_path = 'C:/Users/liang/GitHub/strategies/rename_script_v2.sh'
    write_rename_script(commands, mappings, script_path)

    # Write detailed mapping file
    mapping_path = 'C:/Users/liang/GitHub/strategies/rename_mapping_v2.txt'
    write_mapping_file(mappings, mapping_path)

    print(f"\nGenerated files:")
    print(f"  1. Rename script: {script_path}")
    print(f"  2. Mapping file:  {mapping_path}")
    print(f"\nTotal rename commands: {len(commands)}")

    # Show first 15 examples
    print("\n" + "="*80)
    print("First 15 rename examples:")
    print("="*80)
    for i in range(0, min(45, len(mappings)), 3):
        if mappings[i].startswith('#'):
            print(mappings[i])
            print(mappings[i+1])
            print()

    print("="*80)
    print("\nTo execute the rename:")
    print("  bash rename_script_v2.sh")
    print("\nIMPORTANT: Review the mapping file first to ensure correctness!")
    print("="*80)

if __name__ == '__main__':
    main()
