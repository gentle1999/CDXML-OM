# 发布流程

发布工作流位于
[`.github/workflows/release.yml`](../../.github/workflows/release.yml)。只有推送匹配
`v*` 的标签才会触发。工作流会验证标签是否严格等于 `v` 加上
[`src/cdxml_om/_version.py`](../../src/cdxml_om/_version.py) 中的规范 PEP 440 版本；带
`+local` 等本地版本后缀会被拒绝。开发版、alpha、beta 和 release candidate 等 PEP 440
预发布版本会被接受，并在 GitHub Release 中标为预发布。

## 一次性发布配置

首次发布前，必须在 PyPI 配置 Trusted Publishing。为 `cdxml-om` 注册待定或现有发布者：

| PyPI 发布者字段 | 值 |
| --- | --- |
| Owner | `gentle1999` |
| Repository | `CDXML-OM` |
| 工作流文件名 | `release.yml` |
| GitHub environment | `pypi` |

如果 PyPI 上尚无该项目，使用 PyPI 的待定发布者流程；首次成功发布前，项目名称不会被保留。
请参阅 PyPI 的[添加发布者说明](https://docs.pypi.org/trusted-publishers/adding-a-publisher/)
和[通过 OIDC 创建项目](https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/)。

在 GitHub 仓库设置中创建 `pypi` environment，将部署限制为匹配 `v*` 的发布标签，并可考虑要求
可信审核者批准。添加适用于 `v*` 的标签规则集，限制发布维护者以外的人员创建、更新或删除标签。
工作流还会检查标签指向的提交已经包含在默认分支历史中。

## 工作流步骤

1. 无发布权限的构建 job 安装锁定的开发环境，运行 Ruff、Pyright、mypy、pytest、schema 检查与
   重建，以及包验证。
2. 它运行固定来源特性用例，生成与当前 JUnit 结果绑定的证据，并将报告作为单独的质量产物上传。
3. 构建唯一一对 wheel 和 source distribution，在隔离运行时环境中对这些确切文件执行 smoke test，
   校验标签和元数据版本，并在 `packages/` 目录之外生成 `SHA256SUMS`。
4. 唯一的 `release-dist` 产物包含这些相同的包文件字节和校验清单。PyPI job 下载并校验该产物，
   通过 OIDC Trusted Publishing 仅发布 `packages/` 中的文件。它只有 `id-token: write` 权限，不会
   checkout 或执行项目代码。
5. 仅在 PyPI 发布成功后，单独的最小权限 job 才会下载并校验同一产物，再用已验证的 wheel、sdist
   和校验清单创建 GitHub Release。它不会重新构建发行文件。

所有第三方 GitHub Actions 都固定到完整 commit SHA。仓库 secrets 中不保存长期有效的 PyPI token。
不会覆盖现有 PyPI 文件或 GitHub Release：`skip-existing` 已关闭，GitHub CLI 也不使用
`--clobber`。

校验清单路径相对于 release bundle 目录。验证 workflow artifact 时，在 bundle 根目录执行：

```sh
sha256sum --check --strict SHA256SUMS
```

GitHub Release 的文件下载是平铺的。如需使用随附清单验证这些文件，请将 wheel 和 sdist 放入
`SHA256SUMS` 旁边的 `packages/` 目录，再从该目录的父目录运行同一命令。

## 本地预检与打标签

先只修改 `_version.py`，写入计划发布的规范版本，然后更新锁文件并运行仓库检查。下面的命令会将构建
写入新的临时目录，并验证工作流将要发布的同一组文件；将示例标签替换为 `_version.py` 中的精确版本：

```sh
uv lock
uv sync --locked --extra dev
uv run --no-sync ruff check .
uv run --no-sync ruff format --check .
uv run --no-sync pyright
uv run --no-sync mypy
uv run --no-sync pytest
uv run --no-sync python -m tools.schema_compiler check
uv run --no-sync python -m tools.schema_compiler build
# 只要求生成产物保持不变；上文所述的 _version.py 和 uv.lock 版本更新是有意修改。
git diff --exit-code -- src/cdxml_om/_generated schema/schema.lock.json

release_dir="$(mktemp -d "${TMPDIR:-/tmp}/cdxml-om-release.XXXXXX")"
mkdir -p "$release_dir/release-bundle/packages"
uv build --no-create-gitignore --out-dir "$release_dir/release-bundle/packages"
uv run --no-sync python tools/check_package.py \
  --dist-dir "$release_dir/release-bundle/packages"
release_tag="v1.2.3"  # 替换为源码中的精确版本。
uv run --no-sync python -m tools.release \
  --tag "$release_tag" \
  --packages-dir "$release_dir/release-bundle/packages" \
  --bundle-dir "$release_dir/release-bundle"
(cd "$release_dir/release-bundle" && sha256sum --check --strict SHA256SUMS)
```

版本修改经审查并合并到默认分支后，创建并推送完全匹配的标签来触发工作流：

```sh
git tag -a v1.2.3 -m "Release v1.2.3"  # 使用 _version.py 中的精确版本。
git push origin v1.2.3
```

版本修改尚未进入默认分支前，不要推送标签。特权 job 使用辅助工具验证后的标签和版本输出，不会把事件
payload 直接插入 shell 命令。

## 失败与重跑

发布前的构建失败可以修复后重跑。PyPI 发布失败后，先检查已发布文件清单：若没有文件上传，可修复原因后
重试；若只上传了部分文件，不要盲目重跑整个工作流，也不要启用 `skip-existing`。请由发布维护者协调部分发布，
通常应通过修正后发布新版本来安全恢复。如果 PyPI 已完整发布但 GitHub Release job 失败，应在同一次
workflow run 中仅重跑失败的 `github-release` job；它会复用已经成功的 PyPI 依赖。PyPI 上传成功后重跑
整个 workflow 会因重复文件而失败，这是预期行为。不要启用覆盖或 clobber。

工作流配置不代表远程发布已经运行。PyPI 发布者注册以及首次发布时的项目注册都由维护者负责。
