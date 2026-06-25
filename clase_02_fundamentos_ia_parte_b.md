# Clase 2: Fundamentos de la IA y Herramientas de Gemini Enterprise — Parte B

## Definición Estratégica

**Título:** IA que actúa: introducción a la inteligencia artificial agéntica

**Audiencia:** Profesionales, gerentes y líderes de equipo de la industria de seguros. Completaron la Clase 1: entienden qué es la IA generativa, cómo funciona un LLM, y conocen el ecosistema de herramientas Google.

**Promesa de empoderamiento:**
Al terminar esta sesión, entenderás por qué la IA agéntica es un cambio de paradigma y no solo una mejora incremental sobre los chatbots. Sabrás describir la arquitectura interna de un agente, reconocer los patrones de diseño que determinan su comportamiento, evaluar sus riesgos, y distinguir cuándo un proceso de seguros necesita un agente y cuándo basta con un prompt bien escrito. La última media hora pondrás las manos en un agente funcional que clasifica siniestros.

**Objetivos de aprendizaje:**

1. Explicar qué distingue a un agente de IA de un chatbot, usando los tres criterios operativos: uso de herramientas, toma de decisiones autónoma y ejecución en múltiples pasos.
2. Describir la arquitectura de un agente (modelo, instrucciones, herramientas, orquestación) y el rol que cumple cada componente.
3. Comparar los patrones de diseño agéntico (ReAct, planificación, reflexión, multi-agente) y evaluar cuál aplica a un proceso de seguros dado.
4. Identificar los modos de falla específicos de agentes (errores en cascada, uso inadecuado de herramientas, loops infinitos) y las estrategias para mitigarlos.

---

## Resumen Ejecutivo

Esta sesión establece el marco conceptual de la IA agéntica: qué es, cómo se estructura, qué patrones de diseño existen, y qué riesgos introduce. Se trabaja con profundidad teórica porque las decisiones de implementación dependen de entender la arquitectura, no de conocer una herramienta particular. En la última media hora se pasa de la teoría a la práctica con un agente funcional de triaje de siniestros que los participantes ejecutan, modifican y evalúan.

---

## Módulo 1: El paradigma agéntico — Qué cambia y por qué importa
**Duración:** 30 minutos

### Concepto Clave
La IA generativa que usamos hasta ahora es reactiva: responde cuando le preguntas y se detiene cuando termina de responder. La IA agéntica opera con un objetivo: recibe una meta, decide qué pasos dar, usa herramientas, observa los resultados, y ajusta su plan hasta completar la tarea. La diferencia no es el modelo. Es la arquitectura que lo rodea.

### Puntos de Enseñanza

1. **El espectro de autonomía — cuatro niveles:**

   En la práctica, las aplicaciones de IA no son binarias ("chatbot o agente"). Existen niveles intermedios, y entender dónde cae cada solución ayuda a calibrar expectativas y riesgos.

   **Nivel 1 — Prompt simple:** Un usuario escribe una instrucción, el modelo responde en un turno. Sin herramientas, sin memoria, sin decisiones. Ejemplo en seguros: "Redacta un correo de acuse de recibo de siniestro." Útil para tareas atómicas.

   **Nivel 2 — Cadena (Chain):** Varios prompts encadenados, donde el output de uno alimenta al siguiente. La secuencia es fija, definida por el programador. Ejemplo: leer un aviso de siniestro → extraer campos → generar un resumen estructurado. No hay decisión del modelo sobre qué paso ejecutar; el flujo es determinístico.

   **Nivel 3 — Agente:** Un modelo con acceso a herramientas y capacidad de decidir qué hacer en cada paso. El flujo no es fijo: depende de lo que el modelo observe. Si la póliza está vigente, sigue un camino; si está vencida, sigue otro. El modelo razona, actúa, observa, y vuelve a razonar.

   **Nivel 4 — Sistema multi-agente:** Varios agentes especializados que colaboran. Un orquestador distribuye tareas: uno analiza la póliza, otro evalúa el siniestro, otro redacta la comunicación. Cada sub-agente tiene sus propias herramientas e instrucciones.

   La mayoría de las implementaciones actuales operan en los niveles 2 y 3. El nivel 4 existe pero es más complejo de implementar y gobernar.

