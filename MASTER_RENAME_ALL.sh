#!/bin/bash
# ============================================================================
# 主重命名脚本 - 统一执行所有目录的MD文件重命名
# ============================================================================
# 总文件数: 5,807 个 MD 文件 (26个目录)
# 重命名格式: 序号-中文名-英文名.md
# 使用 git mv 保留版本历史
# ============================================================================

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 统计变量
TOTAL_FILES=5807
CURRENT_COUNT=0

# 打印彩色信息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 显示进度
show_progress() {
    local files=$1
    local name=$2
    CURRENT_COUNT=$((CURRENT_COUNT + files))
    local percent=$((CURRENT_COUNT * 100 / TOTAL_FILES))
    echo -e "${GREEN}[${percent}%]${NC} 完成 ${files} 个文件 - ${name}"
}

# 主脚本开始
echo "============================================================================"
echo "  策略文件批量重命名工具"
echo "  总计: ${TOTAL_FILES} 个文件 | 26 个目录"
echo "============================================================================"
echo ""

# 检查git状态
print_info "检查 Git 仓库状态..."
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "当前目录不是 Git 仓库！"
    exit 1
fi

if [[ -n $(git status -s) ]]; then
    print_warning "工作区有未提交的更改，建议先提交或暂存"
    read -p "是否继续? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "操作已取消"
        exit 0
    fi
fi

print_success "Git 检查通过"
echo ""

# 询问执行模式
echo "请选择执行模式:"
echo "  [1] 全部执行 (一次性重命名所有 5,807 个文件)"
echo "  [2] 分组执行 (按7个Agent分组，可逐步确认)"
echo "  [3] 按目录执行 (逐个目录执行，共26个目录)"
echo "  [4] 仅预览 (不执行，只显示将要执行的脚本)"
echo ""
read -p "请输入选项 [1-4]: " mode

