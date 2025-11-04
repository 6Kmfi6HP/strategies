#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 llms.txt 文件的自动化脚本
为量化交易策略库创建符合 llmstxt.org 规范的索引文件
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple
from urllib.parse import quote


# 配置
REPO_URL = "https://raw.githubusercontent.com/6Kmfi6HP/strategies/master"
ROOT_DIR = Path(__file__).parent

# 分类信息
CATEGORIES = {
    "01-技术指标-移动平均线": {"count": 2453, "desc": "EMA、SMA、VWMA、Hull MA、ALMA、KAMA等移动平均线策略", "type": "技术指标"},
    "02-技术指标-MACD": {"count": 11, "desc": "MACD、信号线、柱状图指标策略", "type": "技术指标"},
    "03-技术指标-RSI": {"count": 494, "desc": "相对强弱指标、超买超卖策略", "type": "技术指标"},
    "04-技术指标-ADX": {"count": 46, "desc": "平均趋向指标、趋势强度策略", "type": "技术指标"},
    "05-技术指标-布林带": {"count": 198, "desc": "布林通道、波动率策略", "type": "技术指标"},
    "06-技术指标-ATR": {"count": 96, "desc": "真实波幅、止损位策略", "type": "技术指标"},
    "07-技术指标-CCI": {"count": 55, "desc": "顺势指标、超买超卖策略", "type": "技术指标"},
    "08-技术指标-KDJ": {"count": 50, "desc": "随机指标、快慢线策略", "type": "技术指标"},
    "09-技术指标-成交量": {"count": 91, "desc": "VWAP、OBV、MFI、成交量加权策略", "type": "技术指标"},
    "10-技术指标-趋势指标": {"count": 487, "desc": "Supertrend、Ichimoku、Alligator趋势跟踪策略", "type": "技术指标"},
    "11-技术指标-综合指标": {"count": 304, "desc": "多指标组合、综合信号策略", "type": "技术指标"},
    "12-交易方法-高频交易": {"count": 51, "desc": "短周期、高频开仓、套利策略", "type": "交易方法"},
    "13-交易方法-网格交易": {"count": 51, "desc": "等比网格、等差网格、动态网格策略", "type": "交易方法"},
    "14-交易方法-套利": {"count": 45, "desc": "跨市场套利、统计套利、期现套利策略", "type": "交易方法"},
    "15-交易方法-马丁格尔": {"count": 28, "desc": "倍投策略、反向马丁策略", "type": "交易方法"},
    "16-交易方法-反转策略": {"count": 169, "desc": "均值回归、震荡反转策略", "type": "交易方法"},
    "17-交易方法-突破策略": {"count": 294, "desc": "价格突破、通道突破、形态突破策略", "type": "交易方法"},
    "18-交易方法-定投策略": {"count": 18, "desc": "定期定额、动态定投策略", "type": "交易方法"},
    "19-交易方法-形态识别": {"count": 68, "desc": "K线形态、技术形态、价格模式识别策略", "type": "交易方法"},
    "20-交易方法-斐波那契": {"count": 3, "desc": "斐波那契回撤、扩展、时间周期策略", "type": "交易方法"},
    "21-资产类型-比特币": {"count": 22, "desc": "比特币专项策略（高波动、24小时交易、链上数据）", "type": "资产类型"},
    "22-资产类型-黄金": {"count": 14, "desc": "黄金专项策略（避险属性、美元负相关）", "type": "资产类型"},
    "23-资产类型-以太坊": {"count": 3, "desc": "以太坊专项策略（智能合约、Gas费、DeFi生态）", "type": "资产类型"},
    "24-教学文档": {"count": 23, "desc": "量化入门、策略开发教程", "type": "其他"},
    "25-API工具": {"count": 116, "desc": "交易所API、数据接口、工具库", "type": "其他"},
    "26-其他策略": {"count": 617, "desc": "混合策略、实验性策略", "type": "其他"},
}


def extract_strategy_name(filename: str) -> Tuple[str, str]:
    """
    从文件名提取策略名称
    格式: 序号-中文名-英文名.md
    返回: (中文名, 英文名)
    """
    if not filename.endswith('.md'):
        return filename, ""

    name_without_ext = filename[:-3]

    # 按 - 分割
    parts = name_without_ext.split('-')

    if len(parts) < 2:
        return name_without_ext, ""

    # 第一部分是序号，跳过
    parts = parts[1:]

    # 找到第一个全是小写英文字母或包含英文的部分作为英文名的开始
    chinese_parts = []
    english_parts = []
    found_english = False

    for part in parts:
        # 判断是否为英文部分
        # 英文部分特征：全是小写字母，或者包含英文单词
        is_english = False
        if part:
            # 如果这部分包含英文字母且不包含中文字符
            has_chinese = any('\u4e00' <= c <= '\u9fff' for c in part)
            has_english = any(c.isalpha() and ord(c) < 128 for c in part)

            if has_english and not has_chinese:
                is_english = True

            if is_english or found_english:
                found_english = True
                english_parts.append(part)
            else:
                chinese_parts.append(part)

    chinese_name = '-'.join(chinese_parts) if chinese_parts else name_without_ext
    english_name = '-'.join(english_parts) if english_parts else ""

    # 如果中文名为空，使用原始文件名
    if not chinese_name:
        chinese_name = name_without_ext

    return chinese_name, english_name