2. **Tres criterios para distinguir un agente de un chatbot:**

   Criterio 1 — **Uso de herramientas:** Un chatbot genera texto. Un agente genera texto Y ejecuta acciones en sistemas externos: consulta una base de datos de pólizas, escribe en una planilla de siniestros, envía un correo al reasegurador. Las herramientas son la interfaz entre el modelo y el mundo real.

   Criterio 2 — **Toma de decisiones autónoma:** Un chatbot responde lo que le preguntas. Un agente evalúa la situación y decide qué hacer. Si detecta que faltan datos, pide más información antes de continuar. Si la severidad es alta, agrega una acción (notificar al reasegurador) que no ejecutaría en un caso de baja severidad. La bifurcación ocurre dentro del agente, no por programación externa.

   Criterio 3 — **Ejecución en múltiples pasos:** Un chatbot opera en un turno (input → output). Un agente encadena pasos donde cada resultado influye en el siguiente: leer aviso → extraer número de póliza → consultar estado → si vigente, clasificar severidad → buscar liquidador → registrar → responder. El número de pasos no es fijo: depende del caso.

3. **La analogía operativa:**

   Un chatbot es como un asistente que solo responde preguntas que le haces por escrito. Le preguntas algo, te responde, y ahí termina.

   Un agente es como un empleado al que le asignas una tarea. Le dices "procesa estos avisos de siniestro." El empleado lee cada aviso, busca la póliza en el sistema, clasifica la severidad según los criterios que le enseñaste, asigna al liquidador correspondiente, y te avisa si algo requiere tu atención directa. Toma decisiones dentro del marco que le definiste. Si algo se sale de su competencia, se detiene y te consulta.

   La calidad del trabajo del empleado depende de tres cosas: qué tan claras son las instrucciones que le diste, qué herramientas tiene a su disposición, y qué tan bien definidos están los límites de su autonomía. Lo mismo aplica a un agente.

4. **¿Por qué ahora? Qué habilitó la IA agéntica:**

   Los agentes como concepto no son nuevos. La investigación en sistemas multi-agente tiene décadas (arquitectura BDI, planificación automatizada, sistemas expertos). Lo que cambió en 2023-2025 es que los LLM demostraron ser capaces de:

   - Interpretar instrucciones en lenguaje natural con suficiente fiabilidad para tomar decisiones operativas.
   - Decidir cuándo y cómo usar herramientas a partir de descripciones textuales (function calling).
   - Razonar paso a paso de forma coherente a lo largo de una secuencia de acciones.
   - Manejar ambigüedad y casos no previstos con un nivel aceptable de sensatez.

   El modelo no cambió fundamentalmente; lo que cambió fue la confianza (aún parcial) en su capacidad de operar como motor de decisión dentro de un sistema más amplio.

5. **Dónde encaja esto en seguros — primeros candidatos:**

   Los procesos con mayor afinidad agéntica en una aseguradora comparten cuatro características: volumen alto (se ejecutan decenas o cientos de veces por semana), pasos secuenciales (un resultado alimenta al siguiente), decisiones condicionales (si X entonces Y), y acceso a datos externos (sistemas core, planillas, correos).

   Candidatos naturales: triaje de avisos de siniestro, pre-evaluación de solicitudes de seguro, gestión de renovaciones, monitoreo de cumplimiento normativo, verificación de cobertura ante consultas de corredores. Todos cumplen las cuatro condiciones.

   Candidatos que NO necesitan un agente: generar un correo individual, resumir un documento, traducir un texto. Estas son tareas de un solo paso donde un prompt bien construido es suficiente.

### Recursos de Apoyo

**Diapositiva 1 — Espectro de autonomía:**
Diagrama con los 4 niveles (prompt → cadena → agente → multi-agente), con un ejemplo de seguros en cada nivel.

**Diapositiva 2 — "Responder vs. Actuar":**
Pantalla dividida en dos mitades. Izquierda en tono oscuro (gris azulado), derecha con color (azul o verde profundo). Cada mitad cuenta la misma micro-historia: un aviso de siniestro llega a la compañía.

