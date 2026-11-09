"""One bounded, neutral installed-wheel cycle; no source checkout or real memory."""
import asyncio
from contextlib import asynccontextmanager
import json
import os
from pathlib import Path
import sys
import tempfile
from urllib.request import urlopen

import dandelion
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def call(client, name, arguments=None):
    result = await client.call_tool(name, arguments or {})
    assert not result.is_error, (name, result)
    return json.loads(next(part.text for part in result.content if part.type == "text"))


@asynccontextmanager
async def connect(directory):
    env = {k: v for k, v in os.environ.items()
           if not k.upper().startswith(("PYTHON", "DANDELION_"))}
    params = StdioServerParameters(
        command=sys.executable,
        args=["-I", "-m", "dandelion", "serve", "--memory-path", str(directory),
              "--local-owner", "--lifecycle-v1", "--access-mode", "trusted-local"],
        cwd=str(directory), env=env,
    )
    async with stdio_client(params) as (reader, writer):
        async with ClientSession(reader, writer) as client:
            initialized = await client.initialize()
            assert initialized.server_info.version == "1.0.0rc18"
            yield client


async def check(directory):
    assert sys.flags.isolated
    package = Path(dandelion.__file__).resolve()
    assert "site-packages" in package.parts, package
    assert dandelion.__version__ == "1.0.0rc18"
    async with connect(directory) as client:
        fact = await call(client, "create_fact", {"subject": "demo.port", "value": "8080"})
        note = await call(client, "remember_typed", {
            "domain": "demo", "record_kind": "OBSERVATION", "disposition": "ACTIVE",
            "content": "Now: " + fact["reference_templates"]["live"]
                       + "; before: " + fact["reference_templates"]["pinned"],
        })
        changed = await call(client, "lifecycle_v1_correct_fact", {
            "key": fact["key"], "expected_revision": 1, "value": "8081"})
        assert changed["revision"] == 2
    async with connect(directory) as client:
        assert (await call(client, "domain_map"))["count"] == 1
        current = await call(client, "get_fact", {"key": fact["key"]})
        assert (current["value"], current["authority"]) == ("8081", "AGENT")
        old = await call(client, "get_fact", {"key": fact["key"], "revision": 1})
        assert old["value"] == "8080"
        read = await call(client, "read_memory", {"memory_id": note["memory_id"]})
        assert read["text"] == "Now: 8081; before: 8080"
        standalone = await call(client, "create_fact", {"subject": "demo.standalone", "value": "retained"})
        studio = await call(client, "open_studio")
        with urlopen(studio["url"], timeout=10) as response:
            page = response.read()
            assert response.status == 200
            assert b"timeline-date" in page and b"memory-edit-form" in page
            assert b'id="include-history"' in page
        with urlopen(studio["url"] + "memory", timeout=10) as response:
            snapshot = json.load(response)
        assert snapshot["owner"]["package_version"] == "1.0.0rc18"
        facts = {row["key"]: row for row in snapshot["facts"]}
        assert facts[standalone["key"]]["current"]["value"] == "retained"
        assert facts[fact["key"]]["current"]["value"] == "8081"
        assert {row["revision"]: row["value"] for row in facts[fact["key"]]["revisions"]} == {1: "8080", 2: "8081"}


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="dandelion-portability-") as temp:
        asyncio.run(asyncio.wait_for(check(Path(temp)), timeout=90))
    print(json.dumps({"status": "PASS", "release": "1.0.0rc18",
                      "platform": sys.platform, "python": sys.version.split()[0],
                      "scope": "installed stdio and Studio HTTP; not desktop client or agent quality"}))
