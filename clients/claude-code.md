# Claude Code

Tested with Claude Code. Other clients are not listed here until they have passed the same test; for them, follow the client's own documentation.

Every database call needs an API key; a free account is enough (https://mdexa.com/signup/). Replace `YOUR_KEY` with your key and add the server:

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp --header "Authorization: Bearer YOUR_KEY"
```

Then ask, for example: "Is MIMIC-IV in Mdexa?" or "Can I use the AlphaFold 3 weights commercially? Use Mdexa and quote the source."

# Claude Code（中文）

已用 Claude Code 实测。其他客户端在通过同样的实测之前不列在这里，请以客户端自己的文档为准。

每次数据库调用都需要 API 密钥，免费账号即可（https://mdexa.com/signup/）。把命令里的 `YOUR_KEY` 换成你的 Key，再添加服务：

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp --header "Authorization: Bearer YOUR_KEY"
```

然后可以直接问，例如：「MIMIC-IV 在 Mdexa 里吗？」「AlphaFold 3 的权重能商用吗？用 Mdexa 查并引用来源。」
