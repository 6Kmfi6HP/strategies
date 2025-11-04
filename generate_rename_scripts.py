#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate renaming scripts for markdown files in technical indicator directories
"""

import os
import re
import sys
from pathlib import Path

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Directory mappings
DIRECTORIES = {
    "09-技术指标-成交量": r"C:\Users\liang\GitHub\strategies\09-技术指标-成交量",
    "10-技术指标-趋势指标": r"C:\Users\liang\GitHub\strategies\10-技术指标-趋势指标",
    "11-技术指标-综合指标": r"C:\Users\liang\GitHub\strategies\11-技术指标-综合指标"
}

def read_file_content(filepath):
    """Read markdown file content"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except:
        try:
            with open(filepath, 'r', encoding='gbk') as f:
                content = f.read()
            return content
        except:
            return ""

def extract_strategy_name(filename, content):
    """Extract strategy name from filename and content"""
    # Remove .md extension
    name = filename.replace('.md', '')

    # Try to extract Chinese and English parts from filename
    chinese_part = ""
    english_part = ""

    # Pattern 1: Chinese-English split
    if '-' in name:
        parts = name.split('-')
        chinese_chars = []
        english_chars = []

        for part in parts:
            if re.search(r'[\u4e00-\u9fff]', part):
                chinese_chars.append(part)
            else:
                english_chars.append(part)

        if chinese_chars:
            chinese_part = '-'.join(chinese_chars)
        if english_chars:
            english_part = '-'.join(english_chars).lower()

    # If no clear separation, try to extract from content
    if not chinese_part or not english_part:
        # Look for title in content
        lines = content.split('\n')[:10]  # Check first 10 lines
        for line in lines:
            if line.startswith('#'):
                title = line.lstrip('#').strip()
                # Try to split Chinese and English
                if re.search(r'[\u4e00-\u9fff]', title):
                    # Extract Chinese
                    chinese_match = re.findall(r'[\u4e00-\u9fff]+(?:[\u4e00-\u9fff\s]*[\u4e00-\u9fff]+)*', title)
                    if chinese_match and not chinese_part:
                        chinese_part = ''.join(chinese_match).strip()

                    # Extract English
                    english_match = re.sub(r'[\u4e00-\u9fff\s]+', '', title)
                    if english_match and not english_part:
                        english_part = re.sub(r'[^a-zA-Z0-9\s-]', '', english_match)
                        english_part = re.sub(r'\s+', '-', english_part.strip()).lower()
                break

    # Fallback: use original filename parts
    if not chinese_part:
        # Try to find any Chinese in original name
        chinese_match = re.findall(r'[\u4e00-\u9fff]+', name)
        if chinese_match:
            chinese_part = ''.join(chinese_match)
        else:
            chinese_part = "策略"  # Default

    if not english_part:
        # Clean up and use filename
        english_part = re.sub(r'[\u4e00-\u9fff]+', '', name)
        english_part = re.sub(r'[^a-zA-Z0-9\s-]', ' ', english_part)
        english_part = re.sub(r'\s+', '-', english_part.strip()).lower()
        if not english_part:
            english_part = "strategy"

    # Clean up
    chinese_part = chinese_part.strip().replace(' ', '-')
    english_part = english_part.strip().lower()
    english_part = re.sub(r'-+', '-', english_part)
    english_part = english_part.strip('-')

    return chinese_part, english_part

def generate_rename_script(directory_name, directory_path):
    """Generate rename script for a directory"""
    print(f"\n{'='*80}")
    print(f"Processing: {directory_name}")
    print(f"{'='*80}\n")

    # Get all markdown files
    md_files = sorted([f for f in os.listdir(directory_path) if f.endswith('.md')])

    print(f"Total files: {len(md_files)}\n")

    # Generate renaming commands
    rename_commands = []
    rename_commands.append(f"# {directory_name} - Renaming Script")
    rename_commands.append(f"# Total files: {len(md_files)}")
    rename_commands.append(f"# Directory: {directory_path}\n")

    for idx, filename in enumerate(md_files, start=1):
        filepath = os.path.join(directory_path, filename)
        content = read_file_content(filepath)

        # Extract strategy names
        chinese_name, english_name = extract_strategy_name(filename, content)

        # Generate new filename
        new_filename = f"{idx:03d}-{chinese_name}-{english_name}.md"

        # Generate git mv command
        if filename != new_filename:
            cmd = f'git mv "{filename}" "{new_filename}"'
            rename_commands.append(cmd)
        else:
            rename_commands.append(f"# Already correct: {filename}")

    # Print to console
    for cmd in rename_commands:
        print(cmd)

    # Save to file
    script_filename = f"rename_script_{directory_name.split('-')[0]}.sh"
    script_path = os.path.join(directory_path, script_filename)

    with open(script_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(rename_commands))

    print(f"\n✓ Script saved to: {script_path}\n")

    return rename_commands

def main():
    """Main function"""
    print("="*80)
    print("MARKDOWN FILE RENAMING SCRIPT GENERATOR")
    print("="*80)

    all_scripts = {}

    for dir_name, dir_path in DIRECTORIES.items():
        if os.path.exists(dir_path):
            scripts = generate_rename_script(dir_name, dir_path)
            all_scripts[dir_name] = scripts
        else:
            print(f"⚠ Directory not found: {dir_path}")

    # Generate master script
    master_script_path = r"C:\Users\liang\GitHub\strategies\rename_all_master.sh"
    with open(master_script_path, 'w', encoding='utf-8') as f:
        f.write("#!/bin/bash\n")
        f.write("# Master renaming script for all technical indicator directories\n")
        f.write("# Generated automatically\n\n")

        for dir_name, scripts in all_scripts.items():
            f.write(f"\n# {'='*60}\n")
            f.write(f"# {dir_name}\n")
            f.write(f"# {'='*60}\n")
            dir_path = DIRECTORIES[dir_name]
            f.write(f'cd "{dir_path}"\n\n')

            for cmd in scripts:
                if cmd.startswith('git mv'):
                    f.write(cmd + '\n')
            f.write('\n')

    print("="*80)
    print(f"✓ MASTER SCRIPT SAVED: {master_script_path}")
    print("="*80)
    print("\nSUMMARY:")
    for dir_name in all_scripts:
        print(f"  - {dir_name}: {len([c for c in all_scripts[dir_name] if c.startswith('git mv')])} files to rename")
    print("\nRun the master script to apply all changes:")
    print(f"  bash {master_script_path}")
    print("="*80)

if __name__ == "__main__":
    main()