Mitad izquierda, titulada "Usar un LLM": Un rectángulo arriba con el texto del aviso ("Incendio en bodega, póliza POL-2024-001, 3000 UF"). Una flecha única, recta, hacia abajo. Un bloque de respuesta genérica: texto corrido, sin estructura, sin datos verificados. Debajo, en letra chica: "No consultó la póliza. No verificó vigencia. No asignó liquidador. No registró nada." El tono visual es estático: una pregunta, una respuesta, fin de la historia.

Mitad derecha, titulada "Usar un Agente": El mismo aviso de siniestro arriba. En vez de una flecha recta, un flujo con 5 pasos visibles encadenados, cada uno con un ícono minimalista en estilo line art:
Paso 1, ícono de lupa: "Lee el aviso, extrae póliza"
Paso 2, ícono de base de datos: "Consulta sistema: vigente, Incendio"
Paso 3, ícono de balanza: "Clasifica: 3000 UF, severidad Alta"
Paso 4, ícono de persona: "Asigna: María González, Senior"
Paso 5, ícono de sobre: "Genera aviso al reasegurador"
Al final, un bloque de respuesta estructurada (PÓLIZA / RAMO / SEVERIDAD / LIQUIDADOR / AVISO REASEGURADOR), visualmente limpio. Debajo: "Consultó datos reales. Tomó decisiones. Ejecutó acciones. Dejó registro."

Al pie de la slide, una línea horizontal que cruza ambas mitades con una escala:
Extremo izquierdo: "TÚ HACES TODO — el modelo redacta"
Extremo derecho: "EL AGENTE HACE TODO — tú supervisas"

Diseño: sin texto largo. Cada paso del lado derecho tiene máximo 6 palabras. El contraste visual entre la flecha solitaria de la izquierda y el flujo de 5 pasos de la derecha es el mensaje. La slide tiene que funcionar aunque el presentador no diga nada durante 5 segundos.

---

## Módulo 2: Arquitectura y patrones de diseño — Cómo se construye un agente por dentro
**Duración:** 30 minutos

### Concepto Clave
Todos los agentes de IA, independientemente de la herramienta con la que se construyan, comparten una arquitectura de cuatro componentes y operan en un ciclo de razonamiento-acción. Entender esa estructura permite evaluar cualquier implementación, diagnosticar fallas, y tomar decisiones informadas sobre diseño.

### Puntos de Enseñanza

1. **Los cuatro componentes de todo agente:**

   **Componente 1 — Modelo base (el razonador):** El LLM que procesa la información y decide qué hacer. Es el único componente que "razona" (en el sentido estadístico de predicción de tokens). Todo lo demás es infraestructura alrededor del modelo. La elección del modelo afecta la calidad del razonamiento, la velocidad, el costo, y la capacidad de seguir instrucciones complejas. No todos los modelos sirven para agentes: se necesita un modelo con buena capacidad de function calling y de seguir instrucciones multi-paso.

   **Componente 2 — Instrucciones (el mandato):** Un bloque de texto que define quién es el agente, qué puede hacer, cómo debe actuar, y qué tiene prohibido. Es la descripción de cargo del agente. Las instrucciones determinan la calidad del comportamiento mucho más que la elección del modelo. Un modelo mediocre con instrucciones excelentes supera a un modelo superior con instrucciones vagas.

   Qué incluyen las instrucciones de un agente de seguros: el rol ("Eres un agente de triaje de siniestros"), el proceso paso a paso, los criterios de clasificación (umbrales de severidad, reglas especiales para catástrofes), el formato de respuesta, las restricciones ("nunca inventes datos"), y las condiciones de parada ("si faltan datos, pide antes de clasificar").

   **Componente 3 — Herramientas (las manos):** Funciones que el agente puede invocar para interactuar con el mundo exterior. Cada herramienta tiene un nombre, una descripción en lenguaje natural, y parámetros de entrada y salida. El modelo NO ejecuta la herramienta directamente: emite una señal ("quiero usar la herramienta X con estos parámetros"), el orquestador la ejecuta, y el resultado vuelve al modelo.

   La descripción de la herramienta es crítica. El modelo decide cuándo usarla leyendo esa descripción. Si dice "Consulta el estado de una póliza por su número. Usar siempre que el aviso mencione un número de póliza", el modelo sabrá cuándo invocarla. Si dice "Herramienta de pólizas", no sabrá cuándo ni cómo. Escribir buenas descripciones de herramientas es ingeniería de prompts aplicada a la interfaz modelo-herramienta.

   **Componente 4 — Orquestación (el motor):** El sistema que coordina el ciclo de ejecución. Recibe la respuesta del modelo, detecta si hay una invocación de herramienta, la ejecuta, alimenta el resultado de vuelta al modelo, y repite hasta que el modelo indica que terminó. El orquestador también maneja errores (qué pasa si la herramienta falla), límites (máximo de iteraciones para evitar loops infinitos), y trazabilidad (registrar cada paso para auditoría).

