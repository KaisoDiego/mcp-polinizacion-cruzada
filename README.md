# 🧬 MCP Server — Cross-Pollination for Software Architecture

An MCP (Model Context Protocol) server that exposes 3 cross-pollination tools: given a software problem, it extracts its abstract principles, finds correlations in external fields (biology, physics, economics, etc.), and proposes an alternative implementation inspired by those natural processes.

**Verified with 2 different agentic clients:** Claude Desktop and CrewAI — without modifying a single line of the server.

---

## What is cross-pollination in software?

A design technique where the fundamental principles of a software problem are abstracted from the technological domain and analogous solutions are sought in other fields. For example: the problem of *load balancing without a central coordinator* is solved analogously to how biological tissues distribute nutrients — without a central node, using local gradients.

The server implements this process as 3 chained tools:

```
abstrae_tool → compara_tool → implementa_tool
```

---

## Exposed Tools

| Tool | Input | Output |
|---|---|---|
| `abstrae_tool` | Software problem description | Fundamental principles without tech jargon |
| `compara_tool` | Abstract principles | External field correlation with confidence level |
| `implementa_tool` | Correlation + original problem | Concrete implementation proposal with pseudocode |

Each tool makes an internal call to Claude (Haiku 4.5) with a specialized prompt. The MCP client doesn't need to know how they're implemented — it discovers and uses them dynamically.

---

## Architecture

```
server.py (FastMCP, Stdio transport)
     ↓ exposes 3 tools via MCP
     ├── Client 1: Claude Desktop
     │   config: claude_desktop_config.json
     └── Client 2: CrewAI
         config: cliente_mcp.py (MCPServerAdapter)
```

**Dynamic discovery verified:**
```
Tools available from MCP server: ['abstrae_tool', 'compara_tool', 'implementa_tool']
```
CrewAI discovers the tools at runtime via `tools/list` — they are not hardcoded in the client.

---

## Installation

### Prerequisites
- Python 3.10+
- Anthropic API key (console.anthropic.com)

### Setup
```bash
git clone https://github.com/KaisoDiego/mcp-polinizacion-cruzada.git
cd mcp-polinizacion-cruzada
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
pip install mcp anthropic python-dotenv
```

Create a `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Verify the server starts
```bash
python server.py
# Output: "Servidor MCP de Polinización Cruzada iniciado"
# Ctrl+C to stop
```

---

## Client 1 — Claude Desktop

Edit `claude_desktop_config.json`:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "polinizacion-cruzada": {
      "command": "/absolute/path/to/venv/Scripts/python.exe",
      "args": ["/absolute/path/to/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

Restart Claude Desktop completely. Verify in **Settings → Developer** that the server appears with a green dot.

**Test prompt:**
> "Apply cross-pollination to the problem of designing a rate limiting system for a high-concurrency API"

---

## Client 2 — CrewAI

```bash
pip install crewai "crewai-tools[mcp]"
```

```python
from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
import asyncio

async def main():
    server_params = {
        "command": "/absolute/path/to/venv/Scripts/python.exe",
        "args": ["/absolute/path/to/server.py"]
    }
    async with MCPServerAdapter(server_params) as mcp_tools:
        agent = Agent(
            role="Software Architect with Cross-Pollination",
            goal="Apply cross-pollination to propose innovative implementations",
            backstory="An architect who combines knowledge from multiple disciplines.",
            tools=list(mcp_tools),
            llm="anthropic/claude-haiku-4-5-20251001"
        )
        task = Task(
            description="Apply cross-pollination to: {your_problem}. Use tools in sequence.",
            expected_output="Document with abstract principles, external correlation, and implementation proposal.",
            agent=agent
        )
        crew = Crew(agents=[agent], tasks=[task])
        print(crew.kickoff())

asyncio.run(main())
```

---

## Demo — Real Example

**Input:** *"Design a load balancing system for 50 workers without a central coordinator"*

**`abstrae_tool` →** Principles: distribution without central authority, local optimization with partial visibility, dynamic stability, asynchronous communication.

**`compara_tool` →** `[High confidence]` Correlation with nutrient diffusion in biological tissues — cells without a central coordinator, local gradients, paracrine signaling.

**`implementa_tool` →** Proposal: load gradient + spreading diffusion algorithm inspired by the tissue model. Includes Python pseudocode and comparative table vs. standard consistent hashing.

---

## Technical Findings

- **Critical Stdio rule:** never use `print()` in the server — it corrupts the JSON-RPC stream. Use `print(..., file=sys.stderr)` instead.
- **FastMCP** automatically generates `inputSchema` from Python type hints and docstrings.
- **Client friction:** Claude Desktop requires only JSON configuration. CrewAI requires `MCPServerAdapter` + async handling + `crewai-tools[mcp]` extra package.

---

## Stack

- `mcp` — official Model Context Protocol SDK
- `anthropic` — Anthropic SDK for LLM calls
- `FastMCP` — abstraction over the SDK for defining tools with decorators
- Transport: **Stdio** (local) — upgradeable to Streamable HTTP for remote multi-client

---

## Context

Project #3 of a 8-10 week AI agents learning plan. Empirically verifies MCP's core promise: the same server serves clients from different frameworks without modifying a single line of server code.

Related projects:
- [Project #2 — CrewAI vs LangGraph](https://github.com/KaisoDiego/crewai-langgraph-comparativa)
