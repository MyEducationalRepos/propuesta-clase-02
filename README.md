# Clase 02: IA que actúa - Introducción a la IA Agéntica

Este proyecto contiene los materiales para la Clase 2 del programa de IA para Seguros (Insurex). Incluye dos ejemplos funcionales de un agente de triaje de siniestros: uno con código (Google ADK + Python) y otro visual sin código (n8n). El objetivo es que puedas ver cómo un agente de IA toma decisiones autónomas para clasificar siniestros, verificar pólizas y asignar liquidadores, todo sin intervención humana.

## Qué necesitas antes de empezar

Solo necesitas dos cosas:

1. **Docker Desktop** (un programa que permite ejecutar aplicaciones en "contenedores", que son como computadores virtuales dentro de tu computador)
2. **Una API Key de Google** (una clave de texto que le permite al programa comunicarse con la inteligencia artificial de Google)

No necesitas instalar Python, n8n, ni ninguna otra herramienta. Todo funciona dentro de Docker.

## Paso 1: Instalar Docker Desktop

Docker Desktop es una aplicación que se instala como cualquier otro programa.

1. Ve a [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/)
2. Haz clic en "Download for Mac" o "Download for Windows" según corresponda
3. Abre el archivo descargado e instálalo como cualquier otra aplicación (arrastra al folder Aplicaciones en Mac, o sigue el instalador en Windows)
4. Abre Docker Desktop después de instalarlo. Verás un icono de ballena en la barra superior (Mac) o en la bandeja del sistema (Windows). Déjalo abierto mientras trabajas con este proyecto.

## Paso 2: Obtener una API Key de Google

La API Key es una clave que permite que el programa se comunique con Gemini (la IA de Google).

