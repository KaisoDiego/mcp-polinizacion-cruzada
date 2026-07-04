# 🧬 MCP Server — Polinización Cruzada para Arquitectura de Software

Un servidor MCP (Model Context Protocol) que expone 3 herramientas de **polinización cruzada**: dado un problema de software, extrae sus principios abstractos, busca correlaciones en campos externos (biología, física, economía, etc.) y propone una implementación alternativa inspirada en esos procesos naturales.

**Verificado con 2 clientes agénticos distintos:** Claude Desktop y CrewAI — sin modificar una línea del servidor.

---

## ¿Qué es polinización cruzada en software?

Es una técnica de diseño donde los principios fundamentales de un problema de software se abstraen del dominio tecnológico y se buscan soluciones análogas en otros campos. Por ejemplo: el problema de *balanceo de carga sin coordinador central* se resuelve de forma análoga a como los tejidos biológicos distribuyen nutrientes — sin un nodo central, usando gradientes locales.

El servidor implementa este proceso en 3 herramientas encadenadas:

```
abstrae_tool → compara_tool → implementa_tool
```

---

## Herramientas expuestas

| Tool | Input | Output |
|---|---|---|
| `abstrae_tool` | Descripción del problema de software | Principios fundamentales sin jerga tecnológica |
| `compara_tool` | Principios abstractos | Correlación en campo externo con nivel de confianza |
| `implementa_tool` | Correlación + problema original | Propuesta de implementación con pseudocódigo |

Cada tool hace una llamada interna a Claude (Haiku 4.5) con un prompt especializado. El cliente MCP no necesita saber cómo están implementadas — solo las descubre y las usa.

---

## Arquitectura

```
server.py (FastMCP, transporte Stdio)
     ↓ expone 3 tools via MCP
     ├── Cliente 1: Claude Desktop
     │   config: claude_desktop_config.json
     └── Cliente 2: CrewAI
         config: cliente_mcp.py (MCPServerAdapter)
```

**Discovery dinámico verificado:**
```
Tools disponibles desde servidor MCP: ['abstrae_tool', 'compara_tool', 'implementa_tool']
```
CrewAI descubre las tools en runtime via `tools/list` — no están hardcodeadas en el cliente.

---

## Instalación

### Prerequisitos
- Python 3.10+
- API key de Anthropic (console.anthropic.com)

### Setup
```bash
git clone https://github.com/KaisoDiego/mcp-polinizacion-cruzada.git
cd mcp-polinizacion-cruzada
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
pip install mcp anthropic python-dotenv
```

Crea un archivo `.env`:
```
ANTHROPIC_API_KEY=sk-ant-...
```

### Verificar que el servidor arranca
```bash
python server.py
# Output: "Servidor MCP de Polinización Cruzada iniciado"
# Ctrl+C para salir
```

---

## Conectar Cliente 1 — Claude Desktop

Edita `claude_desktop_config.json` (ubicación según OS):
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "polinizacion-cruzada": {
      "command": "/ruta/absoluta/venv/Scripts/python.exe",
      "args": ["/ruta/absoluta/server.py"],
      "env": {
        "ANTHROPIC_API_KEY": "sk-ant-..."
      }
    }
  }
}
```

Reinicia Claude Desktop completamente. Verifica en **Settings → Developer** que el servidor aparece con punto verde.

**Prompt de prueba:**
> "Aplica polinización cruzada al problema de diseñar un sistema de rate limiting para una API con alta concurrencia"

---

## Conectar Cliente 2 — CrewAI

```bash
pip install crewai "crewai-tools[mcp]"
```

```python
from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter
import asyncio

async def main():
    server_params = {
        "command": "/ruta/absoluta/venv/Scripts/python.exe",
        "args": ["/ruta/absoluta/server.py"]
    }
    async with MCPServerAdapter(server_params) as mcp_tools:
        agente = Agent(
            role="Arquitecto de Software con Polinización Cruzada",
            goal="Aplicar polinización cruzada para proponer implementaciones innovadoras",
            backstory="Arquitecto que combina conocimiento de múltiples disciplinas.",
            tools=list(mcp_tools),
            llm="anthropic/claude-haiku-4-5-20251001"
        )
        tarea = Task(
            description="Aplica polinización cruzada al problema: {tu_problema}. Usa las tools en secuencia.",
            expected_output="Documento con principios abstractos, correlación externa y propuesta de implementación.",
            agent=agente
        )
        crew = Crew(agents=[agente], tasks=[tarea])
        print(crew.kickoff())

asyncio.run(main())
```

---

## Demo — Ejemplo real

**Input:** *"Diseñar un sistema de balanceo de carga para 50 workers sin coordinador central"*

**`abstrae_tool` →** Principios: distribución sin autoridad central, optimización local con visibilidad parcial, estabilidad dinámica, comunicación asincrónica.

**`compara_tool` →** `[Alta confianza]` Correlación con difusión de nutrientes en tejidos biológicos — células sin coordinador central, gradientes locales, señales paracrinas.

**`implementa_tool` →** Propuesta: algoritmo de gradiente de carga + difusión creciente inspirado en el modelo tisular. Incluye pseudocódigo Python y tabla comparativa vs. hash consistente estándar.

---

## Hallazgos técnicos

- **Regla crítica Stdio:** nunca usar `print()` en el servidor — corrompe el stream JSON-RPC. Usar `print(..., file=sys.stderr)`.
- **FastMCP** genera el `inputSchema` automáticamente desde type hints y docstrings de Python.
- **Fricción por cliente:** Claude Desktop requiere solo configuración JSON. CrewAI requiere `MCPServerAdapter` + manejo async + extra `crewai-tools[mcp]`.

---

## Stack

- `mcp` — SDK oficial de Model Context Protocol
- `anthropic` — SDK de Anthropic para llamadas al LLM
- `FastMCP` — abstracción sobre el SDK para definir tools con decoradores
- Transporte: **Stdio** (local) — migrable a Streamable HTTP para multi-cliente remoto

---