2. **El ciclo ReAct — Razonamiento + Acción:**

   El patrón más común de operación agéntica. El acrónimo viene de "Reasoning + Acting." El ciclo tiene cuatro fases que se repiten:

   **Pensar:** El modelo analiza la situación actual. "Tengo un aviso de siniestro. Menciona la póliza POL-2024-001. Necesito verificar si está vigente antes de clasificar."

   **Actuar:** El modelo emite una invocación de herramienta. "Llamar a consultar_poliza con parámetro POL-2024-001."

   **Observar:** El orquestador ejecuta la herramienta y devuelve el resultado. "Estado: Vigente. Ramo: Incendio. Suma asegurada: 500M CLP."

   **Razonar de nuevo:** El modelo integra la observación y decide el siguiente paso. "La póliza está vigente, ramo Incendio. El monto estimado es 3000 UF, mayor a 2000 UF: severidad Alta. Necesito asignar un liquidador senior."

   El ciclo se repite hasta que el modelo determina que la tarea está completa y emite una respuesta final en lugar de una invocación de herramienta.

   Este ciclo es visible en los logs de ejecución. Cuando un agente se equivoca, leer el log de ReAct permite identificar en qué paso tomó una decisión incorrecta: ¿razonó mal? ¿La herramienta devolvió datos erróneos? ¿Interpretó mal el resultado? La trazabilidad del loop ReAct es lo que hace a un agente auditable.

3. **Otros patrones de diseño agéntico:**

   **Plan-and-Execute (Planificar y Ejecutar):** A diferencia de ReAct (que razona paso a paso), este patrón genera primero un plan completo y luego lo ejecuta secuencialmente. Útil cuando el proceso tiene muchos pasos y el orden importa. Ejemplo: evaluar un riesgo nuevo requiere un plan de 8 pasos (obtener datos del solicitante, verificar antecedentes, consultar tablas de riesgo, calcular prima tentativa, verificar capacidad, consultar restricciones regulatorias, generar propuesta, enviar al suscriptor). El agente genera el plan al inicio y luego ejecuta cada paso.

   **Reflexión (Self-Correction):** El agente revisa su propio output antes de entregarlo. Después de generar una clasificación de siniestro, una segunda pasada evalúa: "¿Usé correctamente los criterios de severidad? ¿La asignación de liquidador es coherente con el ramo?" Si detecta un error, corrige antes de responder. Aumenta la calidad a costa de mayor latencia y costo.

   **Multi-Agente (Delegación):** Un agente orquestador distribuye sub-tareas a agentes especializados. Agente 1 analiza la póliza, Agente 2 clasifica el siniestro, Agente 3 redacta la comunicación. Cada sub-agente tiene sus propias instrucciones y herramientas. El orquestador integra los resultados. Este patrón aplica a procesos complejos donde la especialización mejora la calidad, pero introduce complejidad en la coordinación.

4. **Memoria — el problema del contexto persistente:**

   Los LLM no recuerdan nada entre sesiones. Cada ejecución parte de cero. Para un agente que procesa siniestros, esto significa que no "aprende" de casos anteriores a menos que se implemente un mecanismo de memoria explícito.

   **Memoria de corto plazo:** La conversación actual. Funciona dentro de una sesión. Permite al agente recordar lo que dijo hace tres turnos. Se agota cuando la conversación excede la ventana de contexto del modelo.

   **Memoria de largo plazo:** Un almacenamiento externo (base de datos, vector store) donde el agente guarda y recupera información entre sesiones. Ejemplo: un agente que recuerda que la póliza POL-2024-001 tuvo 3 siniestros en los últimos 12 meses, porque consultó esa información en ejecuciones anteriores y la almacenó.

   La memoria de largo plazo no es estándar en la mayoría de las implementaciones actuales. Requiere diseño deliberado: qué guardar, cuándo consultarlo, cómo evitar que información desactualizada contamine las decisiones.

