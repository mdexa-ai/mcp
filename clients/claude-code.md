# Claude Code

Tested with Claude Code. Other clients are not listed here until they have passed the same test; for them, follow the client's own documentation.

Add the server (no account needed for light use):

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp
```

With a free-account key (higher limits, `batch_check`), keep the key in an environment variable:

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp --header "Authorization: Bearer $MDEXA_API_KEY"
```

Then ask, for example: "Is MIMIC-IV in Mdexa?" or "Can I use the AlphaFold 3 weights commercially? Use Mdexa and quote the source."

# Claude Code（中文）

已用 Claude Code 实测。其他客户端在通过同样的实测之前不列在这里，请以客户端自己的文档为准。

添加服务（轻量使用无需账号）：

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp
```

使用免费账号的 Key（更高额度、可用 `batch_check`），Key 放在环境变量里：

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp --header "Authorization: Bearer $MDEXA_API_KEY"
```

然后可以直接问，例如：「MIMIC-IV 在 Mdexa 里吗？」「AlphaFold 3 的权重能商用吗？用 Mdexa 查并引用来源。」
