# 交互式示例

[English](../examples.md) | 简体中文

仓库包含三个可执行 notebook，用于演示重点 API；它们不能替代固定来源特性覆盖清单，
也不代表完整 DTD 符合性或 ChemDraw 兼容性验证。

- [01 — 核心工作流](../../examples/notebooks/01_core_workflow.ipynb)：解析、导航、修改、
  创建/移除对象，并往返验证引用。
- [02 — 文档特性](../../examples/notebooks/02_document_features.ipynb)：局部资源、富文本、
  图形、反应引用、不规则类型字段和词法 Spectrum 数据。
- [03 — 验证与保留](../../examples/notebooks/03_validation_and_preservation.ipynb)：未知 XML
  保留、结构化验证结果及外部实体安全处理。

## 安装与运行

在仓库检出目录安装可选 notebook 工具：

```bash
uv sync --extra notebooks
```

将已执行副本写入新目录，不修改仓库中的 notebook：

```bash
notebook_output="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-notebooks.XXXXXX")"
uv run --no-sync python -m tools.run_notebooks --output-dir "$notebook_output"
```

CI 和本地开发可执行 notebook 并检查已保存输出是否仍然匹配：

```bash
uv run --no-sync python -m tools.run_notebooks --check
```

审查 notebook 修改后，可用 `uv run --no-sync python -m tools.run_notebooks --update`
刷新仓库中的执行输出。运行器会先执行全部 notebook，再开始更新源文件；每个文件通过
原子替换写入，但后续多文件写入若遇到文件系统错误，仍可能只完成部分更新。输出副本模式
不会覆盖已有路径。

运行器为当前 Python 解释器临时创建 kernel，并为每个 notebook 使用新的临时工作目录。
这可以避免相对路径产物写入检出目录，但不是 Python 代码的安全沙箱。请将 notebook
视为可信代码，不要因为文件位于仓库内就执行未经审查的 notebook。交互式运行时，在安装
`notebooks` extra 后，用支持 Jupyter 的编辑器打开文件并选择当前检出目录的 Python 环境。

仓库还包含七个供人工检查的持久 CDXML 文件。打开顺序、来源说明和兼容性边界见
[人工检查样例说明](../../examples/render_samples/README.zh-CN.md)。用户报告称，其中六个文件在 Windows
ChemDraw Professional 25.5.0.5789 中正常打开并渲染；较早的曲线载荷出现 “vector too long”。曲线探针
随后已更新，等待复验。该报告没有截图或可独立复现的应用产物，不构成独立 ChemDraw 验证。
