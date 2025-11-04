#!/bin/bash
################################################################################
# Pre-Rename Verification Script
# Agent 3 - 2025-11-05
#
# This script verifies that all files and scripts are ready before renaming
################################################################################

PROJECT_ROOT="C:/Users/liang/GitHub/strategies"

echo "================================================================================"
echo "  Pre-Rename Verification Script"
echo "  Technical Indicator Group B"
echo "================================================================================"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

errors=0
warnings=0

################################################################################
# 1. Check if scripts exist
################################################################################
echo "1. Checking renaming scripts..."

scripts=(
    "rename_bollinger.sh"
    "rename_atr.sh"
    "rename_cci.sh"
    "rename_kdj.sh"
    "rename_all_group_b.sh"
)

for script in "${scripts[@]}"; do
    if [ -f "$PROJECT_ROOT/$script" ]; then
        echo "  ✓ $script found"
    else
        echo "  ✗ $script NOT FOUND"
        errors=$((errors + 1))
    fi
done

echo ""

################################################################################
# 2. Check if directories exist
################################################################################
echo "2. Checking target directories..."

dirs=(
    "05-技术指标-布林带"
    "06-技术指标-ATR"
    "07-技术指标-CCI"
    "08-技术指标-KDJ"
)

expected_counts=(198 96 55 50)

for i in "${!dirs[@]}"; do
    dir="${dirs[$i]}"
    expected="${expected_counts[$i]}"
    dir_path="$PROJECT_ROOT/$dir"

    if [ -d "$dir_path" ]; then
        actual=$(find "$dir_path" -maxdepth 1 -name "*.md" -type f | wc -l)
        if [ "$actual" -eq "$expected" ]; then
            echo "  ✓ $dir ($actual files)"
        else
            echo "  ⚠ $dir (expected $expected files, found $actual)"
            warnings=$((warnings + 1))
        fi
    else
        echo "  ✗ $dir NOT FOUND"
        errors=$((errors + 1))
    fi
done

echo ""

################################################################################
# 3. Check git status
################################################################################
echo "3. Checking git status..."

cd "$PROJECT_ROOT" || exit 1

if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  ✓ Git repository detected"

    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
        echo "  ⚠ Warning: You have uncommitted changes"
        warnings=$((warnings + 1))
        echo ""
        echo "    Current git status:"
        git status --short | head -10
        if [ "$(git status --short | wc -l)" -gt 10 ]; then
            echo "    ... (and more)"
        fi
    else
        echo "  ✓ Working directory is clean"
    fi
else
    echo "  ✗ Not a git repository"
    errors=$((errors + 1))
fi

echo ""

################################################################################
# 4. Count total rename commands
################################################################################
echo "4. Counting rename commands..."

total_commands=0

for script in "rename_bollinger.sh" "rename_atr.sh" "rename_cci.sh" "rename_kdj.sh"; do
    if [ -f "$PROJECT_ROOT/$script" ]; then
        count=$(grep -c "^git mv" "$PROJECT_ROOT/$script" 2>/dev/null || echo 0)
        total_commands=$((total_commands + count))
        echo "  • $script: $count commands"
    fi
done

echo ""
echo "  Total rename commands: $total_commands"

if [ "$total_commands" -ne 399 ]; then
    echo "  ⚠ Warning: Expected 399 commands, found $total_commands"
    warnings=$((warnings + 1))
else
    echo "  ✓ Command count matches expected (399)"
fi

echo ""

################################################################################
# 5. Sample file checks
################################################################################
echo "5. Checking sample files..."

sample_files=(
    "05-技术指标-布林带/Bollinger-Bands-Breakout-Strategy-布林带突破策略.md"
    "06-技术指标-ATR/ATR-Smoothed.md"
    "07-技术指标-CCI/CCI-MTF-ObOs.md"
    "08-技术指标-KDJ/Stochastic动量突破策略Stochastic-Momentum-Breakout-Strategy.md"
)

for file in "${sample_files[@]}"; do
    if [ -f "$PROJECT_ROOT/$file" ]; then
        echo "  ✓ Sample file exists: ${file##*/}"
    else
        echo "  ✗ Sample file missing: $file"
        errors=$((errors + 1))
    fi
done

echo ""

################################################################################
# Summary
################################################################################
echo "================================================================================"
echo "  VERIFICATION SUMMARY"
echo "================================================================================"
echo ""

if [ $errors -eq 0 ] && [ $warnings -eq 0 ]; then
    echo "✓ All checks passed! Ready to proceed with renaming."
    echo ""
    echo "To execute the renaming, run:"
    echo "  bash rename_all_group_b.sh"
    exit 0
elif [ $errors -eq 0 ]; then
    echo "⚠ Verification completed with $warnings warning(s)."
    echo ""
    echo "You can proceed, but review warnings above."
    echo ""
    echo "To execute the renaming, run:"
    echo "  bash rename_all_group_b.sh"
    exit 0
else
    echo "✗ Verification failed with $errors error(s) and $warnings warning(s)."
    echo ""
    echo "Please fix the errors above before proceeding."
    exit 1
fi
