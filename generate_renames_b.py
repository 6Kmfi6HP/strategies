#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import re
import sys

# Force UTF-8 output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DIRS = [
    (r"C:\Users\liang\GitHub\strategies\16-交易方法-反转策略", "16-reversal"),
    (r"C:\Users\liang\GitHub\strategies\17-交易方法-突破策略", "17-breakout"),
    (r"C:\Users\liang\GitHub\strategies\18-交易方法-定投策略", "18-dca"),
    (r"C:\Users\liang\GitHub\strategies\19-交易方法-形态识别", "19-pattern"),
    (r"C:\Users\liang\GitHub\strategies\20-交易方法-斐波那契", "20-fibonacci")
]

def extract_names(filename):
    """Extract Chinese and English parts from filename."""
    name = filename.replace('.md', '')

    chinese = []
    english = []

    # Split by common separators
    parts = re.split(r'[-_]', name)

    for part in parts:
        if not part:
            continue
        if re.search(r'[\u4e00-\u9fff]', part):
            chinese.append(part)
        elif re.search(r'[a-zA-Z]', part):
            english.append(part)

    cn = ''.join(chinese)
    en = '-'.join(english).lower()

    # Clean
    cn = re.sub(r'^[^\u4e00-\u9fff]+', '', cn)
    cn = re.sub(r'[^\u4e00-\u9fff]+$', '', cn)
    en = re.sub(r'^-+|-+$', '', en)
    en = re.sub(r'-{2,}', '-', en)

    return cn, en

def process_dir(dirpath, dirname):
    """Process one directory."""
    if not os.path.exists(dirpath):
        return []

    files = sorted([f for f in os.listdir(dirpath) if f.endswith('.md')])
    commands = [f"\n# {dirname} ({len(files)} files)", f'cd "{dirpath}"', ""]

    for i, old in enumerate(files, 1):
        cn, en = extract_names(old)
        seq = f"{i:03d}"

        if cn and en:
            new = f"{seq}-{cn}-{en}.md"
        elif cn:
            new = f"{seq}-{cn}.md"
        elif en:
            new = f"{seq}-{en}.md"
        else:
            new = f"{seq}-{old}"

        if old != new:
            commands.append(f'git mv "{old}" "{new}"')

    return commands

def main():
    all_cmds = ["#!/bin/bash", "# Trading Method Group B Rename Script", ""]
    total = 0

    for dirpath, dirname in DIRS:
        cmds = process_dir(dirpath, dirname)
        all_cmds.extend(cmds)
        total += len([c for c in cmds if c.startswith('git mv')])

    output = r"C:\Users\liang\GitHub\strategies\rename_group_b.sh"
    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_cmds))

    print(f"Generated: {output}")
    print(f"Total renames: {total}")

if __name__ == "__main__":
    main()
