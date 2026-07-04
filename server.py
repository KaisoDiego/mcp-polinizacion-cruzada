import sys
import os
from mcp.server.fastmcp import FastMCP
import anthropic
from dotenv import load_dotenv

load_dotenv()

# ── SERVIDOR MCP ──────────────────────────────────────────────────────────────
mcp = FastMCP("Servidor de Polinización Cruzada 🧬")
client = anthropic.Anthropic()

# ── TOOL 1: ABSTRAE ───────────────────────────────────────────────────────────
@mcp.tool()
def abstrae_tool(problema: str) -> str:
    """
    Extrae los principios fundamentales de un problema de software,
    descontextualizados de la informática. Úsala primero, antes que
    compara_tool o implementa_tool.
    """
    print(f"[abstrae_tool] Procesando: {problema[:50]}...", file=sys.stderr)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""Eres un experto en abstracción de sistemas.
            
Dado este problema de software: "{problema}"

Extrae sus principios fundamentales SIN usar jerga tecnológica.
Expresa cada principio como un concepto universal que podría aplicarse
en cualquier dominio (biología, física, economía, etc.).

Formato de respuesta:
## Principios Fundamentales

1. [Principio 1]: [descripción en lenguaje universal]
2. [Principio 2]: [descripción en lenguaje universal]
...

Máximo 5 principios. Sé específico y conciso."""
        }]
    )
    return response.content[0].text

# ── TOOL 2: COMPARA ───────────────────────────────────────────────────────────
@mcp.tool()
def compara_tool(principios: str) -> str:
    """
    Busca correlaciones entre los principios abstractos dados y procesos
    naturales o consolidados en campos externos a la informática.
    Úsala después de abstrae_tool y antes de implementa_tool.
    """
    print(f"[compara_tool] Buscando correlaciones...", file=sys.stderr)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1200,
        messages=[{
            "role": "user",
            "content": f"""Eres un experto en polinización cruzada entre disciplinas.

Dados estos principios abstractos:
{principios}

Busca procesos en campos EXTERNOS a la informática (biología, física,
economía, arquitectura, logística, música, urbanismo, ecología, etc.)
donde estos principios aparezcan de forma natural o consolidada.

Para cada correlación:
- Indica el campo externo
- Describe el proceso análogo
- Justifica por qué los principios coinciden
- Asigna nivel de confianza: [Alta confianza] o [Especulativo]

Si no existe correlación útil, decláralo abiertamente.

Formato:
## Correlación Externa

**Campo:** [nombre del campo]
**Proceso análogo:** [descripción]
**Justificación:** [por qué coinciden los principios]
**Confianza:** [Alta confianza / Especulativo]"""
        }]
    )
    return response.content[0].text

# ── TOOL 3: IMPLEMENTA ────────────────────────────────────────────────────────
@mcp.tool()
def implementa_tool(correlacion: str, problema: str) -> str:
    """
    Traduce una correlación externa en una propuesta de implementación
    concreta de software. Úsala después de compara_tool, como último paso.
    """
    print(f"[implementa_tool] Generando propuesta...", file=sys.stderr)
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""Eres un arquitecto de software experto en polinización cruzada.

Problema original: "{problema}"

Correlación externa identificada:
{correlacion}

Traduce esta correlación en una propuesta de implementación de software concreta.
Incluye pseudocódigo o descripción técnica detallada.

Formato:
## Propuesta con Polinización Cruzada

### Inspiración
[Cómo el proceso externo inspira la solución]

### Implementación
[Pseudocódigo o descripción técnica]

### Ventajas sobre implementación estándar
- [ventaja 1]
- [ventaja 2]

### Limitaciones
- [limitación 1]"""
        }]
    )
    return response.content[0].text

# ── ENTRY POINT ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Servidor MCP de Polinización Cruzada iniciado", file=sys.stderr)
    mcp.run(transport="stdio")