case $mode in
    1)
        print_info "模式 1: 全部执行"
        echo ""

        # Agent 1: 移动平均线 (2,453)
        print_info "【Agent 1】执行: 01-技术指标-移动平均线 (2,453 文件)"
        if [ -f "rename_script_v2.sh" ]; then
            bash rename_script_v2.sh
            show_progress 2453 "移动平均线"
        else
            print_error "未找到 rename_script_v2.sh"
        fi
        echo ""

        # Agent 2: 技术指标组A (551)
        print_info "【Agent 2】执行: 技术指标组A - MACD/RSI/ADX (551 文件)"
        if [ -f "rename_scripts.sh" ]; then
            bash rename_scripts.sh
            show_progress 551 "MACD/RSI/ADX"
        else
            print_error "未找到 rename_scripts.sh"
        fi
        echo ""

        # Agent 3: 技术指标组B (399)
        print_info "【Agent 3】执行: 技术指标组B - 布林带/ATR/CCI/KDJ (399 文件)"
        if [ -f "rename_all_group_b.sh" ]; then
            bash rename_all_group_b.sh
            show_progress 399 "布林带/ATR/CCI/KDJ"
        else
            print_error "未找到 rename_all_group_b.sh"
        fi
        echo ""

        # Agent 4: 技术指标组C (882)
        print_info "【Agent 4】执行: 技术指标组C - 成交量/趋势/综合 (882 文件)"
        if [ -f "rename_all_master.sh" ]; then
            bash rename_all_master.sh
            show_progress 882 "成交量/趋势/综合"
        else
            print_error "未找到 rename_all_master.sh"
        fi
        echo ""

        # Agent 5: 交易方法组A (175)
        print_info "【Agent 5】执行: 交易方法组A - 高频/网格/套利/马丁 (175 文件)"
        if [ -f "rename-agent5-scripts.sh" ]; then
            bash rename-agent5-scripts.sh
            show_progress 175 "高频/网格/套利/马丁"
        else
            print_error "未找到 rename-agent5-scripts.sh"
        fi
        echo ""

        # Agent 6: 交易方法组B (552)
        print_info "【Agent 6】执行: 交易方法组B - 反转/突破/定投/形态/斐波 (552 文件)"
        if [ -f "rename_group_b.sh" ]; then
            bash rename_group_b.sh
            show_progress 552 "反转/突破/定投/形态/斐波"
        else
            print_error "未找到 rename_group_b.sh"
        fi
        echo ""

        # Agent 7: 资产与支持材料 (795)
        print_info "【Agent 7】执行: 资产与支持材料 (795 文件)"
        if [ -f "run_all_renaming.sh" ]; then
            bash run_all_renaming.sh
            show_progress 795 "资产/教学/API/其他"
        else
            print_error "未找到 run_all_renaming.sh"
        fi
        echo ""

        print_success "所有文件重命名完成！"
        ;;

    2)
        print_info "模式 2: 分组执行"
        echo ""

        agents=(
            "rename_script_v2.sh:Agent 1 - 移动平均线 (2,453):2453"
            "rename_scripts.sh:Agent 2 - MACD/RSI/ADX (551):551"
            "rename_all_group_b.sh:Agent 3 - 布林带/ATR/CCI/KDJ (399):399"
            "rename_all_master.sh:Agent 4 - 成交量/趋势/综合 (882):882"
            "rename-agent5-scripts.sh:Agent 5 - 高频/网格/套利/马丁 (175):175"
            "rename_group_b.sh:Agent 6 - 反转/突破/定投/形态/斐波 (552):552"
            "run_all_renaming.sh:Agent 7 - 资产/教学/API/其他 (795):795"
        )

        for agent in "${agents[@]}"; do
            IFS=':' read -r script name count <<< "$agent"
            echo "----------------------------------------"
            print_info "准备执行: ${name}"
            read -p "是否执行此组? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                if [ -f "$script" ]; then
                    bash "$script"
                    show_progress "$count" "$name"
                    print_success "完成: ${name}"
                else
                    print_error "未找到脚本: $script"
                fi
            else
                print_warning "跳过: ${name}"
            fi
            echo ""
        done

        print_success "分组执行完成！"
        ;;

    3)
        print_info "模式 3: 按目录执行"
        print_warning "此模式需要手动执行各目录的脚本"
        echo ""
        echo "脚本位置:"
        echo "  - Agent 1: rename_script_v2.sh"
        echo "  - Agent 2: rename_scripts.sh"
        echo "  - Agent 3: rename_bollinger.sh, rename_atr.sh, rename_cci.sh, rename_kdj.sh"
        echo "  - Agent 4: rename_script_09.sh, rename_script_10.sh, rename_script_11.sh"
        echo "  - Agent 5: rename-agent5-scripts.sh"
        echo "  - Agent 6: rename_group_b.sh"
        echo "  - Agent 7: rename_bitcoin.sh, rename_gold.sh, rename_ethereum.sh, ..."
        echo ""
        print_info "请根据需要手动执行各个脚本"
        ;;

    4)
        print_info "模式 4: 仅预览"
        echo ""
        echo "将要执行的脚本列表:"
        echo "  [1] rename_script_v2.sh         - 2,453 files (移动平均线)"
        echo "  [2] rename_scripts.sh           - 551 files (MACD/RSI/ADX)"
        echo "  [3] rename_all_group_b.sh       - 399 files (布林带/ATR/CCI/KDJ)"
        echo "  [4] rename_all_master.sh        - 882 files (成交量/趋势/综合)"
        echo "  [5] rename-agent5-scripts.sh    - 175 files (高频/网格/套利/马丁)"
        echo "  [6] rename_group_b.sh           - 552 files (反转/突破/定投/形态/斐波)"
        echo "  [7] run_all_renaming.sh         - 795 files (资产/教学/API/其他)"
        echo ""
        echo "总计: 5,807 个文件将被重命名"
        echo ""
        print_info "预览完成，未执行任何操作"
        ;;

    *)
        print_error "无效的选项"
        exit 1
        ;;
esac

echo ""
echo "============================================================================"
print_success "重命名任务完成！"
echo "============================================================================"
echo ""
print_info "下一步操作建议:"
echo "  1. 检查重命名结果: git status"
echo "  2. 查看具体变更: git diff --name-status"
echo "  3. 验证文件数量: 在各目录中执行 ls *.md | wc -l"
echo "  4. 提交更改: git add . && git commit -m '标准化策略文件命名'"
echo ""