5. **El diseño de la interfaz humano-agente:**

   El grado de autonomía del agente no es técnico; es una decisión de negocio. Se define en función del riesgo: ¿qué pasa si el agente se equivoca?

   **Autonomía total (sin supervisión):** El agente ejecuta de principio a fin sin intervención humana. Apropiado solo para tareas donde el costo del error es bajo y reversible. Ejemplo: clasificar correos entrantes por categoría.

   **Human-in-the-loop (humano en el circuito):** El agente ejecuta hasta un punto de decisión crítico y se detiene hasta que un humano aprueba. Ejemplo: el agente clasifica el siniestro y asigna liquidador, pero el liquidador senior debe aprobar antes de que se notifique al reasegurador.

   **Human-on-the-loop (humano supervisando):** El agente ejecuta de principio a fin, pero un humano revisa los resultados periódicamente (cada hora, cada batch, cada día). Ejemplo: el agente procesa 40 avisos diarios; un supervisor revisa un muestreo del 20% al final del día.

   En seguros, donde las decisiones tienen consecuencias financieras y legales, la recomendación es empezar con human-in-the-loop y migrar gradualmente a human-on-the-loop cuando la tasa de error del agente sea consistentemente baja.

### Recursos de Apoyo
Diapositiva con el ciclo ReAct (Pensar → Actuar → Observar → Razonar de nuevo) como un diagrama circular con un ejemplo de triaje de siniestros en cada fase. Segunda diapositiva con los tres niveles de autonomía (total, in-the-loop, on-the-loop) y la relación con el nivel de riesgo.

---

## Módulo 3: Riesgos, evaluación y caminos de implementación
**Duración:** 20 minutos

### Concepto Clave
Un agente de IA introduce modos de falla que no existen en un chatbot. Entenderlos antes de implementar evita sorpresas costosas. A esto se suma la necesidad de evaluar al agente con el mismo rigor con el que se evaluaría a un empleado nuevo: casos de prueba, situaciones límite, y criterios claros de aceptación.

### Puntos de Enseñanza

1. **Modos de falla específicos de agentes:**

   **Error en cascada:** El agente toma una decisión incorrecta en el paso 2, y esa decisión contamina todos los pasos siguientes. Ejemplo: clasifica mal el ramo del siniestro (dice "Vehículo" cuando es "Incendio") y asigna un liquidador que no tiene competencia en ese tipo de siniestro. En un chatbot, el error afecta una respuesta. En un agente, el error se propaga.

   Mitigación: validación intermedia. En pasos críticos, verificar el output del agente contra reglas determinísticas antes de continuar. Si el ramo que el agente asignó no coincide con el ramo de la póliza consultada, detener la ejecución.

   **Uso inadecuado de herramientas:** El agente decide usar una herramienta cuando no debería, o la usa con parámetros incorrectos. Ejemplo: invoca la herramienta de asignación de liquidador antes de haber consultado la póliza, y asigna basándose en datos inventados.

   Mitigación: descripciones de herramientas que especifiquen pre-condiciones ("Usar después de haber verificado la vigencia de la póliza"). Restricciones en las instrucciones del agente que definan el orden obligatorio.

   **Loop infinito:** El agente entra en un ciclo donde repite los mismos pasos sin avanzar. Ejemplo: pide un dato al usuario, interpreta la respuesta como insuficiente, vuelve a pedir el mismo dato. Esto consume recursos y bloquea la ejecución.

   Mitigación: límite máximo de iteraciones en el orquestador (por ejemplo, máximo 10 ciclos). Si el agente no ha completado la tarea en ese límite, se detiene y escala a un humano.

   **Alucinación agéntica:** El agente genera datos que no provienen de las herramientas y los usa como si fueran reales. Ejemplo: en lugar de llamar a la herramienta de consulta de póliza, el agente "inventa" que la póliza está vigente y continúa procesando.

   Mitigación: instrucciones explícitas ("Nunca inventes datos que no provengan de las herramientas"), verificación del log para confirmar que las herramientas se invocaron, y auditoría de las respuestas contra los datos reales del sistema.

