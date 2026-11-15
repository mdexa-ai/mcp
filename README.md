# Mdexa MCP examples

Connect an agent to the Mdexa database over MCP. Mdexa is a license-verification database for medical AI datasets and open models, built for agents, with a quoted source behind every verdict.

This repository holds client setup examples and sample prompts only. It contains no server code. The server is hosted at `https://mcp.mdexa.com/mcp` (Streamable HTTP). Light use needs no account.

Other languages: [中文](README.zh.md)

## Connect

Claude Code:

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp
```

Clients that accept the generic `mcpServers` form (check your client; Mdexa has not tested every client):

```json
{ "mcpServers": { "mdexa": { "url": "https://mcp.mdexa.com/mcp" } } }
```

The configuration format of other clients is the client's own. Mdexa lists a setup only for clients that have passed a real test, and the generic `mcpServers` form is not accepted by every client, so check your client's documentation. See https://mdexa.com/developers/ and https://mdexa.com/developers/faq/.

With a free-account key (higher limits, batch checking), send it as `Authorization: Bearer <key>`. In Claude Code:

```bash
claude mcp add --transport http mdexa https://mcp.mdexa.com/mcp --header "Authorization: Bearer $MDEXA_API_KEY"
```

Keep keys out of repositories and prompts.

## Tools

`search_datasets`, `search_content`, `get_card`, `get_license_evidence`, `list_facets`, `get_overview` (not counted), `get_access`, `find_similar_datasets`, `batch_check` (needs a free-account key), `check_changes`, `request_dataset`.

## Five prompts to copy

1. Can I use the AlphaFold 3 weights commercially? Use Mdexa and quote the source. (`get_card` for `alphafold3`: code Apache-2.0, weights restricted.)
2. AlphaFold DB has a permissive license. Why does it still carry risk flags? (`get_license_evidence` for `alphafold-db`.)
3. Check this list of datasets and tell me which are not in Mdexa. (`batch_check`.)
4. Is MIMIC-IV in Mdexa? (`search_datasets`; if the answer is "not listed", that is a definitive answer.)
5. What is the license of CBLUE: the repository license and the data license separately? (`get_card`.)

## Notes

- A permissive license with risk flags is not a clean bill; a repository license is not a data license; a model has a code license and a weights license, and Mdexa records both.
- Records state what the source pages say. They are not legal advice. Mdexa does not host dataset files; each record links to the original source.

## Links

Website https://mdexa.com/ · Agent guide https://mdexa.com/agents.md · llms.txt https://mdexa.com/llms.txt · Open records https://github.com/mdexa-ai/database

## License

Apache-2.0, see [LICENSE](LICENSE).

