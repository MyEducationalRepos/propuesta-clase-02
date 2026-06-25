"""
Agente de Triaje de Siniestros -- Google ADK
=============================================
Ejemplo funcional para la Clase 2 del programa de IA para Seguros.

Ejecución vía Docker:
    docker compose up adk

Requiere GOOGLE_API_KEY en el archivo .env (ver .env.copy).
"""

import asyncio
import os
import sys

from google.adk.agents import Agent
from google.adk.runners import InMemoryRunner
from google.genai import types

if not os.environ.get("GOOGLE_API_KEY"):
    sys.exit(
        "ERROR: GOOGLE_API_KEY no está definida.\n"
        "Copia .env.copy a .env y agrega tu API key de Google AI Studio.\n"
        "Luego ejecuta: docker compose up adk"
    )


# =============================================================================
# HERRAMIENTAS (TOOLS)
# =============================================================================
# Cada función es una herramienta que el agente puede invocar.
# El modelo lee el docstring para decidir CUÁNDO usarla.
# Los type hints definen los parámetros que el modelo debe proveer.
# =============================================================================

def consultar_poliza(numero_poliza: str) -> dict:
    """Consulta el estado y los datos de una póliza por su número.
    Retorna estado (Vigente/Vencida), ramo, suma asegurada y deducible.
    Usar siempre que el aviso de siniestro mencione un número de póliza.
    """
    # En producción, esto sería una llamada a la API del sistema de pólizas.
    # Aquí se usa un diccionario como simulación.
    polizas = {
        "POL-2024-001": {
            "estado": "Vigente",
            "ramo": "Incendio",
            "suma_asegurada": "500.000.000 CLP",
            "deducible": "10 UF",
            "asegurado": "Industrias del Pacífico SpA",
        },
        "POL-2024-002": {
            "estado": "Vencida",
            "ramo": "Vehículo",
            "suma_asegurada": "25.000.000 CLP",
            "deducible": "3 UF",
            "asegurado": "Transportes Ruta Sur Ltda.",
        },
        "POL-2024-003": {
            "estado": "Vigente",
            "ramo": "Responsabilidad Civil",
            "suma_asegurada": "200.000.000 CLP",
            "deducible": "5 UF",
            "asegurado": "Farmacias del Centro S.A.",
        },
        "POL-2024-004": {
            "estado": "Vigente",
            "ramo": "Transporte",
            "suma_asegurada": "150.000.000 CLP",
            "deducible": "8 UF",
            "asegurado": "Logística Andes SpA",
        },
    }
    resultado = polizas.get(numero_poliza)
    if resultado:
        return resultado
    return {"estado": "No encontrada", "mensaje": "Póliza no existe en el sistema"}