2. **Cómo evaluar un agente — el enfoque de testing:**

   Evaluar un agente es como evaluar a un empleado durante su período de prueba. Se necesitan casos de prueba que cubran el rango completo de situaciones que enfrentará:

   **Casos estándar:** El escenario más común, donde todo funciona según lo esperado. Si el agente falla aquí, las instrucciones básicas están mal.

   **Casos límite (edge cases):** Situaciones en el borde de las reglas. Un monto de exactamente 500 UF: ¿es "Baja" o "Media"? Una póliza que vence hoy a medianoche: ¿está vigente o no? Estos casos revelan ambigüedades en las instrucciones.

   **Casos de error:** Datos faltantes, pólizas inexistentes, formatos inesperados. El agente debe manejarlos con gracia (pedir más datos, informar que no puede procesar) en lugar de fallar silenciosamente o inventar.

   **Casos adversariales:** Inputs diseñados para confundir al agente. Un aviso que contiene dos números de póliza. Un texto ambiguo que podría ser un siniestro o una consulta general. Estos casos revelan la robustez del agente frente a la variabilidad del mundo real.

   Un agente no está listo para producción hasta que pasa los cuatro tipos de casos con una tasa de acierto aceptable para el negocio. ¿Cuál es "aceptable"? Depende del riesgo: para triaje preliminar (que un humano revisará después), 90% puede ser suficiente. Para decisiones con impacto financiero directo, 99% puede ser insuficiente.

3. **Dos caminos de implementación:**

   **Camino visual (sin código):** Plataformas como n8n permiten construir agentes conectando nodos en un canvas. El nodo de "AI Agent" contiene el modelo y las instrucciones; los nodos de herramientas conectan con Google Sheets, Gmail, APIs. El resultado es un flujo visual donde cada paso es observable. Apto para equipos de negocio que quieren prototipar rápido sin dependencia técnica. Se entrega un archivo JSON importable con el workflow de ejemplo (ver `ejemplo_workflow_n8n.json`).

   **Camino con código (Python):** Frameworks como Google ADK permiten definir agentes con control total sobre la lógica. Las herramientas son funciones Python, las instrucciones son cadenas de texto, y la ejecución se controla programáticamente. Mayor flexibilidad, mayor complejidad. Apto para equipos técnicos o proyectos que requieren integración profunda con sistemas internos. Se entrega un archivo Python con el agente completo (ver `ejemplo_agente_adk.py`).

   Ambos resuelven el mismo problema. La elección depende de tres factores: si hay desarrolladores disponibles, qué tan compleja es la lógica de negocio, y a qué escala operará el agente. La recomendación general: prototipar en el camino visual, escalar con código.

4. **La progresión realista:**

   Etapa 1 — Validar la idea (horas): Probar si el modelo puede seguir las instrucciones y usar las herramientas correctamente con 5-10 casos de prueba. Se hace en un entorno de laboratorio.

   Etapa 2 — Piloto controlado (semanas): Ejecutar el agente con datos reales pero con supervisión humana en cada paso. Medir tasa de acierto, identificar fallas, iterar las instrucciones.

   Etapa 3 — Producción supervisada (meses): El agente opera con volumen real. Un humano revisa un muestreo de los resultados. Se monitorean métricas de calidad, latencia y costo.

   Etapa 4 — Operación autónoma (si se justifica): El agente opera sin revisión caso a caso. Se mantiene monitoreo automatizado (alertas cuando la tasa de error sube, cuando el modelo cambia de comportamiento por una actualización del proveedor, cuando cambian los datos del negocio).

### Recursos de Apoyo
Diapositiva con la matriz de modos de falla (error en cascada, uso inadecuado de herramientas, loop infinito, alucinación agéntica) con un ejemplo de seguros para cada uno y su mitigación en una línea.

---

## Aplicación Práctica — Industria de Seguros
**Duración:** 30 minutos

### Caso: Triaje de siniestros con un agente funcional

**Contexto:**
La compañía de seguros "Protección Nacional" recibe entre 30 y 50 avisos de siniestro diarios. Un ejecutivo lee cada aviso, busca la póliza en el sistema, clasifica la severidad, busca al liquidador disponible, y registra todo en una planilla. El proceso toma entre 10 y 15 minutos por aviso.

Se construyó un agente de triaje que automatiza este proceso. Los participantes van a ejecutarlo, evaluarlo, y mejorarlo.

