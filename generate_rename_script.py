#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate rename commands for 2,453 markdown files
Follows the format: 序号-中文名-英文名.md
"""

import re
import os
from pathlib import Path
from typing import Tuple, List

def extract_names_from_filename(filename: str) -> Tuple[str, str]:
    """
    Extract Chinese and English names from filename.
    Returns: (chinese_name, english_name)
    """
    # Remove .md extension
    name = filename.replace('.md', '')

    # Pattern 1: Chinese-English (策略-Strategy or 策略Strategy)
    # Split by common patterns
    parts = []

    # Try to find Chinese characters
    chinese_match = re.search(r'[\u4e00-\u9fff]+', name)

    # Extract all Chinese segments
    chinese_parts = re.findall(r'[\u4e00-\u9fff]+', name)
    chinese_name = ''.join(chinese_parts) if chinese_parts else ''

    # Extract English parts (remove Chinese and clean up)
    english_temp = re.sub(r'[\u4e00-\u9fff]+', '', name)
    # Clean up separators
    english_temp = re.sub(r'^[-_]+|[-_]+$', '', english_temp)
    # Replace multiple separators with single hyphen
    english_temp = re.sub(r'[-_]+', '-', english_temp)
    # Convert to lowercase
    english_name = english_temp.lower().strip('-_')

    # If no Chinese found, try to generate from English
    if not chinese_name and english_name:
        # Common English to Chinese mappings for key strategy terms
        cn_map = {
            'strategy': '策略',
            'trading': '交易',
            'trend': '趋势',
            'momentum': '动量',
            'breakout': '突破',
            'crossover': '交叉',
            'ema': 'EMA',
            'sma': 'SMA',
            'macd': 'MACD',
            'rsi': 'RSI',
            'bollinger': '布林带',
            'atr': 'ATR',
            'volume': '成交量',
            'moving-average': '移动平均',
            'exponential': '指数',
            'dual': '双',
            'triple': '三',
            'multi': '多',
            'indicator': '指标',
        }
        # Extract key terms for Chinese name generation
        for eng, cn in cn_map.items():
            if eng in english_name.lower() and cn not in chinese_name:
                chinese_name += cn

    return chinese_name, english_name

def normalize_name(chinese: str, english: str) -> str:
    """
    Normalize name to format: chinese-english
    All English lowercase with hyphens
    """
    # Clean Chinese name
    chinese_clean = re.sub(r'[^\u4e00-\u9fff0-9A-Za-z]+', '', chinese)

    # Clean English name - convert to kebab-case
    english_clean = english.lower()
    # Replace spaces and underscores with hyphens
    english_clean = re.sub(r'[\s_]+', '-', english_clean)
    # Remove special characters except hyphens
    english_clean = re.sub(r'[^a-z0-9-]+', '-', english_clean)
    # Remove multiple consecutive hyphens
    english_clean = re.sub(r'-+', '-', english_clean)
    # Remove leading/trailing hyphens
    english_clean = english_clean.strip('-')

    if chinese_clean and english_clean:
        return f"{chinese_clean}-{english_clean}"
    elif chinese_clean:
        return chinese_clean
    elif english_clean:
        return english_clean
    else:
        return "unknown-strategy"

def read_filenames(filepath: str) -> List[str]:
    """Read all filenames from the sorted file list."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def generate_rename_commands(filenames: List[str], base_dir: str) -> Tuple[List[str], List[str]]:
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

        # Generate normalized name
        normalized = normalize_name(chinese, english)

        # Create new filename with sequence number
        new_filename = f"{idx:03d}-{normalized}.md"

        # Escape quotes and special characters for bash
        old_escaped = old_filename.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')
        new_escaped = new_filename.replace('"', '\\"').replace('$', '\\$').replace('`', '\\`')

        # Generate git mv command
        cmd = f'git mv "{old_escaped}" "{new_escaped}"'
        commands.append(cmd)

        # Store mapping for reference
        name_mapping.append(f"# {idx:03d}: {old_filename} -> {new_filename}")

    return commands, name_mapping

def main():
    """Main function to generate the rename script."""
    # Read sorted filenames
    filenames = read_filenames('C:/Users/liang/GitHub/strategies/sorted_files.txt')

    print(f"Total files to process: {len(filenames)}")

    # Generate rename commands
    base_dir = r"C:\Users\liang\GitHub\strategies\01-技术指标-移动平均线"
    commands, mappings = generate_rename_commands(filenames, base_dir)

    # Write the complete bash script
    output_script = 'C:/Users/liang/GitHub/strategies/rename_script.sh'
    with open(output_script, 'w', encoding='utf-8', newline='\n') as f:
        f.write('#!/bin/bash\n')
        f.write('# Rename script for 2,453 markdown files\n')
        f.write('# Format: 序号-中文名-英文名.md\n')
        f.write('# Generated automatically\n\n')
        f.write(f'cd "C:/Users/liang/GitHub/strategies/01-技术指标-移动平均线"\n\n')
        f.write('# File rename mappings:\n')

        # Write first 20 mappings as examples
        for mapping in mappings[:20]:
            f.write(f'{mapping}\n')
        f.write(f'# ... and {len(mappings) - 20} more files\n\n')

        f.write('echo "Starting rename process..."\n')
        f.write('echo "Total files to rename: {}"\n\n'.format(len(commands)))

        # Write all commands
        for i, cmd in enumerate(commands, start=1):
            if i % 100 == 0:
                f.write(f'\necho "Progress: {i}/{len(commands)} files renamed"\n')
            f.write(f'{cmd}\n')

        f.write('\necho "Rename complete! {} files processed."\n'.format(len(commands)))
        f.write('echo "Please review changes with: git status"\n')

    # Also write detailed mapping file
    mapping_file = 'C:/Users/liang/GitHub/strategies/rename_mapping.txt'
    with open(mapping_file, 'w', encoding='utf-8') as f:
        f.write('Complete File Rename Mapping\n')
        f.write('='*80 + '\n\n')
        for mapping in mappings:
            f.write(f'{mapping}\n')

    print(f"\nGenerated files:")
    print(f"1. Rename script: {output_script}")
    print(f"2. Mapping file: {mapping_file}")
    print(f"\nTotal rename commands: {len(commands)}")

    # Show first 10 examples
    print("\n" + "="*80)
    print("First 10 rename examples:")
    print("="*80)
    for i in range(min(10, len(mappings))):
        print(mappings[i])

if __name__ == '__main__':
    main()