1. Ve a [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Inicia sesión con tu cuenta de Google (la misma del correo Gmail)
3. Haz clic en el botón "Create API Key"
4. Google generará una clave larga (algo como `AIzaSyC...`). Cópiala y guárdala en un lugar seguro. La necesitarás en el siguiente paso.

## Paso 3: Abrir una terminal

La terminal es una ventana donde escribes comandos de texto para controlar tu computador. Es como darle instrucciones escritas en vez de hacer clic.

**En Mac:**
- Presiona `Cmd + Espacio` (se abre Spotlight, el buscador)
- Escribe `Terminal` y presiona Enter

**En Windows:**
- Presiona la tecla Windows
- Escribe `PowerShell` y presiona Enter

Verás una ventana con texto. Ahí es donde escribirás los comandos de los siguientes pasos.

## Paso 4: Descargar el proyecto

Tienes dos opciones:

**Opción A: Descargar como ZIP (más fácil)**
- Descarga el ZIP desde la página del repositorio
- Descomprímelo en una carpeta que recuerdes (por ejemplo, tu Escritorio)
- En la terminal, navega a esa carpeta. Por ejemplo:

```bash
cd ~/Desktop/propuesta-clase-02
```

El comando `cd` significa "cambiar de directorio" (change directory). Es como abrir una carpeta haciendo doble clic, pero por texto.

**Opción B: Clonar con git**

Si tienes git instalado, ejecuta:

```bash
git clone <url-del-repositorio>
cd propuesta-clase-02
```

El comando `git clone` descarga una copia completa del proyecto.

## Paso 5: Configurar la API Key

Necesitas crear un archivo de configuración con tu clave de Google.

Ejecuta este comando en la terminal (copia y pega):

```bash
cp .env.copy .env
```

Este comando copia el archivo `.env.copy` y lo renombra a `.env`. El archivo `.env` es donde guardarás tu clave secreta.

Ahora abre el archivo `.env` con cualquier editor de texto (TextEdit en Mac, Bloc de Notas en Windows) y reemplaza `your-key-here` por la API Key que copiaste en el Paso 2.

## Paso 6: Ejecutar un ejemplo

Ahora puedes elegir cuál ejemplo ejecutar.

### Ejemplo con código (ADK + Python)

Ejecuta este comando:

```bash
docker compose up adk
```

Esto le dice a Docker que construya y ejecute el agente de triaje. Docker descargará todo lo necesario automáticamente (la primera vez puede tardar unos minutos). Verás en la terminal cómo el agente procesa 6 casos de prueba de siniestros, mostrando su razonamiento paso a paso.

Cuando termine, la terminal se detendrá sola. Para más detalles, lee [examples/adk/README.md](examples/adk/README.md).

### Ejemplo visual (n8n)

Ejecuta este comando:

```bash
docker compose up n8n
```

Esto inicia n8n, una herramienta visual donde puedes ver el flujo del agente como un diagrama de cajas conectadas (sin escribir código). El workflow y la credencial de Gemini se configuran automáticamente al iniciar.

Cuando veas un mensaje que diga "n8n ready on 0.0.0.0, port 5678", abre tu navegador y ve a:

[http://localhost:5678](http://localhost:5678)

Verás una pantalla de inicio de sesión. Usa estas credenciales (ya vienen configuradas):

- **Correo:** `admin@clase.local`
- **Contraseña:** `clase02`

Después de iniciar sesión, los workflows importados no aparecen directamente en la pantalla. Para encontrarlos, haz clic en el logotipo de n8n (esquina superior izquierda), selecciona **"Workflows"** y abre:

- **"Triaje de Siniestros — Agente IA"** para ejecutar los 6 casos de prueba en lote
- **"Triaje de Siniestros — Chat IA"** para escribir un aviso nuevo en el chat y recibir la respuesta del agente

Para más detalles, lee [examples/n8n/README.md](examples/n8n/README.md).

## Estructura del proyecto

```
propuesta-clase-02/
├── .env.copy                              # Plantilla para tu clave de Google
├── docker-compose.yml                     # Archivo que coordina los contenedores
├── clase_02_fundamentos_ia_parte_b.md     # Propuesta de clase (plan completo)
├── examples/
│   ├── adk/                               # Ejemplo con código
│   │   ├── agente_triaje.py               # Código del agente de triaje
│   │   ├── pyproject.toml                 # Lista de dependencias
│   │   ├── Dockerfile                     # Instrucciones para construir el contenedor
│   │   └── README.md                      # Guía detallada de este ejemplo
│   └── n8n/                               # Ejemplo visual (sin código)
│       ├── workflow_triaje.json           # Workflow batch/webhook (importado al iniciar)
│       ├── workflow_triaje_chat.json      # Workflow chat interactivo
│       ├── init-workflows.sh             # Script que importa ambos workflows al iniciar
│       ├── Dockerfile                     # Instrucciones para construir el contenedor
│       └── README.md                      # Guía detallada de este ejemplo
├── data/                                  # Archivos de salida generados por n8n
│   ├── alertas_reaseguro.md              # Alertas para el reasegurador (solo alta severidad)
│   └── log_triaje.md                     # Registro de todos los siniestros procesados
└── openspec/                              # Especificaciones técnicas del proyecto
```

## Cómo detener todo

Cuando termines de trabajar, detén los contenedores con este comando:

```bash
docker compose down
```

Esto apaga todo limpiamente. No se pierde ningún archivo del proyecto.

Si quieres detener el proceso mientras está corriendo, presiona `Ctrl + C` en la terminal.

## Errores comunes y cómo solucionarlos

### "Cannot connect to the Docker daemon" o "docker: command not found"

Docker Desktop no está abierto. Abre la aplicación Docker Desktop y espera a que el icono de la ballena deje de moverse (significa que ya está listo). Luego intenta el comando de nuevo.

### "Error: API key not valid" o errores relacionados con la autenticación

Tu API Key de Google es incorrecta o no la copiaste bien. Abre el archivo `.env` y verifica que:
- No hay espacios extra antes ni después de la clave
- Copiaste la clave completa (empieza con `AIza...`)
- No dejaste el texto `your-key-here` sin reemplazar

### "port is already allocated" o "port 5678 already in use"

Otro programa está usando el mismo puerto. Esto puede pasar si ya ejecutaste `docker compose up n8n` en otra terminal. Soluciones:
- Ejecuta `docker compose down` para detener contenedores anteriores
- Cierra otras terminales que puedan tener el proyecto corriendo

### "no matching manifest for linux/arm64" (en Mac con chip M1/M2/M3)

Es poco frecuente con este proyecto, pero si aparece, asegúrate de tener Docker Desktop actualizado a la última versión.

### La descarga tarda mucho la primera vez

Es normal. Docker necesita descargar las "imágenes base" (como plantillas de sistema operativo). Esto solo ocurre la primera vez. Las siguientes ejecuciones serán mucho más rápidas.