**Material:**
Los participantes trabajan con el archivo `ejemplo_agente_adk.py` en Google Colab (el facilitador comparte el notebook con el código pre-cargado). El agente tiene tres herramientas: consultar póliza, asignar liquidador, y registrar clasificación.

**Avisos de prueba (cubren los 4 tipos de evaluación del Módulo 3):**

Aviso 1 — Caso estándar:
"Se reporta robo con fractura de ventanal en sucursal de farmacia. Póliza POL-2024-003. Sustrajeron equipos computacionales. Valor estimado 300 UF. Sin heridos."
→ Esperado: Póliza vigente, RC, severidad Baja, Pool General.

Aviso 2 — Caso de error (póliza inexistente):
"Filtración de agua en oficina del tercer piso. Daño a servidores y mobiliario. Póliza POL-2024-099. Monto estimado 1200 UF."
→ Esperado: El agente informa que la póliza no existe. No clasifica.

Aviso 3 — Caso estándar + acción adicional (alta severidad):
"Explosión en caldera de edificio industrial. Daño estructural severo en el ala norte. Póliza POL-2024-001. Estimación preliminar: 8000 UF. Dos trabajadores con quemaduras leves evacuados al hospital."
→ Esperado: Póliza vigente, Incendio, severidad Alta, liquidador senior, aviso al reasegurador.

Aviso 4 — Caso de error (datos incompletos):
"Cliente llama para avisar que chocaron su auto estacionado. No tiene el número de póliza a mano. Dice que el daño es considerable."
→ Esperado: El agente solicita el número de póliza. No clasifica con datos insuficientes.

**Ejercicio paso a paso:**

Paso 1 — Ejecutar los 4 avisos (10 min):
Cada participante corre el agente con los 4 avisos y registra en un Google Sheet compartido: número de aviso, clasificación del agente, ¿es correcta? (sí/no), observación.

Paso 2 — Leer el log de ReAct (5 min):
Para el Aviso 3 (el más complejo), revisar el log de ejecución del agente. Identificar: ¿cuántas herramientas invocó? ¿En qué orden? ¿Dónde razonó correctamente? ¿Inventó algún dato?

Paso 3 — Modificar y re-testear (10 min):
Elegir una de estas mejoras y aplicarla:
- Agregar la regla de terremoto a las instrucciones ("Si el siniestro es por terremoto o sismo, clasificar siempre como Alta, agregar nota: Activar protocolo de catástrofe").
- Agregar una póliza nueva al diccionario de datos (POL-2024-004, Transporte, vigente) y probar con un aviso de volcamiento de camión.
Ejecutar de nuevo y verificar que la mejora funcione sin romper los otros casos.

Paso 4 — Reflexión (5 min):
Discusión guiada: ¿Cuánto tiempo tomó procesar 4 avisos con el agente? ¿Cuánto tomaría manualmente? ¿El agente manejó bien los errores? ¿Dónde pondrían el checkpoint humano? ¿Qué herramientas adicionales necesitaría para operar en producción?

### Criterio de éxito
El participante procesa los 4 avisos, el agente clasifica correctamente al menos 3, y el participante identifica en el log de ReAct los pasos de razonamiento y las invocaciones de herramientas.

---

## Mecanismos de Evaluación

**1. Quiz conceptual (3 preguntas):**

Pregunta 1: Un agente de IA se distingue de un chatbot porque:
a) Usa un modelo de lenguaje más avanzado → Incorrecto
b) Puede usar herramientas, tomar decisiones autónomas y ejecutar múltiples pasos → Correcto
c) Tiene una interfaz visual más sofisticada → Incorrecto

Pregunta 2: En el ciclo ReAct, después de que el agente observa el resultado de una herramienta, el siguiente paso es:
a) Ejecutar la siguiente herramienta en orden → Incorrecto
b) Razonar sobre el resultado y decidir qué hacer a continuación → Correcto
c) Entregar la respuesta final al usuario → Incorrecto

Pregunta 3: Un agente clasifica un siniestro incorrectamente porque consultó la póliza pero interpretó mal el ramo. Este tipo de error se llama:
a) Loop infinito → Incorrecto
b) Error en cascada → Correcto
c) Alucinación agéntica → Incorrecto

