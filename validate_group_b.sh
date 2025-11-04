#!/bin/bash
# Validation script for Trading Method Group B renaming
# This script checks if all files were renamed correctly

echo "=========================================="
echo "Trading Method Group B - Validation"
echo "=========================================="
echo ""

# Directory 16
echo "Directory 16: 反转策略 (Reversal Strategies)"
cd "C:\Users\liang\GitHub\strategies\16-交易方法-反转策略"
TOTAL=$(ls *.md 2>/dev/null | wc -l)
RENAMED=$(ls *.md 2>/dev/null | grep -E '^[0-9]{3}-' | wc -l)
echo "  Total files: $TOTAL"
echo "  Renamed files (format: 001-*): $RENAMED"
echo "  Expected: 169"
if [ "$RENAMED" -eq 169 ]; then
    echo "  Status: ✓ PASS"
else
    echo "  Status: ✗ FAIL"
fi
echo ""

# Directory 17
echo "Directory 17: 突破策略 (Breakout Strategies)"
cd "C:\Users\liang\GitHub\strategies\17-交易方法-突破策略"
TOTAL=$(ls *.md 2>/dev/null | wc -l)
RENAMED=$(ls *.md 2>/dev/null | grep -E '^[0-9]{3}-' | wc -l)
echo "  Total files: $TOTAL"
echo "  Renamed files (format: 001-*): $RENAMED"
echo "  Expected: 294"
if [ "$RENAMED" -eq 294 ]; then
    echo "  Status: ✓ PASS"
else
    echo "  Status: ✗ FAIL"
fi
echo ""

# Directory 18
echo "Directory 18: 定投策略 (DCA Strategies)"
cd "C:\Users\liang\GitHub\strategies\18-交易方法-定投策略"
TOTAL=$(ls *.md 2>/dev/null | wc -l)
RENAMED=$(ls *.md 2>/dev/null | grep -E '^[0-9]{3}-' | wc -l)
echo "  Total files: $TOTAL"
echo "  Renamed files (format: 001-*): $RENAMED"
echo "  Expected: 18"
if [ "$RENAMED" -eq 18 ]; then
    echo "  Status: ✓ PASS"
else
    echo "  Status: ✗ FAIL"
fi
echo ""

# Directory 19
echo "Directory 19: 形态识别 (Pattern Recognition)"
cd "C:\Users\liang\GitHub\strategies\19-交易方法-形态识别"
TOTAL=$(ls *.md 2>/dev/null | wc -l)
RENAMED=$(ls *.md 2>/dev/null | grep -E '^[0-9]{3}-' | wc -l)
echo "  Total files: $TOTAL"
echo "  Renamed files (format: 001-*): $RENAMED"
echo "  Expected: 68"
if [ "$RENAMED" -eq 68 ]; then
    echo "  Status: ✓ PASS"
else
    echo "  Status: ✗ FAIL"
fi
echo ""

# Directory 20
echo "Directory 20: 斐波那契 (Fibonacci)"
cd "C:\Users\liang\GitHub\strategies\20-交易方法-斐波那契"
TOTAL=$(ls *.md 2>/dev/null | wc -l)
RENAMED=$(ls *.md 2>/dev/null | grep -E '^[0-9]{3}-' | wc -l)
echo "  Total files: $TOTAL"
echo "  Renamed files (format: 001-*): $RENAMED"
echo "  Expected: 3"
if [ "$RENAMED" -eq 3 ]; then
    echo "  Status: ✓ PASS"
else
    echo "  Status: ✗ FAIL"
fi
echo ""

echo "=========================================="
echo "Validation Complete"
echo "=========================================="
