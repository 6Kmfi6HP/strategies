# File Renaming Instructions for 01-技术指标-移动平均线

## Overview
This document provides instructions for renaming 2,453 markdown files in the `01-技术指标-移动平均线` directory.

## Files Generated

1. **rename_script_v2.sh** (499KB, 2,555 lines)
   - Complete bash script with all git mv commands
   - Preserves git history
   - Includes progress indicators
   - Ready to execute

2. **rename_mapping_v2.txt** (515KB)
   - Complete mapping of old names to new names
   - Useful for reference and verification
   - All 2,453 files documented

3. **sorted_files.txt**
   - Alphabetically sorted list of original filenames
   - Used as input for the rename script generator

## Naming Convention

**Format**: `序号-中文名-英文名.md`

Where:
- **序号** (Sequence Number): Three-digit number (001-2453)
- **中文名** (Chinese Name): Extracted from original filename or generated from strategy content
- **英文名** (English Name): Lowercase English description with kebab-case (hyphens)

### Examples:
- Old: `EMA-MACD-动量跟踪策略EMA-MACD-Momentum-Tracking-Strategy.md`
- New: `096-动量跟踪策略-ema-macd-ema-macd-momentum-tracking-strategy.md`

- Old: `3EMA.md`
- New: `010-EMA策略-3ema.md`

- Old: `Adaptive-Bollinger-Bands-Trend-Following-Strategy-with-Multi-Level-Risk-Management-自适应布林带趋势跟踪策略与多层风险管理系统.md`
- New: `020-自适应布林带趋势跟踪策略与多层风险管理系-adaptive-bollinger-bands-trend-following-strategy-multi.md`

## How to Execute

### Step 1: Review the Mapping
Before executing, review the mapping file to ensure correctness:
```bash
less rename_mapping_v2.txt
# or
head -100 rename_mapping_v2.txt
```

### Step 2: Backup (Optional but Recommended)
Create a backup branch:
```bash
cd "C:/Users/liang/GitHub/strategies"
git checkout -b backup-before-rename
git checkout master  # or your working branch
```

### Step 3: Execute the Rename Script
```bash
cd "C:/Users/liang/GitHub/strategies"
bash rename_script_v2.sh
```

The script will:
- Change to the correct directory
- Rename all 2,453 files using `git mv`
- Show progress every 100 files
- Display completion message

### Step 4: Verify the Changes
```bash
cd "C:/Users/liang/GitHub/strategies/01-技术指标-移动平均线"

# Check a few renamed files
ls | head -20

# View git status
git status

# Check total file count
ls *.md | wc -l
```

### Step 5: Commit the Changes
```bash
git add .
git commit -m "Rename moving average strategy files with sequential numbering

- Renamed 2,453 files in 01-技术指标-移动平均线
- Format: 序号-中文名-英文名.md
- Sequential numbering from 001 to 2453
- Lowercase English names with kebab-case
- Preserves git history using git mv"
```

## Rollback (If Needed)

If something goes wrong:

### Option 1: Reset Changes (Before Commit)
```bash
git reset --hard HEAD
```

### Option 2: Revert Commit (After Commit)
```bash
git revert HEAD
```

### Option 3: Use Backup Branch
```bash
git checkout backup-before-rename
```

## Naming Rules Applied

1. **Sequential Numbering**: Files numbered 001-2453 in alphabetical order
2. **Separator**: Hyphen (-) used throughout
3. **Case**: English parts all lowercase
4. **Chinese Text**: Preserved from original filename or generated
5. **Length Limits**:
   - Chinese name: max 20 characters
   - English name: max 60 characters (abbreviated if necessary)
6. **Special Characters**: Removed or converted to hyphens

## Script Features

- **Git History Preservation**: Uses `git mv` instead of `mv`
- **Progress Tracking**: Shows progress every 100 files
- **Error Handling**: Exits if directory doesn't exist
- **Special Character Escaping**: Properly handles quotes, dollar signs, backticks
- **Unix Line Endings**: Compatible with bash on Windows/Git Bash

## Statistics

- Total files: 2,453
- Rename commands: 2,453
- Script size: 499KB
- Mapping file size: 515KB
- Estimated execution time: 2-5 minutes

## Verification Checklist

After execution, verify:
- [ ] File count is still 2,453
- [ ] All files have .md extension
- [ ] Filenames follow format: `\d{3}-.*-.*\.md`
- [ ] No duplicate filenames
- [ ] Git shows 2,453 renamed files
- [ ] Sample files can be opened and read correctly

## Support Files

All generated files are in: `C:/Users/liang/GitHub/strategies/`
- `rename_script_v2.sh` - Main execution script
- `rename_mapping_v2.txt` - Complete mapping reference
- `sorted_files.txt` - Original sorted filenames
- `generate_rename_script_v2.py` - Python script used to generate the rename script

## Notes

- The script is idempotent - running it multiple times will fail safely after first execution
- Chinese character extraction may not be perfect for all files
- Some English names may be abbreviated due to length constraints
- Review mapping file first if you want to make adjustments before execution

## Contact

If you encounter issues or need modifications, review the Python generator script and adjust the naming logic as needed.
