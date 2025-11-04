#!/bin/bash
################################################################################
# Master Renaming Script - Technical Indicator Group B
# Agent 3 - 2025-11-05
#
# This script executes all renaming operations for:
#   - 05-技术指标-布林带 (198 files)
#   - 06-技术指标-ATR (96 files)
#   - 07-技术指标-CCI (55 files)
#   - 08-技术指标-KDJ (50 files)
#
# Total: 399 files
################################################################################

set -e  # Exit on error

PROJECT_ROOT="C:/Users/liang/GitHub/strategies"

echo "================================================================================"
echo "  Technical Indicator Group B - Master Renaming Script"
echo "================================================================================"
echo ""
echo "This script will rename 399 markdown files across 4 directories."
echo "All operations use 'git mv' to preserve file history."
echo ""
echo "Directories:"
echo "  1. 05-技术指标-布林带 (198 files)"
echo "  2. 06-技术指标-ATR (96 files)"
echo "  3. 07-技术指标-CCI (55 files)"
echo "  4. 08-技术指标-KDJ (50 files)"
echo ""
echo "================================================================================"
echo ""

# Confirmation prompt
read -p "Do you want to proceed with the renaming? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Operation cancelled."
    exit 0
fi

echo ""
echo "Starting renaming operations..."
echo ""

# Counter for tracking progress
total_renamed=0

################################################################################
# 1. Bollinger Bands (布林带)
################################################################################
echo "================================================================================"
echo "[1/4] Processing: 05-技术指标-布林带 (198 files)"
echo "================================================================================"

if [ -f "$PROJECT_ROOT/rename_bollinger.sh" ]; then
    bash "$PROJECT_ROOT/rename_bollinger.sh"
    bollinger_count=$(grep -c "^git mv" "$PROJECT_ROOT/rename_bollinger.sh" || echo 0)
    total_renamed=$((total_renamed + bollinger_count))
    echo "✓ Completed: $bollinger_count files renamed"
else
    echo "✗ Error: rename_bollinger.sh not found"
    exit 1
fi

echo ""

################################################################################
# 2. ATR
################################################################################
echo "================================================================================"
echo "[2/4] Processing: 06-技术指标-ATR (96 files)"
echo "================================================================================"

if [ -f "$PROJECT_ROOT/rename_atr.sh" ]; then
    bash "$PROJECT_ROOT/rename_atr.sh"
    atr_count=$(grep -c "^git mv" "$PROJECT_ROOT/rename_atr.sh" || echo 0)
    total_renamed=$((total_renamed + atr_count))
    echo "✓ Completed: $atr_count files renamed"
else
    echo "✗ Error: rename_atr.sh not found"
    exit 1
fi

echo ""

################################################################################
# 3. CCI
################################################################################
echo "================================================================================"
echo "[3/4] Processing: 07-技术指标-CCI (55 files)"
echo "================================================================================"

if [ -f "$PROJECT_ROOT/rename_cci.sh" ]; then
    bash "$PROJECT_ROOT/rename_cci.sh"
    cci_count=$(grep -c "^git mv" "$PROJECT_ROOT/rename_cci.sh" || echo 0)
    total_renamed=$((total_renamed + cci_count))
    echo "✓ Completed: $cci_count files renamed"
else
    echo "✗ Error: rename_cci.sh not found"
    exit 1
fi

echo ""

################################################################################
# 4. KDJ
################################################################################
echo "================================================================================"
echo "[4/4] Processing: 08-技术指标-KDJ (50 files)"
echo "================================================================================"

if [ -f "$PROJECT_ROOT/rename_kdj.sh" ]; then
    bash "$PROJECT_ROOT/rename_kdj.sh"
    kdj_count=$(grep -c "^git mv" "$PROJECT_ROOT/rename_kdj.sh" || echo 0)
    total_renamed=$((total_renamed + kdj_count))
    echo "✓ Completed: $kdj_count files renamed"
else
    echo "✗ Error: rename_kdj.sh not found"
    exit 1
fi

echo ""

################################################################################
# Summary
################################################################################
echo "================================================================================"
echo "  SUMMARY"
echo "================================================================================"
echo ""
echo "✓ All renaming operations completed successfully!"
echo ""
echo "Statistics:"
echo "  - Directories processed: 4"
echo "  - Total files renamed: $total_renamed"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Check diff: git diff --name-status"
echo "  3. Commit changes: git commit -m 'Rename technical indicator files (Group B)'"
echo ""
echo "================================================================================"
