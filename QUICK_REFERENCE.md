# Quick Reference - File Renaming Guide

## Files Generated

1. **rename_scripts.sh** - Complete bash script (585 lines, 551 git mv commands)
2. **RENAMING_SUMMARY.md** - Detailed report with samples and instructions
3. **QUICK_REFERENCE.md** - This quick reference guide

## Quick Stats

| Directory | Location | Files | Range |
|-----------|----------|-------|-------|
| MACD | `02-技术指标-MACD` | 11 | 001-011 |
| RSI | `03-技术指标-RSI` | 494 | 001-494 |
| ADX | `04-技术指标-ADX` | 46 | 001-046 |
| **Total** | | **551** | |

## Execute Commands

### Quick Execute (All at once)
```bash
cd "C:\Users\liang\GitHub\strategies"
bash rename_scripts.sh
```

### Safe Execute (Directory by directory)
```bash
# MACD (11 files)
cd "C:\Users\liang\GitHub\strategies\02-技术指标-MACD"
# Copy and run lines 13-23 from rename_scripts.sh

# RSI (494 files)
cd "C:\Users\liang\GitHub\strategies\03-技术指标-RSI"
# Copy and run lines 34-527 from rename_scripts.sh

# ADX (46 files)
cd "C:\Users\liang\GitHub\strategies\04-技术指标-ADX"
# Copy and run lines 538-583 from rename_scripts.sh
```

## Naming Format

**Pattern:** `序号-中文名-英文名.md`

**Example:**
```
001-基于有限马丁格尔的高级MACD策略-advanced-macd-strategy-with-limited-martingale.md
```

**Rules:**
- 3-digit sequence (001, 002, 003...)
- Hyphen separators (kebab-case)
- Lowercase English
- Chinese preserved as-is
- Sequential per directory

## Sample Transformations

### MACD
```
Before: Advanced-MACD-Strategy-with-Limited-Martingale-基于有限马丁格尔的高级MACD策略.md
After:  001-基于有限马丁格尔的高级MACD策略-advanced-macd-strategy-with-limited-martingale.md
```

### RSI
```
Before: RSI与布林带交叉双向回归策略-RSI-and-Bollinger-Bands-Cross-Regression-Dual-Strategy.md
After:  065-RSI与布林带交叉双向回归策略-rsi-and-bollinger-bands-cross-regression-dual-strategy.md
```

### ADX
```
Before: ADX动态平均趋势指标策略ADX-Dynamic-Trend-Strategy.md
After:  003-ADX动态平均趋势指标策略ADX-dynamic-trend-strategy.md
```

## Verification

Run these to verify counts:
```bash
# Count total commands
grep -c "^git mv" rename_scripts.sh
# Should output: 551

# Count by directory
sed -n '/02-技术指标-MACD/,/Total files:/p' rename_scripts.sh | grep -c "^git mv"  # 11
sed -n '/03-技术指标-RSI/,/Total files:/p' rename_scripts.sh | grep -c "^git mv"   # 494
sed -n '/04-技术指标-ADX/,/Total files:/p' rename_scripts.sh | grep -c "^git mv"   # 46
```

## File Locations

All generated files are in: `C:\Users\liang\GitHub\strategies\`

```
strategies/
├── rename_scripts.sh          # Main execution script
├── RENAMING_SUMMARY.md        # Detailed report
├── QUICK_REFERENCE.md         # This file
├── 02-技术指标-MACD/          # 11 files to rename
├── 03-技术指标-RSI/           # 494 files to rename
└── 04-技术指标-ADX/           # 46 files to rename
```

## Next Steps

1. Review the sample commands in RENAMING_SUMMARY.md
2. Optionally test with one file using `--dry-run` flag
3. Execute rename_scripts.sh or run directory by directory
4. Verify results with `ls` in each directory
5. Commit changes with git

---

**Agent 2 Task Complete** ✓
