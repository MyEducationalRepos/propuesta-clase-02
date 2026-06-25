# Agente de Triaje de Siniestros (Google ADK)

Este ejemplo es un agente de inteligencia artificial que clasifica siniestros de seguros de forma automática. "Triaje" significa decidir la prioridad y el camino que debe seguir cada caso, igual que en una urgencia médica.

El agente recibe un aviso de siniestro en texto libre (como lo escribiría un asegurado o un corredor) y decide por sí solo qué hacer: verifica la póliza, clasifica la severidad, asigna un liquidador y genera un reporte estructurado. Todo esto sin intervención humana.

Usa Google ADK (Agent Development Kit, un kit de desarrollo de agentes) con el modelo Gemini 2.5 Flash.

## Antes de ejecutar

Asegúrate de haber completado los Pasos 1 a 5 del [README principal](../../README.md). En resumen necesitas:

- Docker Desktop abierto y funcionando
- El archivo `.env` creado con tu API Key de Google

## Cómo ejecutar el agente

Abre tu terminal, navega a la carpeta del proyecto (la carpeta `propuesta-clase-02`) y ejecuta:

```bash
docker compose up adk
```

Este comando le dice a Docker que:
1. Construya un contenedor con Python y las dependencias necesarias
2. Ejecute el agente de triaje con 6 casos de prueba predefinidos
3. Muestre los resultados en tu terminal

La primera vez puede tardar 2-3 minutos mientras Docker descarga todo. Las siguientes veces será mucho más rápido.

## Qué verás en la terminal

Cuando el agente se ejecute, verás textos como estos:

```
[TOOL_CALL] consultar_poliza({"numero_poliza": "POL-2024-001"})
[TOOL_RESULT] {"estado": "Vigente", "ramo": "Incendio", ...}
```

Esto significa:

- `[TOOL_CALL]`: El agente decidió usar una herramienta. Muestra cuál herramienta eligió y con qué datos. Es como si el agente dijera "voy a buscar esta póliza en el sistema".
- `[TOOL_RESULT]`: La herramienta respondió con datos. El agente los lee y decide qué hacer después.
- Al final de cada caso, verás un texto largo con la clasificación completa del siniestro.

## Qué hace el agente paso a paso

Para cada aviso de siniestro, el agente sigue este proceso:

1. Lee el aviso y extrae el número de póliza
2. Consulta el estado de la póliza (herramienta `consultar_poliza`)
3. Si la póliza está vigente, clasifica la severidad (Baja, Media o Alta) según el monto y las circunstancias
4. Asigna un liquidador según el ramo y la severidad (herramienta `asignar_liquidador`)
5. Registra la clasificación en el sistema (herramienta `registrar_clasificacion`)
6. Genera un resumen estructurado con toda la información

Si la póliza está vencida o no existe, el agente detiene el proceso y lo informa.

## El ciclo ReAct (Razonar, Actuar, Observar)

Lo que hace especial a un agente (versus un chatbot común) es que toma decisiones por sí solo. El patrón se llama ReAct:

```
Razonar -> "Necesito verificar si la póliza está vigente"
   Actuar  -> [TOOL_CALL] consultar_poliza(...)
   Observar -> [TOOL_RESULT] {"estado": "Vigente", ...}
Razonar -> "La póliza está vigente. Ahora debo evaluar la severidad y asignar liquidador"
   Actuar  -> [TOOL_CALL] asignar_liquidador(...)
   Observar -> [TOOL_RESULT] {"liquidador": "María González", ...}
Razonar -> "Tengo todos los datos. Genero la respuesta final"
   Responder -> Texto con la clasificación completa
```

El agente repite este ciclo cuantas veces sea necesario. No sigue un guión fijo: decide en cada momento qué herramienta usar basándose en lo que ya sabe.

## Casos de prueba incluidos

El agente procesa estos 6 casos automáticamente:

| # | Caso | Qué demuestra |
|---|------|---------------|
| 1 | Robo en farmacia (POL-2024-003, 300 UF) | Triaje estándar, severidad baja |
| 2 | Colisión vehículo (POL-2024-002, 800 UF) | Póliza vencida: el agente detiene el proceso |
| 3 | Explosión industrial (POL-2024-001, 8000 UF, heridos) | Alta severidad + aviso al reasegurador |
| 4 | Auto chocado (sin póliza, sin monto) | Datos incompletos: el agente solicita información |
| 5 | Terremoto en Concepción (POL-2024-001) | Regla especial: protocolo de catástrofe |
| 6 | Filtración de agua (POL-2024-099, 1200 UF) | Póliza no encontrada en el sistema |

## Qué puedes probar por tu cuenta

Una vez que hayas visto los resultados, puedes experimentar:

- **Modificar un caso de prueba**: Abre el archivo `agente_triaje.py` con un editor de texto, busca la sección de casos de prueba al final, y cambia el texto de un aviso. Por ejemplo, cambia el monto o agrega heridos. Luego ejecuta de nuevo con `--build`.
- **Cambiar las instrucciones del agente**: En el mismo archivo, busca el texto que dice `instruction` (las instrucciones del agente). Prueba agregar una regla nueva, como "Si el monto supera 5000 UF, siempre clasificar como Alta severidad".

Después de cualquier cambio, necesitas ejecutar con `--build` para que Docker reconstruya el contenedor:

```bash
docker compose up adk --build
```

## Errores comunes

### "GOOGLE_API_KEY environment variable not set"

No encontró tu clave de Google. Verifica que:
- Creaste el archivo `.env` en la carpeta raíz del proyecto (no dentro de `examples/adk/`)
- El archivo contiene tu clave correctamente

### "Error 429: Resource exhausted" o "Quota exceeded"

Hiciste demasiadas solicitudes a la API de Google en poco tiempo. Espera unos minutos y vuelve a intentar. La capa gratuita tiene un límite de solicitudes por minuto.

### "Error building Docker image"

Asegúrate de que Docker Desktop está abierto y funcionando. Si el error persiste, intenta:

```bash
docker compose down
docker compose up adk --build
```
