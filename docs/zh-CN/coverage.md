# 覆盖率计量方法

[English](../coverage.md) | 简体中文

Schema 编译器的 `coverage` 命令将规范生成物与固定 Revvity DTD 比较，其 SHA-256 为
`5311978e514ffe154108540c3634c314dc66031a4f3c877a681fc6dca8e128c2`。精确分母为 53 个元素、
762 组“所属元素/属性”组合，以及包含字符数据的两个 DTD 元素（`s`、`spectrum`）。覆盖率
报告由静态开发工具生成；解析文档时不会加载 DTD、SDK 来源目录、YAML 或覆盖率工具。

覆盖率各阶段分别计量：

- `known`：该项存在于固定 DTD 清单中，不代表其语义或 ChemDraw 行为已知。
- `canonical_*_known`：存在经审查的规范对象/属性映射。
- `implemented`：生成的 wrapper 描述符连接到运行时 codec；仅保留不透明 XML 不算实现。
- `typed`：静态注册表中存在准确的生成模型/描述符。
- `test_case_declared`：独立特性目录将该项关联到明确命名的断言。
- `tested` 和 `round_trip_verified`：所有关联 pytest 用例均在当前、源码绑定的测试运行中通过。
  失败、跳过、未收集或已过期的用例均不计入。
- `chemdraw_verified`：需要独立应用产物和观察记录；测试语料往返不等于 ChemDraw 互操作。

DTD 分母和 SDK 扩展分母分开统计。扩展集合包含 20 组 DTD 之外、由 SDK 精确记录的 XML
元素/属性组合，以及 3 个 Curve 大小写别名；别名不增加 DTD 属性对分母。两个字符数据
特性（`s` 和 `spectrum`）单独计数。仅生成清单报告只能证明映射/实现情况和声明的测试
配方，不能证明测试实际通过；需提供新鲜的源码绑定运行证据才能计入 tested 和 round-trip。
SDK 目录同样将类型化特性用例与原始属性保留用例分开统计。

截至 **2026-10-05** 的已接受、源码绑定报告显示：53/53 个元素、762/762 组 DTD 属性、
2/2 个 PCDATA 特性和 23/23 组 SDK 扩展已实现、类型化、通过测试并经往返验证。该结果
只适用于固定来源范围。ChemDraw 验证仍为 0；需要另外提供真实应用产物和观察记录。

## 生成报告

```sh
uv run python -m tools.schema_compiler coverage --format text
uv run python -m tools.schema_compiler coverage --format json
```

要运行特性目录并采集 JUnit 结果，使用仓库外的新输出路径：

```sh
evidence_dir="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-feature-run.XXXXXX")"
uv run python -m tools.schema_compiler test-features \
  --run-evidence "$evidence_dir/feature-run.json" \
  --junitxml "$evidence_dir/feature-run.xml" -- tests/coverage
uv run python -m tools.schema_compiler coverage \
  --test-run "$evidence_dir/feature-run.json" --format json
```

Runner 在 pytest 前后计算指纹，将运行证据 sidecar 绑定到新生成的 JUnit 摘要；不会复用
已有 JUnit。修改运行时、schema、特性配方、fixture、辅助代码或测试后，旧运行即失效。
特性目录格式见
[`schema/coverage/feature-cases.schema.json`](../../schema/coverage/feature-cases.schema.json)；
相邻的 `report.schema.json` 和 `test-run.schema.json` 描述报告与运行证据格式。

报告还列出 DTD 子内容模型树，但不声称完整严格文法验证。固定来源中 `altgroup` 内容模型
包含未声明的子标签 `bracket`；若没有其他来源定义它，`<bracket>` 会作为未知元素保留。
`spectrum` 有类型化词法 PCDATA 接口，但未声称数值样本语法。面向使用者的支持范围见
[特性支持](feature-support.md)；更完整的来源事实见
[规范证据基线](specification-baseline.md)。
