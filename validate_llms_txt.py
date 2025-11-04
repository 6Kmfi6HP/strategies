#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证 llms.txt 文件的脚本
检查格式、链接有效性和完整性
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple
from urllib.parse import urlparse


# 配置
ROOT_DIR = Path(__file__).parent
REPO_URL = "https://raw.githubusercontent.com/6Kmfi6HP/strategies/master"

# 预期的分类目录
EXPECTED_CATEGORIES = [
    "01-技术指标-移动平均线",
    "02-技术指标-MACD",
    "03-技术指标-RSI",
    "04-技术指标-ADX",
    "05-技术指标-布林带",
    "06-技术指标-ATR",
    "07-技术指标-CCI",
    "08-技术指标-KDJ",
    "09-技术指标-成交量",
    "10-技术指标-趋势指标",
    "11-技术指标-综合指标",
    "12-交易方法-高频交易",
    "13-交易方法-网格交易",
    "14-交易方法-套利",
    "15-交易方法-马丁格尔",
    "16-交易方法-反转策略",
    "17-交易方法-突破策略",
    "18-交易方法-定投策略",
    "19-交易方法-形态识别",
    "20-交易方法-斐波那契",
    "21-资产类型-比特币",
    "22-资产类型-黄金",
    "23-资产类型-以太坊",
    "24-教学文档",
    "25-API工具",
    "26-其他策略",
]


class ValidationResult:
    """验证结果类"""
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []
        self.stats: Dict[str, int] = {}

    def add_error(self, msg: str):
        self.errors.append(f"[ERROR] {msg}")

    def add_warning(self, msg: str):
        self.warnings.append(f"[WARNING] {msg}")

    def add_info(self, msg: str):
        self.info.append(f"[INFO] {msg}")

    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def print_summary(self):
        """打印验证摘要"""
        print("\n" + "="*60)
        print("验证摘要")
        print("="*60)

        if self.info:
            print("\n信息:")
            for msg in self.info:
                print(f"  {msg}")

        if self.warnings:
            print(f"\n警告 ({len(self.warnings)}):")
            for msg in self.warnings[:10]:  # 只显示前10个
                print(f"  {msg}")
            if len(self.warnings) > 10:
                print(f"  ... 还有 {len(self.warnings) - 10} 个警告")

        if self.errors:
            print(f"\n错误 ({len(self.errors)}):")
            for msg in self.errors[:10]:  # 只显示前10个
                print(f"  {msg}")
            if len(self.errors) > 10:
                print(f"  ... 还有 {len(self.errors) - 10} 个错误")

        print("\n" + "="*60)
        if self.is_valid():
            print("验证通过！所有 llms.txt 文件格式正确。")
        else:
            print(f"验证失败！发现 {len(self.errors)} 个错误。")
        print("="*60 + "\n")


def validate_markdown_link(line: str) -> Tuple[bool, str, str]:
    """
    验证 Markdown 链接格式
    返回: (是否有效, 链接文本, URL)
    """
    # 匹配 Markdown 链接格式: [文本](URL)
    pattern = r'\- \[([^\]]*)\]\(([^)]+)\)(?:: (.+))?$'
    match = re.match(pattern, line.strip())

    if not match:
        return False, "", ""

    link_text = match.group(1)
    url = match.group(2)

    return True, link_text, url