def asignar_liquidador(ramo: str, severidad: str) -> dict:
    """Asigna un liquidador según el ramo del siniestro y su severidad estimada.
    Usar después de haber clasificado la severidad del siniestro.
    Parámetros:
        ramo: el ramo de la póliza (Incendio, Vehículo, RC, Transporte, etc.)
        severidad: Alta, Media o Baja
    """
    asignaciones = {
        ("Incendio", "Alta"): {
            "liquidador": "María González",
            "cargo": "Liquidador Senior — Incendio",
            "telefono": "+56 9 8765 4321",
            "email": "mgonzalez@proteccion-nacional.cl",
        },
        ("Incendio", "Media"): {
            "liquidador": "Carlos Ruiz",
            "cargo": "Liquidador — Incendio",
            "telefono": "+56 9 1234 5678",
            "email": "cruiz@proteccion-nacional.cl",
        },
        ("Incendio", "Baja"): {
            "liquidador": "Pool General",
            "cargo": "Asignación automática",
            "telefono": "Mesa central: +56 2 2345 6789",
            "email": "siniestros@proteccion-nacional.cl",
        },
        ("Responsabilidad Civil", "Alta"): {
            "liquidador": "Andrea Soto",
            "cargo": "Liquidador Senior — RC",
            "telefono": "+56 9 5555 1234",
            "email": "asoto@proteccion-nacional.cl",
        },
        ("Responsabilidad Civil", "Media"): {
            "liquidador": "Pool General",
            "cargo": "Asignación automática",
            "telefono": "Mesa central: +56 2 2345 6789",
            "email": "siniestros@proteccion-nacional.cl",
        },
        ("Responsabilidad Civil", "Baja"): {
            "liquidador": "Pool General",
            "cargo": "Asignación automática",
            "telefono": "Mesa central: +56 2 2345 6789",
            "email": "siniestros@proteccion-nacional.cl",
        },
        ("Transporte", "Alta"): {
            "liquidador": "Roberto Méndez",
            "cargo": "Liquidador Senior — Transporte",
            "telefono": "+56 9 7777 8888",
            "email": "rmendez@proteccion-nacional.cl",
        },
        ("Transporte", "Media"): {
            "liquidador": "Pool General",
            "cargo": "Asignación automática",
            "telefono": "Mesa central: +56 2 2345 6789",
            "email": "siniestros@proteccion-nacional.cl",
        },
    }
    resultado = asignaciones.get((ramo, severidad))
    if resultado:
        return resultado
    return {
        "liquidador": "Pool General",
        "cargo": "Asignación manual requerida — combinación no encontrada",
        "telefono": "Mesa central: +56 2 2345 6789",
        "email": "siniestros@proteccion-nacional.cl",
    }


def registrar_clasificacion(
    numero_poliza: str,
    ramo: str,
    severidad: str,
    liquidador: str,
    resumen: str,
) -> dict:
    """Registra la clasificación del siniestro en el sistema de log.
    Usar al final del proceso, después de haber clasificado y asignado liquidador.
    """
    # En producción, esto escribiría en Google Sheets, BigQuery o el sistema core.
    registro = {
        "status": "Registrado",
        "numero_poliza": numero_poliza,
        "ramo": ramo,
        "severidad": severidad,
        "liquidador": liquidador,
        "resumen": resumen,
    }
    print(f"\n[LOG] Siniestro registrado: {registro}")
    return registro


# =============================================================================
# DEFINICIÓN DEL AGENTE
# =============================================================================

INSTRUCCIONES_AGENTE = """Eres un agente de triaje de siniestros para la compañía
de seguros "Protección Nacional" en Chile.

PROCESO:
1. Extrae el número de póliza del aviso de siniestro.
2. Usa la herramienta consultar_poliza para verificar estado y ramo.
3. Si la póliza NO está vigente, informa que el siniestro no puede procesarse
   y detente. No asignes liquidador ni clasifiques.
4. Si está vigente, clasifica la severidad según el monto estimado:
   - Baja: menor a 500 UF
   - Media: entre 500 y 2000 UF
   - Alta: mayor a 2000 UF
5. Usa la herramienta asignar_liquidador con el ramo y la severidad.
6. Usa la herramienta registrar_clasificacion para dejar constancia.
7. Responde con este formato:

   PÓLIZA: [número]
   ASEGURADO: [nombre]
   ESTADO: [vigente/vencida]
   RAMO: [ramo]
   SEVERIDAD: [baja/media/alta]
   LIQUIDADOR: [nombre — cargo]
   CONTACTO: [teléfono / email]
   OBSERVACIONES: [notas relevantes]

REGLAS ESPECIALES:
- Si el siniestro involucra terremoto o sismo, clasificar siempre como Alta
  independientemente del monto. Agregar nota: "Activar protocolo de catástrofe."
- Si hay personas heridas, clasificar siempre como Alta. Agregar nota:
  "Verificar cobertura de responsabilidad civil por lesiones."
- Si el monto supera 2000 UF, agregar una sección AVISO REASEGURADOR con
  un borrador del aviso incluyendo todos los datos disponibles.

RESTRICCIONES:
- Nunca inventes datos que no provengan de las herramientas.
- Si faltan datos en el aviso (número de póliza, monto), solicítalos antes
  de clasificar.
- Toda clasificación es preliminar y requiere validación del liquidador asignado.
"""

