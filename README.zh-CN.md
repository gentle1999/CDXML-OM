# CDXML-OM

[English](README.md) | 简体中文

[![Python ≥3.11](https://img.shields.io/badge/Python-%E2%89%A53.11-blue)](pyproject.toml) [![MIT License](https://img.shields.io/badge/License-MIT-blue)](LICENSE) [![Single-source version](https://img.shields.io/badge/Version-single--source%20configuration-1f6feb)](src/cdxml_om/_version.py) [![Typed package](https://img.shields.io/badge/Typing-py.typed-blue)](src/cdxml_om/py.typed) [![Strict type checks](https://img.shields.io/badge/Types-Pyright%20%2B%20mypy%20strict-8a2be2)](pyproject.toml)

[![Ruff lint and format](https://img.shields.io/badge/Ruff-lint%20%2B%20format%20configured-46a2f1)](pyproject.toml) [![Pytest suite](https://img.shields.io/badge/Tests-pytest%20configured-0a9edc)](tests/) [![CI and releases configured](https://img.shields.io/badge/CI%20%2B%20release-GitHub%20Actions%20configured-lightgrey)](.github/workflows/release.yml) [![Generated static models](https://img.shields.io/badge/Models-53%20static%20wrappers-2ea44f)](docs/architecture.md) [![CDXML XML model](https://img.shields.io/badge/XML-lxml%20tree%20preservation-00599c)](docs/compatibility.md)

[![Pinned DTD scope](https://img.shields.io/badge/Pinned%20DTD-53%20elements%20%2F%20762%20pairs-2ea44f)](docs/feature-support.md) [![PCDATA and SDK extension scope](https://img.shields.io/badge/PCDATA%20%2B%20SDK-2%2F2%20%2B%2023%2F23%20round--trip-2ea44f)](docs/feature-support.md) [![Bilingual documentation](https://img.shields.io/badge/Docs-English%20%2B%20Simplified%20Chinese-blue)](docs/index.md) [![Runtime dependencies](https://img.shields.io/badge/Runtime-lxml%20only%20%2F%20no%20RDKit-blue)](pyproject.toml) [![ChemDraw application verification](https://img.shields.io/badge/ChemDraw%20app%20verification-none-lightgrey)](docs/feature-support.md)

这 15 个徽章描述静态配置和已测来源范围，不代表实时 CI 状态、包索引发布状态或下载统计。固定来源范围内的测试计数
不代表完整 DTD 文法符合性，也不代表通过了 ChemDraw 应用验证。

CDXML-OM 是用于读取、编辑、验证和写出 ChemDraw CDXML 文档的类型化、schema
驱动 Python 对象模型。生成的运行时覆盖固定版本 Revvity DTD 中的全部 53
种元素和 762 组“元素/属性”定义，并单独报告 SDK 文档记录的 XML 扩展。

## 功能

- 根据经过审查的规范 schema 生成类型化模型、字段、枚举和实时子元素集合。
- 保留完整 `lxml` 树，包括未知标签、属性及顺序；每个底层 XML 元素对应稳定的
  Python wrapper 身份。
- 安全解析本地 XML，不联网，也不加载外部实体。
- 特性测试覆盖类型化读取、写入、修改及序列化/重新加载。ChemDraw 应用验证是
  独立声明；目前没有独立可复核的应用验证产物，以下用户报告不计作验证。

用户报告称，[人工样例集](examples/render_samples/README.zh-CN.md)中的六个文件曾在 Windows
ChemDraw Professional 25.5.0.5789 中正常打开并渲染；较早的曲线载荷出现 “vector too long”。曲线候选
之后已更新，等待复验。没有截图或独立应用验证产物，因此该报告不改变 `ChemDrawVerified=0` 的边界。

## 从源码检出目录安装

仓库当前版本是开发版；以下命令从检出目录安装，不假定包索引上已有正式发行版。

```bash
# 在仓库根目录运行；安装项目和运行时依赖。
uv sync

# 或在仓库根目录用 pip 安装可编辑包：
python -m pip install -e .
```

需要 Python 3.11 或更新版本。唯一必需的运行时依赖是 `lxml`；无需安装 RDKit。

## 版本与发布

唯一版本来源是 `src/cdxml_om/_version.py`。Hatchling 直接读取其中的
`__version__` 赋值，不导入运行时包；`cdxml_om.__version__` 和构建产物元数据都取自该值。
发布时只修改这一处，然后运行 `uv lock`、`uv sync` 和
`uv run python tools/check_package.py`，再构建或发布。uv 缓存键包含版本文件，修改版本后
会刷新 editable 安装元数据。不要在 `pyproject.toml` 或 `__init__.py` 中另设版本字面值。
按标签触发的构建与发布流程见[发布指南](docs/zh-CN/releasing.md)。

## 示例

此示例从空文档构造并修改一个小型结构，执行验证、写出、重新加载，并检查键的
端点引用指向重新加载后的节点 wrapper：

```python
from cdxml_om import CDXMLDocument

document = CDXMLDocument.from_string("<CDXML/>")
page = document.pages.create()
fragment = page.fragments.create()
carbon = fragment.nodes.create(element=6, position=(0.0, 0.0))
oxygen = fragment.nodes.create(element=8, position=(10.0, 0.0))
bond = fragment.bonds.create(begin=carbon, end=oxygen, order=1)

bond.order = 2
oxygen.charge = -1
report = document.validate()
assert report.is_valid, report.errors

document.to_file("example.cdxml")
reloaded = CDXMLDocument.from_file("example.cdxml")
reloaded_fragment = reloaded.pages[0].fragments[0]
reloaded_bond = reloaded_fragment.bonds[0]
assert reloaded_bond.begin is reloaded_fragment.nodes[0]
assert reloaded_bond.end is reloaded_fragment.nodes[1]
assert reloaded.validate().is_valid
```

验证器报告已知的 schema 约束，不负责化学正确性，也不等同于完整 DTD 文法验证。
移除对象不会级联删除或改写它的引用。精确支持范围见
[特性支持说明](docs/zh-CN/feature-support.md)。此代码用于演示对象 API，不是页面排版或 ChemDraw 渲染模板；
独立的视觉检查候选见[人工样例](examples/render_samples/README.zh-CN.md)。

## 交互式 notebook

使用 `uv sync --extra notebooks` 安装可选 notebook 工具。[notebook 指南](docs/zh-CN/examples.md)
链接了三个双语示例，覆盖核心编辑、更多文档特性、验证和内容保留。用以下命令执行并检查
已保存输出：

```bash
uv run --no-sync python -m tools.run_notebooks --check
```

运行器使用临时 kernel 和工作目录，但不是安全沙箱；只执行已审查且可信的 notebook。

## 开发

安装开发工具并运行 schema、代码风格、类型和测试检查：

```bash
uv sync --extra dev
uv run python -m tools.schema_compiler check
uv run python -m tools.schema_compiler build
uv run python -m tools.schema_compiler coverage
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run mypy
uv run pytest
uv run --no-sync python -m tools.run_notebooks --check
```

文档导航见[文档目录](docs/zh-CN/index.md)。项目采用
[MIT License](LICENSE)。