def validate_url_format(url: str) -> bool:
    """
    验证 URL 格式是否正确
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False


def validate_root_llms_txt(result: ValidationResult):
    """
    验证根目录的 llms.txt 文件
    """
    print("验证根目录 llms.txt...")

    root_file = ROOT_DIR / "llms.txt"

    if not root_file.exists():
        result.add_error("根目录 llms.txt 文件不存在")
        return

    with open(root_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # 检查基本结构
    if not content.startswith('# '):
        result.add_error("根目录 llms.txt 缺少 H1 标题")

    if '>' not in content[:200]:
        result.add_warning("根目录 llms.txt 可能缺少摘要引用")

    # 检查是否包含所有分类的链接
    missing_categories = []
    for category in EXPECTED_CATEGORIES:
        display_name = category.split('-', 1)[1]
        if display_name not in content:
            missing_categories.append(category)

    if missing_categories:
        result.add_error(f"根目录 llms.txt 缺少以下分类的链接: {', '.join(missing_categories)}")

    # 检查 Optional 部分
    if "## Optional" not in content:
        result.add_warning("根目录 llms.txt 没有 Optional 部分")

    # 统计链接数量
    link_count = content.count('](')
    result.add_info(f"根目录 llms.txt 包含 {link_count} 个链接")

    print(f"  已验证根目录 llms.txt ({link_count} 个链接)")


def validate_category_llms_txt(category: str, result: ValidationResult):
    """
    验证分类目录的 llms.txt 文件
    """
    category_path = ROOT_DIR / category
    llms_file = category_path / "llms.txt"

    if not llms_file.exists():
        result.add_error(f"{category}: llms.txt 文件不存在")
        return

    with open(llms_file, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # 检查基本结构
    if not content.startswith('# '):
        result.add_error(f"{category}: 缺少 H1 标题")

    if '>' not in content[:200]:
        result.add_warning(f"{category}: 可能缺少摘要引用")

    if "## 策略列表" not in content:
        result.add_error(f"{category}: 缺少 '## 策略列表' 部分")

    # 统计链接
    link_count = 0
    main_list_count = 0
    optional_count = 0
    invalid_links = []

    in_optional = False
    for i, line in enumerate(lines, 1):
        if line.strip() == "## Optional":
            in_optional = True
            continue

        if line.strip().startswith('- ['):
            link_count += 1

            # 验证链接格式
            is_valid, link_text, url = validate_markdown_link(line)

            if not is_valid:
                invalid_links.append(f"第 {i} 行: 链接格式无效")
                continue

            # 检查链接文本不为空
            if not link_text:
                invalid_links.append(f"第 {i} 行: 链接文本为空")

            # 验证 URL 格式
            if not validate_url_format(url):
                invalid_links.append(f"第 {i} 行: URL 格式无效")

            # 检查 URL 是否指向正确的仓库
            if not url.startswith(REPO_URL):
                invalid_links.append(f"第 {i} 行: URL 不指向正确的仓库")

            if in_optional:
                optional_count += 1
            else:
                main_list_count += 1

    if invalid_links:
        for error in invalid_links[:5]:  # 只显示前5个错误链接
            result.add_error(f"{category}: {error}")
        if len(invalid_links) > 5:
            result.add_error(f"{category}: 还有 {len(invalid_links) - 5} 个无效链接")

    # 统计信息
    result.add_info(f"{category}: {link_count} 个策略 (主列表: {main_list_count}, Optional: {optional_count})")

    # 如果文件超过100个策略但没有Optional部分
    if link_count > 100 and optional_count == 0:
        result.add_warning(f"{category}: 包含 {link_count} 个策略但没有 Optional 部分")

    return link_count


def main():
    """
    主函数：验证所有 llms.txt 文件
    """
    import sys
    # 设置输出编码为 UTF-8
    if sys.platform == "win32":
        import codecs
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

    print("开始验证 llms.txt 文件...\n")

    result = ValidationResult()

    # 1. 验证根目录 llms.txt
    validate_root_llms_txt(result)
    print()

    # 2. 验证所有分类目录的 llms.txt
    print("验证分类目录 llms.txt...\n")

    total_strategies = 0
    for category in EXPECTED_CATEGORIES:
        count = validate_category_llms_txt(category, result)
        if count:
            total_strategies += count

    # 3. 打印摘要
    result.add_info(f"总计: {total_strategies} 个策略链接")
    result.add_info(f"验证了 {len(EXPECTED_CATEGORIES)} 个分类目录 + 1 个根目录")

    result.print_summary()

    # 返回退出码
    return 0 if result.is_valid() else 1


if __name__ == "__main__":
    exit(main())
