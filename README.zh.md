# Mdexa MCP 示例

Other languages: [English](README.md)

通过 MCP 把 Agent 接到 Mdexa 数据库。Mdexa：为 Agent 而生的医学 AI 数据许可核验库，每条结论都附原文证据。

本仓库只放客户端接入示例和示例提问，不含服务端代码。服务地址 `https://mcp.mdexa.com/mcp`（Streamable HTTP），轻量使用不需要账号。

## 接入

Claude Code：

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp
```

接受通用 `mcpServers` 写法的客户端（以客户端文档为准，Mdexa 未逐一测试各客户端）：

```json
{ "mcpServers": { "mdexa": { "url": "https://mcp.mdexa.com/mcp" } } }
```

其他客户端的配置格式由客户端自己决定。Mdexa 只列出真实测试通过的客户端写法，并非所有客户端都接受通用 `mcpServers` 形式，请以客户端文档为准。详见 https://mdexa.com/zh/developers/ 。

免费账号的 Key（更高额度、批量检查）放在 `Authorization: Bearer <key>`。Claude Code 写法：

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp --header "Authorization: Bearer $MDEXA_API_KEY"
```

Key 不要放进仓库或提示词。

## 五条可直接复制的提问

1. AlphaFold 3 的权重能商用吗？（调 `get_card` 取 `alphafold3`：代码 Apache-2.0，权重受限。）
2. AlphaFold 蛋白结构数据库许可宽松，为什么还有风险标记？（`get_license_evidence` 取 `alphafold-db`。）
3. 帮我检查这份数据集清单哪些没收录。（`batch_check`。）
4. MIMIC-IV 在库里吗？（`search_datasets`；如果答案是「未收录」，这就是明确答案。）
5. CBLUE 的数据许可是什么？仓库许可和数据许可分别是什么？（`get_card`。）

## 说明

- 许可宽松但带风险标记，不等于可以放心用；仓库许可不是数据许可；模型的代码许可与权重许可分开记录。
- 记录的是来源页所述内容，不是法律意见。现在不托管数据文件，每条记录链接到原始来源。

## 许可

Apache-2.0，见 [LICENSE](LICENSE)。
