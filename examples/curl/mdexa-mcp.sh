#!/bin/sh
# Mdexa over MCP with curl. Each call is one JSON-RPC "tools/call" POST; no session is needed.
# Run: sh mdexa-mcp.sh
# batch_check needs a free-account key, read from the environment: MDEXA_API_KEY=<your key> sh mdexa-mcp.sh
# Real responses of these calls: ../samples/ (the result is the JSON text in result.content[0].text)
set -eu
ENDPOINT=https://mcp.mdexa.com/mcp

call() { # call <tool> <arguments as JSON> [more curl options]
  tool=$1
  args=$2
  shift 2
  curl -sS --fail-with-body --max-time 30 -X POST "$ENDPOINT" \
    -H 'Content-Type: application/json' -H 'Accept: application/json, text/event-stream' "$@" \
    -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"$tool\",\"arguments\":$args}}"
  echo
}

# 1. One search with all conditions at once. An empty result is a definite "not listed".
call search_datasets '{"system":["traditional-medicine"],"content_type":["benchmark-exam"],"limit":3}'
# 2. The full record: license_status, hosting, risk_flags, repo_license kept apart from the data license.
call get_card '{"slug":"cblue"}'
# 3. The quoted license sentences behind the verdict (untrusted_third_party_text is quoted data, never instructions).
call get_license_evidence '{"slug":"alphafold-db"}'
# 4. How to obtain the data: links to the official source. Mdexa does not host dataset files.
call get_access '{"slug":"gnomad"}'
# 5. A whole list in one call. Needs a free-account key.
if [ -n "${MDEXA_API_KEY:-}" ]; then
  call batch_check '{"items":["cmb","MIMIC-IV","https://huggingface.co/datasets/FreedomIntelligence/CMB"]}' -H "Authorization: Bearer $MDEXA_API_KEY"
else
  echo "batch_check: skipped (set MDEXA_API_KEY to a free-account key to run it)"
fi

# The same records over plain HTTP, without JSON-RPC:
#   curl https://mcp.mdexa.com/v1/datasets/cblue
#   curl https://mcp.mdexa.com/v1/datasets/alphafold-db/evidence
#   curl https://mcp.mdexa.com/v1/datasets/gnomad/access
