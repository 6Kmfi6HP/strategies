# llms.txt 实施指南

本文档说明如何使用和维护策略库的 llms.txt 索引系统。

## 📁 文件结构

```
strategies/
├── llms.txt                          # 根目录索引（导航到所有分类）
├── generate_llms_txt.py              # 自动生成脚本
├── validate_llms_txt.py              # 验证脚本
├── 01-技术指标-移动平均线/
│   └── llms.txt                      # 移动平均线策略索引（2,453个策略）
├── 02-技术指标-MACD/
│   └── llms.txt                      # MACD策略索引（11个策略）
├── ... (其他24个分类目录)
└── 26-其他策略/
    └── llms.txt                      # 其他策略索引（617个策略）
```

## 🎯 什么是 llms.txt？

llms.txt 是一个标准化的 Markdown 格式文件，专门为 LLM（大语言模型）设计，用于：

- **快速导航**：帮助 AI 助手快速理解和检索策略库内容
- **结构化索引**：提供清晰的分层结构（根目录 → 分类 → 具体策略）
- **直接访问**：使用 GitHub raw 链接直接访问策略文档内容

符合 [llmstxt.org](https://llmstxt.org/) 官方规范。

## 📊 当前统计

- **总策略数**：5,807 个
- **分类数量**：26 个
- **llms.txt 文件**：27 个（1个根 + 26个分类）
- **仓库地址**：https://github.com/6Kmfi6HP/strategies

## 🔗 访问方式

### 1. 根目录入口

访问主索引：
```
https://raw.githubusercontent.com/6Kmfi6HP/strategies/master/llms.txt
```

### 2. 分类索引

访问特定分类（URL编码后的目录名）：
```
https://raw.githubusercontent.com/6Kmfi6HP/strategies/master/01-%E6%8A%80%E6%9C%AF%E6%8C%87%E6%A0%87-%E7%A7%BB%E5%8A%A8%E5%B9%B3%E5%9D%87%E7%BA%BF/llms.txt
```

### 3. 具体策略

每个策略的直接链接格式：
```
https://raw.githubusercontent.com/6Kmfi6HP/strategies/master/[目录名]/[文件名].md
```

## 🛠️ 使用脚本

### 生成 llms.txt 文件

当添加新策略或修改目录结构后，运行：

```bash
python generate_llms_txt.py
```

脚本会：
- 扫描所有26个分类目录
- 提取所有 .md 策略文件
- 生成符合规范的 llms.txt 文件
- 自动处理大目录（>100个文件时使用 Optional 部分）

### 验证 llms.txt 文件

检查所有 llms.txt 文件的完整性和格式：

```bash
python validate_llms_txt.py
```

验证内容包括：
- ✅ 文件是否存在
- ✅ 标题和摘要格式
- ✅ Markdown 链接格式
- ✅ URL 有效性
- ✅ 链接数量统计

## 📝 llms.txt 格式说明

### 根目录 llms.txt

```markdown
# 📈 量化交易策略库

> 综合性量化交易策略文档库，涵盖 5,807 个策略...

本策略库包含：
- **技术栈**：PineScript、JavaScript、Python
- **26个专业分类**：技术指标、交易方法、资产类型等
...

## 技术指标类（11个分类，4,285个策略）

- [技术指标-移动平均线](URL): 描述 (数量)
- [技术指标-MACD](URL): 描述 (数量)
...

## Optional

- [完整README](URL): 说明文档
- [分类说明](URL): 分类体系
```

### 分类目录 llms.txt

```markdown
# 技术指标-移动平均线

> EMA、SMA、VWMA、Hull MA、ALMA、KAMA等移动平均线策略

本分类包含 2453 个量化交易策略文档。

## 策略列表

- [策略1](URL): 策略描述
- [策略2](URL): 策略描述
... (前100个，带完整描述)

## Optional

- [策略101](URL)
- [策略102](URL)
... (100个以后，仅链接文本)
```

## 🎨 设计特点

### 1. 分层结构

- **第一层**：根目录 llms.txt（总导航）
- **第二层**：26个分类目录 llms.txt（分类索引）
- **第三层**：5,807个具体策略文档

### 2. 智能分组

大目录（>100个文件）自动分为：
- **主列表**：前100个策略，带完整描述和标签
- **Optional 部分**：剩余策略，仅显示标题

好处：
- 保持主列表精简，方便 LLM 快速浏览
- Optional 部分提供完整覆盖
- 不丢失任何内容

### 3. 描述增强

每个策略链接包含：
- **中文名称**：策略的中文描述
- **GitHub raw URL**：直接访问策略文档
- **智能标签**：自动识别关键特征（交叉信号、趋势跟踪、突破策略等）

示例：
```markdown
- [MACD双转换零滞后交易策略](URL): MACD双转换... - 交叉信号, 趋势跟踪, 高频交易
```

## 🔄 更新维护

### 添加新策略后

1. 将新的 .md 文件放入相应分类目录
2. 运行生成脚本：
   ```bash
   python generate_llms_txt.py
   ```
3. 验证生成结果：
   ```bash
   python validate_llms_txt.py
   ```
4. 提交到 Git

### 修改仓库配置

如果仓库 URL 更改，修改 `generate_llms_txt.py` 中的：
```python
REPO_URL = "https://raw.githubusercontent.com/6Kmfi6HP/strategies/master"
```

### 新增分类目录

在 `generate_llms_txt.py` 的 `CATEGORIES` 字典中添加新分类：
```python
CATEGORIES = {
    # ... 现有分类 ...
    "27-新分类": {"count": 0, "desc": "分类描述", "type": "类型"},
}
```

## 📚 相关资源

- **llms.txt 官方规范**：https://llmstxt.org/
- **GitHub 仓库**：https://github.com/6Kmfi6HP/strategies
- **FMZ 量化平台**：https://www.fmz.com/

## 💡 最佳实践

### 对于 LLM/AI 助手

1. **首先访问根目录 llms.txt** 了解整体结构
2. **根据需求选择分类** 进入相应的分类索引
3. **查看具体策略** 通过 raw 链接直接访问策略文档
4. **利用 Optional 部分** 获取完整策略列表

### 对于开发者

1. **定期运行验证脚本** 确保索引完整性
2. **添加策略后重新生成** 保持索引最新
3. **遵循命名规范** 便于自动提取策略信息
4. **合理组织分类** 避免单个目录过大

## ❓ 常见问题

### Q: 为什么使用 GitHub raw URL？

A: GitHub raw URL 提供文件的纯文本内容，LLM 可以直接读取和分析，无需处理 HTML。

### Q: Optional 部分是否会被忽略？

A: 不会。Optional 是 llms.txt 规范的一部分，表示"可选但完整"的内容。LLM 可以根据需要访问这些链接。

### Q: 如何处理中文文件名的 URL 编码？

A: 脚本自动使用 `urllib.parse.quote()` 处理中文字符编码，生成有效的 URL。

### Q: 可以手动编辑 llms.txt 吗？

A: 可以，但不推荐。手动编辑容易出错，建议修改生成脚本后重新生成。

## 📞 支持

如有问题或建议，请：
- 提交 GitHub Issue
- 查看官方文档：https://llmstxt.org/
- 参考本项目的 README.md

---

**生成时间**：2025-11-05
**脚本版本**：1.0
**策略总数**：5,807