**2. Evaluación del ejercicio práctico:**
El Google Sheet compartido permite al facilitador verificar si los participantes identificaron correctamente las clasificaciones del agente y detectaron los errores.

**3. Reflexión de cierre:**
Cada participante escribe: "Un proceso de mi organización que podría beneficiarse de un agente es: _______ porque cumple los criterios de: _______." Se recogen para la Clase 5.

---

## Anticipación de Dudas — FAQ del Facilitador

**Pregunta probable 1:** "¿Cuánto cuesta operar un agente? Cada herramienta que invoca consume tokens."
**Respuesta:** Sí, cada ciclo de razonamiento y cada invocación de herramienta consume tokens del modelo. Un agente que hace 5 invocaciones de herramientas consume aproximadamente 3-5x más tokens que un prompt simple. Con los modelos más eficientes (Gemini Flash, Claude Haiku), el costo por ejecución de un agente de triaje de siniestros está en el rango de fracciones de centavo de dólar. Para 40 avisos diarios, el costo mensual es marginal comparado con las horas-persona que reemplaza. El costo relevante no es el de tokens: es el de construir, probar y mantener el agente.

**Pregunta probable 2:** "¿Qué pasa si el proveedor del modelo cambia algo y el agente empieza a fallar?"
**Respuesta:** Es un riesgo real. Los proveedores actualizan sus modelos periódicamente, y una actualización puede cambiar el comportamiento del agente de maneras sutiles (clasifica diferente, invoca herramientas en otro orden, interpreta las instrucciones de forma distinta). La mitigación es: tener un conjunto de casos de prueba automatizados (los mismos 4 avisos del ejercicio, más otros) y ejecutarlos periódicamente. Si la tasa de acierto baja, revisar y ajustar las instrucciones. Algunos equipos fijan la versión del modelo para evitar cambios no controlados.

**Pregunta probable 3:** "¿Necesito un equipo de datos para implementar esto?"
**Respuesta:** Depende del alcance. Un prototipo funcional como el del ejercicio se construye en horas con un desarrollador. Para producción se necesita: un desarrollador que conecte el agente a los sistemas reales (API de pólizas, correo, sistema de siniestros), alguien de seguridad de la información que evalúe los datos que se envían al modelo, y alguien del negocio que defina las reglas, pruebe los resultados, e itere las instrucciones. El equipo mínimo es 3 personas: negocio, desarrollo, seguridad.

---

## Cierre y Próximos Pasos

**Transición a la Clase 3:** La próxima sesión toma las herramientas de Google AI (Gemini en Workspace, NotebookLM, AI Studio) y las encadena en flujos de trabajo integrados para procesos complejos de seguros: desde la recepción de un documento hasta la entrega de un análisis al cliente.

**Tarea inter-sesión (opcional pero recomendada):**
1. Abrir el notebook de Colab y agregar una tercera herramienta al agente: una función que genere el texto de un correo de acuse de recibo dirigido al asegurado. Modificar las instrucciones para que el agente la invoque automáticamente al completar el triaje.
2. Identificar un proceso de tu organización que cumpla los 4 criterios de candidato agéntico (volumen, pasos secuenciales, decisiones condicionales, acceso a datos externos). Describir en un párrafo qué haría el agente, qué herramientas necesitaría, y dónde pondrías el checkpoint humano.

**Archivos de referencia distribuidos:**
- `ejemplo_agente_adk.py` — agente completo en Python con Google ADK
- `ejemplo_workflow_n8n.json` — workflow importable para n8n

---

## Contribuciones

Al completar esta sesión, el participante:

- Ubica cualquier aplicación de IA en el espectro de autonomía (prompt → cadena → agente → multi-agente) y sabe qué implica cada nivel.
- Describe la arquitectura de un agente con sus cuatro componentes y puede evaluar si una implementación los tiene todos.
- Reconoce los patrones de diseño agéntico (ReAct, planificación, reflexión, multi-agente) y evalúa cuál aplica a un proceso dado.
- Identifica los cuatro modos de falla de agentes y las estrategias de mitigación para cada uno.
- Ha ejecutado un agente funcional, leído su log de razonamiento, y modificado sus reglas de negocio para verificar el cambio de comportamiento.
- Tiene criterios claros para evaluar si un proceso de seguros necesita un agente o si basta con un enfoque más simple.