def get_strategy_description(chinese_name: str, english_name: str, category: str) -> str:
    """
    生成策略描述
    """
    # 提取关键词
    keywords = []

    # 从中文名提取关键词
    if "交叉" in chinese_name or "cross" in english_name.lower():
        keywords.append("交叉信号")
    if "趋势" in chinese_name or "trend" in english_name.lower():
        keywords.append("趋势跟踪")
    if "突破" in chinese_name or "breakout" in english_name.lower():
        keywords.append("突破策略")
    if "反转" in chinese_name or "reversal" in english_name.lower():
        keywords.append("反转交易")
    if "网格" in chinese_name or "grid" in english_name.lower():
        keywords.append("网格交易")
    if "高频" in chinese_name or "high.frequency" in english_name.lower():
        keywords.append("高频交易")
    if "套利" in chinese_name or "arbitrage" in english_name.lower():
        keywords.append("套利")

    if keywords:
        return f"{chinese_name} - {', '.join(keywords)}"
    else:
        return chinese_name


def scan_directory_files(directory: Path) -> List[str]:
    """
    扫描目录下的所有 .md 文件
    """
    if not directory.exists():
        return []

    files = []
    for file in sorted(directory.glob("*.md")):
        if file.name != "README.md":  # 排除 README
            files.append(file.name)

    return files


def generate_category_llms_txt(category_name: str, category_info: Dict, files: List[str]) -> str:
    """
    生成分类目录的 llms.txt 内容
    """
    content = []

    # 标题和描述
    display_name = category_name.split('-', 1)[1] if '-' in category_name else category_name
    content.append(f"# {display_name}\n")
    content.append(f"> {category_info['desc']}\n")
    content.append(f"\n本分类包含 {len(files)} 个量化交易策略文档。")
    content.append(f"每个策略均包含：策略原理、源代码实现、优化方向、风险分析。\n")

    # 策略列表
    content.append("## 策略列表\n")

    # 确定是否需要分组
    max_main_list = 100  # 主列表最多显示100个

    if len(files) <= max_main_list:
        # 全部显示
        for filename in files:
            chinese_name, english_name = extract_strategy_name(filename)
            desc = get_strategy_description(chinese_name, english_name, category_name)

            # 构建 GitHub raw URL
            # URL需要编码中文字符
            encoded_category = quote(category_name)
            encoded_filename = quote(filename)
            url = f"{REPO_URL}/{encoded_category}/{encoded_filename}"

            content.append(f"- [{chinese_name}]({url}): {desc}")
    else:
        # 分为主列表和Optional
        for i, filename in enumerate(files[:max_main_list]):
            chinese_name, english_name = extract_strategy_name(filename)
            desc = get_strategy_description(chinese_name, english_name, category_name)

            encoded_category = quote(category_name)
            encoded_filename = quote(filename)
            url = f"{REPO_URL}/{encoded_category}/{encoded_filename}"

            content.append(f"- [{chinese_name}]({url}): {desc}")

        # Optional 部分
        content.append("\n## Optional\n")
        for filename in files[max_main_list:]:
            chinese_name, english_name = extract_strategy_name(filename)

            encoded_category = quote(category_name)
            encoded_filename = quote(filename)
            url = f"{REPO_URL}/{encoded_category}/{encoded_filename}"

            content.append(f"- [{chinese_name}]({url})")

    return '\n'.join(content)


