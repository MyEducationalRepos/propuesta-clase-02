# Workflow de Triaje de Siniestros (n8n)

Este ejemplo hace lo mismo que el ejemplo con código (clasificar siniestros automáticamente), pero usando una herramienta visual llamada n8n. En vez de escribir código, ves el flujo del agente como un diagrama de cajas conectadas por flechas. Es como un diagrama de flujo interactivo que realmente funciona.

n8n (pronunciado "n-eight-n") es una plataforma de automatización visual: conectas "nodos" (cajas) entre sí para crear flujos de trabajo sin programar.

## Antes de ejecutar

Asegúrate de haber completado los Pasos 1 a 5 del [README principal](../../README.md). En resumen necesitas:

- Docker Desktop abierto y funcionando
- El archivo `.env` creado con tu API Key de Google

## Cómo ejecutar n8n

Abre tu terminal, navega a la carpeta del proyecto (la carpeta `propuesta-clase-02`) y ejecuta:

```bash
docker compose up n8n
```

Este comando le dice a Docker que:
1. Construya un contenedor con n8n instalado
2. Importe automáticamente los dos workflows de triaje (no necesitas importar nada manualmente)
3. Inicie n8n en tu computador

Espera hasta ver un mensaje similar a:

```
n8n ready on 0.0.0.0, port 5678
```

Eso significa que n8n está listo. Ahora abre tu navegador (Chrome, Firefox, Safari) y ve a:

[http://localhost:5678](http://localhost:5678)

"localhost" significa "mi propio computador". El número 5678 es el "puerto", como una puerta específica por donde entra la conexión.

## Qué verás en el navegador

### Paso 1: Iniciar sesión

Al abrir `http://localhost:5678` verás una pantalla de inicio de sesión. La cuenta ya está creada automáticamente con estas credenciales:

- **Correo:** `admin@clase.local`
- **Contraseña:** `clase02`

Escríbelas y haz clic en "Sign in".

### Paso 2: Encontrar los workflows importados

Después de iniciar sesión llegarás a un lienzo vacío (la pantalla principal de n8n). Los workflows ya fueron importados, pero no se abren automáticamente. Para encontrarlos:

1. Haz clic en el logotipo de n8n en la esquina superior izquierda (o en el menú lateral si está visible)
2. Selecciona **"Workflows"** en el menú
3. Verás en la lista dos workflows:
   - **"Triaje de Siniestros — Agente IA"** (casos de prueba en lote y webhook)
   - **"Triaje de Siniestros — Chat IA"** (chat interactivo para crear un caso nuevo)
4. Haz clic en el que quieras abrir

### Paso 3: Explorar el workflow

Ahora verás un "canvas" (lienzo) con cajas de colores conectadas por líneas. Cada caja es un "nodo" que hace una tarea específica. El flujo va de izquierda a derecha:

1. Llega un aviso de siniestro (por la izquierda)
2. El agente de IA lo procesa (en el centro)
3. Según el resultado, se toman acciones (hacia la derecha): notificar, registrar, responder

Es como un mapa visual de las decisiones que toma el agente.

## Cómo probar el workflow

La credencial de Gemini se configura automáticamente al iniciar el contenedor usando la clave `GOOGLE_API_KEY` del archivo `.env`. No necesitas configurar nada dentro de n8n.

### Ejecutar todos los casos de prueba (recomendado para la clase)

Abre **"Triaje de Siniestros — Agente IA"**. El workflow incluye 6 casos de prueba integrados (los mismos del ejemplo con código). Para ejecutarlos:

1. Abre el workflow en el navegador (`http://localhost:5678`)
2. Haz clic en el botón naranja **"Execute workflow"** en la parte inferior del canvas

El agente procesará los 6 casos uno por uno. Verás cómo la ejecución avanza nodo por nodo en el canvas. Puedes hacer clic en cada nodo para inspeccionar su entrada y salida. La ejecución toma alrededor de 1-2 minutos en total.

Los 6 casos de prueba son:

1. **Baja severidad** -- Robo en farmacia, 300 UF (POL-2024-003)
2. **Póliza vencida** -- Colisión de vehículo, 800 UF (POL-2024-002)
3. **Alta severidad** -- Explosión industrial, 8000 UF con heridos (POL-2024-001)
4. **Datos incompletos** -- Sin número de póliza ni monto
5. **Terremoto** -- Sismo 6.2, protocolo de catástrofe (POL-2024-001)
6. **Póliza inexistente** -- POL-2024-099, no existe en el sistema

### Alternativa: enviar un caso individual por terminal

Si quieres probar un caso específico, puedes enviar un aviso al webhook. Primero activa el workflow con el interruptor (toggle) en la esquina superior derecha. Luego ejecuta:

```bash
curl -X POST http://localhost:5678/webhook/triaje-siniestro \
  -H "Content-Type: application/json" \
  -d '{
    "aviso": "Se reporta robo con fractura de ventanal en sucursal de farmacia. Póliza POL-2024-003. Sustrajeron equipos computacionales. Valor estimado 300 UF. Sin heridos."
  }'
```

Después de unos segundos, verás en tu terminal la respuesta del agente con la clasificación del siniestro.

### Probar un caso nuevo en el chat (interactivo)

Si quieres escribir tu propio aviso de siniestro y ver la respuesta del agente en una ventana de chat, usa el workflow **"Triaje de Siniestros — Chat IA"**:

1. Abre **"Triaje de Siniestros — Chat IA"** desde la lista de Workflows
2. Verifica que el workflow esté activo (interruptor verde en la esquina superior derecha)
3. Haz clic en el botón **"Chat"** en la esquina inferior derecha del canvas (o en la pestaña Chat del panel lateral)
4. Escribe o pega un aviso de siniestro y presiona Enter

Ejemplo de texto que puedes pegar:

```
Se reporta robo con fractura de ventanal en sucursal de farmacia. Póliza POL-2024-003. Sustrajeron equipos computacionales. Valor estimado 300 UF. Sin heridos.
```

El agente procesará el aviso (puede tardar 15-30 segundos mientras consulta póliza y asigna liquidador) y responderá en el chat con la clasificación estructurada. Los resultados también se guardan en `data/log_triaje.md`.

Para probar una alerta de reaseguro, pega un caso de alta severidad:

```
Explosión en caldera de edificio industrial. Daño estructural severo. Póliza POL-2024-001. Estimación preliminar: 8000 UF. Dos trabajadores con quemaduras leves evacuados al hospital.
```

## Archivos de salida

Cada vez que el agente procesa un siniestro, los resultados se guardan en archivos markdown dentro de la carpeta `data/` del proyecto:

| Archivo | Cuándo se escribe | Contenido |
|---------|-------------------|-----------|
| `data/log_triaje.md` | Siempre (cada siniestro) | Registro completo: fecha, poliza, severidad, liquidador asignado. |
| `data/alertas_reaseguro.md` | Solo cuando la severidad es Alta | Alerta para el reasegurador: fecha, poliza, ramo, observaciones. |

Puedes abrir estos archivos con cualquier editor de texto o visor de markdown para ver los resultados acumulados.

## Descripción de los nodos

### Workflow batch (`Triaje de Siniestros — Agente IA`)

| Nodo | Tipo | Qué hace |
|------|------|----------|
| Ejecutar Todos los Casos | Manual Trigger | Dispara los 6 casos de prueba al hacer clic en "Execute workflow". |
| Casos de Prueba | Code (JavaScript) | Genera los 6 avisos de siniestro como items individuales para el agente. |
| Recibir Aviso de Siniestro | Webhook (POST) | Entrada alternativa. Recibe un aviso individual via curl o API externa. |
| Agente de Triaje | AI Agent (LangChain) | El cerebro del workflow. Razona, usa herramientas y genera la clasificación. |
| Gemini 2.5 Flash | LLM (Google Gemini) | El modelo de IA que alimenta al agente. Temperatura 0.2 para respuestas consistentes. |
| Buscar Póliza | Tool (Code) | Herramienta que consulta datos de una póliza por su número (datos mock inline). |
| Buscar Liquidador | Tool (Code) | Herramienta que asigna un liquidador según ramo y severidad (datos mock inline). |
| ¿Severidad Alta? | If (condicional) | Evalúa si la severidad es "Alta". Si lo es, bifurca el flujo. |
| Alerta Reaseguro | Code (JavaScript) | Escribe una fila en `data/alertas_reaseguro.md` con los datos del siniestro de alta severidad. |
| Registro Log | Code (JavaScript) | Escribe una fila en `data/log_triaje.md` con el resumen de cada caso procesado. |

### Workflow chat (`Triaje de Siniestros — Chat IA`)

| Nodo | Tipo | Qué hace |
|------|------|----------|
| Recibir Mensaje de Chat | Chat Trigger | Entrada principal. Recibe el texto que escribes en el panel de chat de n8n (`$json.chatInput`). |
| Agente de Triaje | AI Agent (LangChain) | Mismo agente de triaje: razona, usa herramientas y responde en el chat. |
| Gemini 2.5 Flash | LLM (Google Gemini) | Modelo Gemini con temperatura 0.2. |
| Buscar Póliza | Tool (Code) | Consulta mock de pólizas por número. |
| Buscar Liquidador | Tool (Code) | Asigna liquidador según ramo y severidad. |
| ¿Severidad Alta? | If (condicional) | Bifurca si la severidad es Alta. |
| Alerta Reaseguro | Code (JavaScript) | Escribe alerta en `data/alertas_reaseguro.md`. |
| Registro Log | Code (JavaScript) | Escribe registro en `data/log_triaje.md`. |

## Errores comunes

### "localhost refused to connect" o "no se puede acceder a este sitio"

n8n aún no ha terminado de iniciar. Espera a que la terminal muestre "n8n ready on 0.0.0.0, port 5678" e intenta de nuevo. Si ya apareció ese mensaje, verifica que escribiste la dirección correcta: `http://localhost:5678` (sin la "s" en http).

### El workflow no aparece en n8n

Los workflows no se abren automáticamente en el lienzo. Para encontrarlos, haz clic en el logotipo de n8n (esquina superior izquierda) y selecciona "Workflows". Busca **"Triaje de Siniestros — Agente IA"** o **"Triaje de Siniestros — Chat IA"**. Si no aparecen, reinicia el contenedor: presiona `Ctrl + C` en la terminal y ejecuta `docker compose up n8n --build` de nuevo.

### curl: command not found (en Windows)

Windows no siempre incluye curl. Alternativas:
- Usa PowerShell en vez de cmd (PowerShell sí incluye curl)
- O instala curl desde [https://curl.se/download.html](https://curl.se/download.html)

### "No credentials found for Gemini" o "Authentication failed"

La variable `GOOGLE_API_KEY` en el archivo `.env` no está definida o es incorrecta. Verifica que el archivo `.env` contenga una clave válida y reinicia el contenedor con `docker compose down && docker compose up n8n`.

### "No response received" en el chat

Si el chat muestra `[No response received. This could happen if streaming is enabled in the trigger but disabled in agent node(s)]`, el workflow de chat tiene un modo de respuesta incompatible. El workflow incluido usa `lastNode` para devolver la clasificación del agente después del registro en log. Reconstruye el contenedor para importar la versión corregida:

```bash
docker compose down && docker compose up n8n --build
```

### El agente responde con un error o no responde

Verifica que:
- El workflow está activado (toggle verde en la esquina superior derecha)
- La credencial de Gemini tiene una API Key válida
- Docker Desktop sigue abierto
