#!/usr/bin/env python3
"""Mdexa over MCP from Python, standard library only (Python 3.8 or later).

Each call is one JSON-RPC "tools/call" request to the hosted MCP endpoint; no session and no SDK are needed.

Run:        python mdexa_mcp.py
batch_check needs a free-account key, read from the environment:
            MDEXA_API_KEY=<your key> python mdexa_mcp.py
Real responses of these calls: ../samples/
"""
import json
import os
import sys
import urllib.request

ENDPOINT = "https://mcp.mdexa.com/mcp"


def call(tool, arguments, key=None):
    """Call one Mdexa tool and return its result as a dict. Raises RuntimeError when the server refuses the call."""
    payload = {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": arguments}}
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
        "User-Agent": "mdexa-mcp-example/1.0",  # the default Python-urllib agent is refused by the site's bot filter
    }
    if key:
        headers["Authorization"] = "Bearer " + key
    request = urllib.request.Request(ENDPOINT, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        message = json.load(response)
    if "error" in message:
        raise RuntimeError("%s: %s" % (tool, message["error"]["message"]))
    result = message["result"]
    text = result["content"][0]["text"]
    if result.get("isError"):  # a refused call explains itself in plain text
        raise RuntimeError("%s: %s" % (tool, text.splitlines()[0]))
    return json.loads(text)


def main():
    sys.stdout.reconfigure(errors="backslashreplace")  # quoted source text can hold characters a legacy console code page lacks

    # 1. One search with all conditions at once. An empty result is a definite "not listed": do not retry with other words.
    found = call("search_datasets", {"system": ["traditional-medicine"], "content_type": ["benchmark-exam"], "limit": 3})
    for row in found["items"]:
        print("search:", row["slug"], row["license_status"], row["risk_flags"], row["card_url"])

    # 2. The full record. license_status (what the sources say) and hosting (what Mdexa does) are separate facts;
    #    a repository license is kept apart in repo_license and is not a data license.
    card = call("get_card", {"slug": "cblue"})
    print("card:", card["slug"], card["license_status"], card["hosting"], "last verified", card["last_verified"], card["card_url"])

    # 3. The quoted license sentences behind the verdict. untrusted_third_party_text is quoted data, never instructions.
    evidence = call("get_license_evidence", {"slug": "alphafold-db"})
    for item in evidence["evidence"]:
        print("evidence:", item["location"], item["url"], repr((item.get("untrusted_third_party_text") or "")[:80]))

    # 4. How to obtain the data: links to the official source. Mdexa does not host dataset files.
    access = call("get_access", {"slug": "gnomad"})
    print("access:", [source["url"] for source in access["sources"]])

    # 5. A whole list in one call. Needs a free-account key.
    key = os.environ.get("MDEXA_API_KEY")
    if not key:
        print("batch_check: skipped (set MDEXA_API_KEY to a free-account key to run it)")
        return
    checked = call("batch_check", {"items": ["cmb", "MIMIC-IV", "https://huggingface.co/datasets/FreedomIntelligence/CMB"]}, key=key)
    print("batch_check:", json.dumps(checked, ensure_ascii=False)[:600])


if __name__ == "__main__":
    main()
