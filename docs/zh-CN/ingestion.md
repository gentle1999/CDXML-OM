# 离线 Schema 来源导入

[English](../ingestion.md) | 简体中文

Schema 导入器将一次明确选定的本地来源转换为待审候选。它不会联网获取内容、执行页面
脚本、更新规范 YAML 或生成运行时代码。候选 JSON 会保留输入路径和 SHA-256 摘要；差分
输出用于证据审查，不是自动应用计划。

```sh
python -m tools.schema_importer import-dtd schema/sources/revvity-CDXML.dtd \
  --output build/revvity-dtd.candidate.json
python -m tools.schema_importer import-sdk path/to/archived-sdk-page.html \
  --output build/node-sdk.candidate.json
python -m tools.schema_importer diff build/node-sdk.candidate.json \
  --output build/node-sdk.diff.json
```

默认输出到标准输出；`--output -` 可显式表示该行为。若目标文件已存在，必须传
`--force`；无论是否传 `--force`，均不允许写入 `schema/canonical/` 下的路径。成功导入或
差分均返回 0，即使差分包含发现项。输入无效、不可读、不安全或格式错误时返回 2，并向
标准错误写出单行结构化 JSON 诊断。差分发现项分为 `added`、`changed`、`missing`；工具
不会裁定哪一来源权威，也不会改写任一来源。

当前差分范围有意受限：检查选定属性是否存在、是否必需、词法默认值、声明类型证据和枚举
选项；检查对象/属性标识符和常量；以及子元素名称清单。不比较完整 DTD 文法、顺序或数量
限制，也不声称完整解释 SDK。能够识别的子对象表格会保留为来源证据，即使没有对应规范
比较项。

## 安全与来源特例

只接受本地路径。DTD 输入必须是 UTF-8。解析前会保守拒绝参数实体声明和引用，并拒绝外部
`SYSTEM`/`PUBLIC` 实体或 DOCTYPE 声明。这会排除可能合成声明或读取外部资源的 DTD 功能；
仓库中的[Revvity DTD 快照](../../schema/sources/revvity-CDXML.dtd)不依赖参数实体。来源
摘要始终针对原始字节计算，早于仅供解析使用的规范化处理。

固定 DTD 含旧式枚举标记 `+`、`-`、`?`（例如 `AS` 属性）。这些标记只在临时输入给 DTD
解析器的字节中进行转义，随后在候选值中恢复。每次仅用于解析的规范化都会记录在候选
文件中；它不会被描述为源文件的修正或 CDX 语义映射。

存档 SDK HTML 在禁用网络、外部 DOCTYPE 和实体加载的模式下解析。工具只读取输入文件
中的表格，不爬取链接，也不执行脚本。SDK 的 object/property 命名空间保持区分：例如带有
`kCDXProp_ColorTable` 的 `Color Table` 清单项会作为 property 保留；CDXML 子元素
`colortable` 不会被赋予 CDX object ID。同理，SDK 类型 `UINT16` 会原样保存，与规范中的
`object_id` 等类型证据比较，但不会静默转换。

导入器识别[SDK 对象清单](https://chemapps.stolaf.edu/iupac/cdx/sdk/AllCDXObjects.htm)
和 [Node 属性表](https://chemapps.stolaf.edu/iupac/cdx/sdk/Node.htm)等页面。这些页面是
证据来源，不是运行时依赖。本地固定 DTD 快照用于可复现导入；上游副本见
[RevVity CDXML DTD](https://static.chemistry.revvitycloud.com/cdxml/CDXML.dtd)。