agente_triaje = Agent(
    name="triaje_siniestros",
    model="gemini-2.5-flash",
    instruction=INSTRUCCIONES_AGENTE,
    tools=[consultar_poliza, asignar_liquidador, registrar_clasificacion],
)


# =============================================================================
# EJECUCIÓN
# =============================================================================

runner = InMemoryRunner(agent=agente_triaje, app_name="triaje_seguros")


async def procesar_siniestro(aviso: str, verbose: bool = True) -> str:
    """Envía un aviso de siniestro al agente y retorna su respuesta."""
    session = await runner.session_service.create_session(
        app_name="triaje_seguros", user_id="demo"
    )
    message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=aviso)],
    )
    response_parts = []
    async for event in runner.run_async(
        user_id="demo",
        session_id=session.id,
        new_message=message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response_parts.append(part.text)
                if verbose and part.function_call:
                    print(f"  [TOOL_CALL] {part.function_call.name}"
                          f"({part.function_call.args})")
                if verbose and part.function_response:
                    print(f"  [TOOL_RESULT] {part.function_response.response}")

    response = "".join(response_parts)
    if verbose:
        print(f"\n{'='*60}")
        print(response)
        print(f"{'='*60}\n")
    return response


# =============================================================================
# CASOS DE PRUEBA
# =============================================================================

AVISOS = [
    # Caso 1: Estándar, baja severidad
    (
        "Caso estándar — Baja severidad",
        "Se reporta robo con fractura de ventanal en sucursal de farmacia. "
        "Póliza POL-2024-003. Sustrajeron equipos computacionales. "
        "Valor estimado 300 UF. Sin heridos.",
    ),
    # Caso 2: Póliza vencida
    (
        "Póliza vencida",
        "Colisión de vehículo de flota en Ruta 68. "
        "Póliza POL-2024-002. Daño estimado 800 UF. Conductor ileso.",
    ),
    # Caso 3: Alta severidad con aviso al reasegurador
    (
        "Alta severidad — Aviso al reasegurador",
        "Explosión en caldera de edificio industrial. "
        "Daño estructural severo en el ala norte. Póliza POL-2024-001. "
        "Estimación preliminar: 8000 UF. "
        "Dos trabajadores con quemaduras leves evacuados al hospital.",
    ),
    # Caso 4: Datos incompletos
    (
        "Datos incompletos",
        "Cliente llama para avisar que chocaron su auto estacionado. "
        "No tiene el número de póliza a mano. "
        "Dice que el daño es considerable pero no sabe el monto.",
    ),
    # Caso 5: Terremoto (regla especial)
    (
        "Terremoto — Protocolo de catástrofe",
        "Daños en edificio comercial de 5 pisos tras sismo de magnitud 6.2 "
        "en Concepción. Póliza POL-2024-001. "
        "Grietas visibles en muros y desprendimiento de cielo. "
        "Monto por evaluar. No se reportan heridos.",
    ),
    # Caso 6: Póliza inexistente
    (
        "Póliza no encontrada",
        "Filtración de agua en oficina del tercer piso. "
        "Daño a servidores y mobiliario. Póliza POL-2024-099. "
        "Monto estimado 1200 UF.",
    ),
]


async def ejecutar_todos():
    """Ejecuta todos los casos de prueba secuencialmente."""
    for titulo, aviso in AVISOS:
        print(f"\n{'#'*60}")
        print(f"# CASO: {titulo}")
        print(f"# INPUT: {aviso[:80]}...")
        print(f"{'#'*60}")
        await procesar_siniestro(aviso)


if __name__ == "__main__":
    asyncio.run(ejecutar_todos())
