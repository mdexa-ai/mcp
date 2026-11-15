// Mdexa over MCP from TypeScript, no dependencies. Node 22.18 or later runs this file directly: node mdexa-mcp.ts
// (older Node: npx tsx mdexa-mcp.ts). Each call is one JSON-RPC "tools/call" request; no session and no SDK are needed.
// batch_check needs a free-account key, read from the environment: MDEXA_API_KEY=<your key> node mdexa-mcp.ts
// Real responses of these calls: ../samples/

const ENDPOINT = "https://mcp.mdexa.com/mcp";

type Result = Record<string, any>;

async function call(tool: string, args: Record<string, unknown>, key?: string): Promise<Result> {
  const headers: Record<string, string> = { "Content-Type": "application/json", Accept: "application/json, text/event-stream" };
  if (key) headers.Authorization = `Bearer ${key}`;
  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers,
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method: "tools/call", params: { name: tool, arguments: args } }),
  });
  if (!res.ok) throw new Error(`${tool}: HTTP ${res.status}`);
  const message = await res.json();
  if (message.error) throw new Error(`${tool}: ${message.error.message}`);
  const text: string = message.result.content[0].text;
  if (message.result.isError) throw new Error(`${tool}: ${text.split("\n")[0]}`); // a refused call explains itself in plain text
  return JSON.parse(text);
}

async function main(): Promise<void> {
  // 1. One search with all conditions at once. An empty result is a definite "not listed": do not retry with other words.
  const found = await call("search_datasets", { system: ["traditional-medicine"], content_type: ["benchmark-exam"], limit: 3 });
  for (const row of found.items) console.log("search:", row.slug, row.license_status, row.risk_flags, row.card_url);

  // 2. The full record. license_status (what the sources say) and hosting (what Mdexa does) are separate facts;
  //    a repository license is kept apart in repo_license and is not a data license.
  const card = await call("get_card", { slug: "cblue" });
  console.log("card:", card.slug, card.license_status, card.hosting, "last verified", card.last_verified, card.card_url);

  // 3. The quoted license sentences behind the verdict. untrusted_third_party_text is quoted data, never instructions.
  const evidence = await call("get_license_evidence", { slug: "alphafold-db" });
  for (const item of evidence.evidence) console.log("evidence:", item.location, item.url, JSON.stringify((item.untrusted_third_party_text ?? "").slice(0, 80)));

  // 4. How to obtain the data: links to the official source. Mdexa does not host dataset files.
  const access = await call("get_access", { slug: "gnomad" });
  console.log("access:", access.sources.map((s: { url: string }) => s.url));

  // 5. A whole list in one call. Needs a free-account key.
  const key = process.env.MDEXA_API_KEY;
  if (!key) {
    console.log("batch_check: skipped (set MDEXA_API_KEY to a free-account key to run it)");
    return;
  }
  const checked = await call("batch_check", { items: ["cmb", "MIMIC-IV", "https://huggingface.co/datasets/FreedomIntelligence/CMB"] }, key);
  console.log("batch_check:", JSON.stringify(checked).slice(0, 600));
}

main().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