def generate_root_llms_txt() -> str:
    """
    生成根目录的 llms.txt 内容
    """
    content = []

    # 标题和摘要
    content.append("# 📈 量化交易策略库\n")
    content.append("> 综合性量化交易策略文档库，涵盖 5,807 个策略，包括技术指标、交易方法、资产类型等多个维度\n")

    # 项目说明
    content.append("本策略库包含：\n")
    content.append("- **技术栈**：PineScript、JavaScript、Python、Pine Script v5")
    content.append("- **26个专业分类**：技术指标、交易方法、资产类型、教学文档等")
    content.append("- **完整文档**：每个策略包含原理、源代码、优化方向、风险分析")
    content.append("- **适用对象**：量化交易者、策略开发者、金融研究人员、算法交易学习者\n")

    # 按类型分组
    type_groups = {}
    for cat_name, cat_info in CATEGORIES.items():
        cat_type = cat_info['type']
        if cat_type not in type_groups:
            type_groups[cat_type] = []
        type_groups[cat_type].append((cat_name, cat_info))

    # 技术指标类
    if "技术指标" in type_groups:
        content.append("## 技术指标类（11个分类，4,285个策略）\n")
        content.append("专注于基于技术指标的量化策略，包括趋势类、震荡类、成交量类、综合类指标。\n")

        for cat_name, cat_info in type_groups["技术指标"]:
            display_name = cat_name.split('-', 1)[1]
            encoded_category = quote(cat_name)
            url = f"{REPO_URL}/{encoded_category}/llms.txt"
            content.append(f"- [{display_name}]({url}): {cat_info['desc']} ({cat_info['count']}个策略)")

    # 交易方法类
    if "交易方法" in type_groups:
        content.append("\n## 交易方法类（9个分类，727个策略）\n")
        content.append("基于不同交易理念和执行方式的策略体系。\n")

        for cat_name, cat_info in type_groups["交易方法"]:
            display_name = cat_name.split('-', 1)[1]
            encoded_category = quote(cat_name)
            url = f"{REPO_URL}/{encoded_category}/llms.txt"
            content.append(f"- [{display_name}]({url}): {cat_info['desc']} ({cat_info['count']}个策略)")

    # 资产类型类
    if "资产类型" in type_groups:
        content.append("\n## 资产类型类（3个分类，39个策略）\n")
        content.append("针对特定资产特性优化的专项策略。\n")

        for cat_name, cat_info in type_groups["资产类型"]:
            display_name = cat_name.split('-', 1)[1]
            encoded_category = quote(cat_name)
            url = f"{REPO_URL}/{encoded_category}/llms.txt"
            content.append(f"- [{display_name}]({url}): {cat_info['desc']} ({cat_info['count']}个策略)")

    # 其他类
    if "其他" in type_groups:
        content.append("\n## 其他类（3个分类，756个策略）\n")
        content.append("教学资源、工具集成和综合性策略。\n")

        for cat_name, cat_info in type_groups["其他"]:
            display_name = cat_name.split('-', 1)[1]
            encoded_category = quote(cat_name)
            url = f"{REPO_URL}/{encoded_category}/llms.txt"
            content.append(f"- [{display_name}]({url}): {cat_info['desc']} ({cat_info['count']}个策略)")

    # Optional 部分
    content.append("\n## Optional\n")
    content.append(f"- [完整README]({REPO_URL}/README.md): 详细的使用说明、统计信息和贡献指南")
    content.append(f"- [分类说明文档]({REPO_URL}/{quote('分类说明.md')}): 完整的分类体系和分类原则说明")

    return '\n'.join(content)


def main():
    """
    主函数：生成所有 llms.txt 文件
    """
    import sys
    # 设置输出编码为 UTF-8
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    print("开始生成 llms.txt 文件...\n")

    # 1. 生成根目录 llms.txt
    print("生成根目录 llms.txt...")
    root_content = generate_root_llms_txt()
    root_file = ROOT_DIR / "llms.txt"

    with open(root_file, 'w', encoding='utf-8') as f:
        f.write(root_content)

    print(f"   已创建: {root_file}\n")

    # 2. 生成每个分类目录的 llms.txt
    print("生成分类目录 llms.txt...\n")

    for category_name, category_info in CATEGORIES.items():
        category_path = ROOT_DIR / category_name

        if not category_path.exists():
            print(f"   [!] 目录不存在，跳过: {category_name}")
            continue

        # 扫描文件
        files = scan_directory_files(category_path)

        if not files:
            print(f"   [!] 没有找到策略文件，跳过: {category_name}")
            continue

        # 生成内容
        content = generate_category_llms_txt(category_name, category_info, files)

        # 写入文件
        output_file = category_path / "llms.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"   [OK] {category_name}: {len(files)} 个策略 -> {output_file.name}")

    print(f"\n完成！已生成 27 个 llms.txt 文件（1个根 + 26个分类）")
    print(f"\n统计信息：")
    print(f"   - 根目录: llms.txt")
    print(f"   - 分类目录: 26 个 llms.txt")
    print(f"   - 索引策略总数: 5,807 个")
    print(f"\n使用说明：")
    print(f"   - 根目录 llms.txt 提供了完整的分类导航")
    print(f"   - 每个分类目录的 llms.txt 包含该分类下所有策略的链接")
    print(f"   - 所有链接均使用 GitHub raw URL 格式")


if __name__ == "__main__":
    main()
