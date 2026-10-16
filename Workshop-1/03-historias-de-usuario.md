# 3. Historias de usuario

## Visitante

### HU-01 Consultar la programación de la jornada

*R1 · Seguir el torneo · Prioridad alta*

Como visitante, quiero ver la programación de la jornada por categoría para saber cuándo y en qué cancha juega el equipo que me interesa.

**Criterios de aceptación:**

- CA1. **Dado que** la organización aprobó la programación de la jornada, **cuando** el visitante elige una categoría, **entonces** ve los partidos con fecha, hora, cancha y equipos, ordenados por hora.
- CA2. **Dado que** un partido todavía no tiene programación aprobada, **cuando** el visitante consulta la jornada, **entonces** el partido aparece como «Por programar», sin cancha ni hora.

### HU-02 Consultar los resultados

*R1 · Seguir el torneo · Prioridad alta*

Como visitante, quiero ver los resultados de la jornada con sus goleadores para enterarme de cómo le fue a cada equipo.

**Criterios de aceptación:**

- CA1. **Dado que** un partido tiene resultado aprobado por la organización, **cuando** el visitante abre la jornada, **entonces** ve el marcador final y los goleadores de cada equipo.
- CA2. **Dado que** un resultado está en revisión, **cuando** el visitante lo consulta, **entonces** ve el marcador con la etiqueta «Provisional».

### HU-03 Consultar la tabla de posiciones

*R1 · Seguir el torneo · Prioridad alta*

Como visitante, quiero ver la tabla de posiciones de cada grupo para saber qué equipos van clasificando.

**Criterios de aceptación:**

- CA1. **Dado que** un grupo tiene partidos jugados, **cuando** el visitante abre la tabla del grupo, **entonces** ve PJ, PG, PE, PP, GF, GC, DG y puntos, ordenados con los criterios de desempate del reglamento.
- CA2. **Dado que** un equipo del grupo se retiró, **cuando** el visitante abre la tabla, **entonces** el equipo aparece al final marcado como «Retirado».

### HU-04 Consultar goleadores y valla menos vencida

*R1 · Seguir el torneo · Prioridad media*

Como visitante, quiero ver los goleadores y la valla menos vencida de cada categoría para seguir los premios individuales.

**Criterios de aceptación:**

- CA1. **Dado que** hay goles registrados en la categoría, **cuando** el visitante abre «Goleadores», **entonces** ve a cada jugador con su nombre, su equipo y su número de goles, sin documento, fecha de nacimiento ni foto.

### HU-05 Consultar los documentos del torneo

*R1 · Informarse · Prioridad alta*

Como visitante, quiero consultar el reglamento, las resoluciones y los comunicados para conocer las reglas y las decisiones de la organización.

**Criterios de aceptación:**

- CA1. **Dado que** la organización marcó un documento como público, **cuando** el visitante entra a «Documentos», **entonces** puede verlo en pantalla y descargarlo en PDF.
- CA2. **Dado que** un documento está dirigido solo a delegados, **cuando** el visitante entra a «Documentos», **entonces** ese documento no aparece.

### HU-06 Instalar la aplicación

*R1 · Llevar el torneo en el celular · Prioridad alta*

Como visitante, quiero instalar la página como aplicación en mi celular para abrir el torneo con un toque.

**Criterios de aceptación:**

- CA1. **Dado que** el visitante abre la página en Android, **cuando** pulsa «Instalar aplicación», **entonces** queda un ícono con la marca de la organización que abre la aplicación a pantalla completa.
- CA2. **Dado que** el visitante abre la página en un iPhone, **cuando** pulsa «Instalar aplicación», **entonces** ve los pasos para agregarla a la pantalla de inicio desde Safari.

### HU-07 Ver la ficha de un equipo

*R2 · Conocer equipos y clubes · Prioridad media*

Como visitante, quiero ver la ficha de un equipo para tener en un solo lugar su calendario, sus resultados y su posición.

**Criterios de aceptación:**

- CA1. **Dado que** el visitante busca un equipo por su nombre, **cuando** abre su ficha, **entonces** ve escudo, categoría, grupo, posición actual, próximos partidos y resultados.

### HU-08 Ver la ficha de un club

*R2 · Conocer equipos y clubes · Prioridad baja*

Como visitante, quiero ver la ficha de un club para conocer todos sus equipos en el torneo.

**Criterios de aceptación:**

- CA1. **Dado que** un club tiene equipos en varias categorías, **cuando** el visitante abre la ficha del club, **entonces** ve sus equipos agrupados por categoría, cada uno con enlace a su ficha.

### HU-09 Leer las noticias

*R2 · Informarse · Prioridad media*

Como visitante, quiero leer las noticias de la organización para enterarme de las novedades del torneo.

**Criterios de aceptación:**

- CA1. **Dado que** la organización publicó noticias, **cuando** el visitante entra a «Noticias», **entonces** las ve de la más reciente a la más antigua y puede compartir cada una con su vista previa.

### HU-10 Ver la galería de la jornada

*R2 · Informarse · Prioridad baja*

Como visitante, quiero ver las fotos y las piezas de cada jornada para revivir los partidos.

**Criterios de aceptación:**

- CA1. **Dado que** la organización publicó el álbum de una jornada, **cuando** el visitante abre la galería de esa jornada, **entonces** ve las fotos y las piezas de programación y resultados de ese día.

### HU-11 Ver el torneo en la página web de la organización

*R2 · Llevar el torneo en el celular · Prioridad media*

Como visitante de la página web de la organización, quiero ver la tabla y los próximos partidos sin salir de esa página para seguir el torneo desde donde ya estoy.

**Criterios de aceptación:**

- CA1. **Dado que** la organización insertó el widget de tabla de una categoría en su página web, **cuando** se aprueba un nuevo resultado de esa categoría, **entonces** el widget muestra la tabla actualizada en máximo un minuto.

### HU-18 Preinscribir un equipo para el próximo torneo

*R4 · Inscribirse al próximo torneo · Prioridad baja*

Como directivo de un club que no está en el torneo, quiero enviar una preinscripción en línea para participar en la próxima edición.

**Criterios de aceptación:**

- CA1. **Dado que** la organización abrió la preinscripción del próximo torneo, **cuando** el directivo envía el formulario con club, categorías y contacto, **entonces** recibe un correo de confirmación y la solicitud queda «Pendiente».

## Aficionado registrado

### HU-12 Crear mi cuenta de aficionado

*R2 · Llevar el torneo en el celular · Prioridad alta*

Como aficionado, quiero crear una cuenta para guardar mis equipos, mis compras y mis reservas.

**Criterios de aceptación:**

- CA1. **Dado que** el visitante está en «Crear cuenta», **cuando** se registra con su correo o con Google y confirma el correo, **entonces** entra a la aplicación como aficionado.
- CA2. **Dado que** un aficionado inicia sesión, **cuando** intenta abrir el panel de delegado o de organización, **entonces** el sistema no le da acceso.

### HU-13 Seguir a mis equipos

*R2 · Llevar el torneo en el celular · Prioridad alta*

Como aficionado, quiero seguir a los equipos de mis hijos o de mi club para ver primero lo que me importa.

**Criterios de aceptación:**

- CA1. **Dado que** el aficionado sigue dos equipos, **cuando** abre la aplicación, **entonces** ve arriba el próximo partido y el último resultado de cada uno.

### HU-14 Recibir avisos de mis equipos

*R2 · Llevar el torneo en el celular · Prioridad media*

Como aficionado, quiero recibir una notificación cuando mi equipo tenga horario o resultado para no tener que estar revisando.

**Criterios de aceptación:**

- CA1. **Dado que** el aficionado activó las notificaciones y sigue un equipo, **cuando** la organización aprueba la programación de la jornada, **entonces** recibe un aviso con fecha, hora y cancha del partido.
- CA2. **Dado que** el aficionado sigue un equipo, **cuando** la organización aprueba el resultado de su partido, **entonces** recibe un aviso con el marcador.

### HU-15 Comprar en la tienda

*R4 · Comprar en la tienda · Prioridad media*

Como aficionado, quiero comprar productos del torneo en línea para no depender de ir a la sede.

**Criterios de aceptación:**

- CA1. **Dado que** el producto tiene existencias, **cuando** el aficionado paga su carrito y la pasarela aprueba el pago, **entonces** el pedido queda «Pagado», se descuentan las existencias y recibe el comprobante por correo.
- CA2. **Dado que** la pasarela rechaza el pago, **cuando** el aficionado vuelve a la tienda, **entonces** el pedido no se confirma y las existencias no cambian.

### HU-16 Reservar fotos o video de un partido

*R4 · Reservar fotos y video · Prioridad alta*

Como aficionado, quiero reservar fotos o video del partido de mi hijo para tener un recuerdo profesional.

**Criterios de aceptación:**

- CA1. **Dado que** el partido está programado y aún no se ha jugado, **cuando** el aficionado elige un paquete y la pasarela aprueba el pago, **entonces** la reserva queda confirmada en «Mis reservas».
- CA2. **Dado que** el partido ya se jugó o fue cancelado, **cuando** el aficionado intenta reservarlo, **entonces** el sistema no permite la reserva.

### HU-17 Recibir el link de mis fotos o video

*R4 · Reservar fotos y video · Prioridad alta*

Como aficionado, quiero recibir el link de mis fotos o video para descargarlos cuando estén listos.

**Criterios de aceptación:**

- CA1. **Dado que** la reserva está pagada, **cuando** el fotógrafo carga el link de entrega, **entonces** el aficionado lo ve en «Mis reservas» y le llega por correo y por notificación.

## Organizador

### HU-19 Configurar la marca de mi página

*R2 · Administrar la página pública · Prioridad alta*

Como organizador, quiero configurar el logo, los colores y el dominio de mi página para que el público la reconozca como nuestra.

**Criterios de aceptación:**

- CA1. **Dado que** el organizador guardó logo, colores y dominio, **cuando** un visitante entra por ese dominio, **entonces** ve la página con esa marca y solo los torneos de esa organización.

### HU-20 Elegir qué se publica

*R1 · Administrar la página pública · Prioridad alta*

Como organizador, quiero decidir qué torneos y secciones se ven en la página pública para mostrar solo lo que está listo.

**Criterios de aceptación:**

- CA1. **Dado que** el organizador apagó la sección «Tienda», **cuando** un visitante abre la página, **entonces** la tienda no aparece en el menú.
- CA2. **Dado que** un torneo está marcado como no público, **cuando** un visitante busca sus datos, **entonces** el torneo no aparece.

### HU-21 Publicar un documento para el público

*R1 · Administrar la página pública · Prioridad alta*

Como organizador, quiero marcar el reglamento y las resoluciones como públicos para que las familias los consulten sin pedirlos por chat.

**Criterios de aceptación:**

- CA1. **Dado que** el organizador tiene un documento publicado para delegados, **cuando** lo marca como «Público», **entonces** el documento aparece en la sección «Documentos» de la página.

### HU-22 Publicar una noticia

*R2 · Administrar la página pública · Prioridad media*

Como organizador, quiero publicar noticias para informar al público sin depender solo de las redes sociales.

**Criterios de aceptación:**

- CA1. **Dado que** el organizador escribió una noticia en borrador, **cuando** la publica, **entonces** aparece de primera en «Noticias».
- CA2. **Dado que** el organizador marcó «Avisar a los seguidores» al publicar, **cuando** la noticia se publica, **entonces** los aficionados con notificaciones activas reciben el aviso.

### HU-23 Publicar la galería de una jornada

*R2 · Administrar la página pública · Prioridad baja*

Como organizador, quiero subir las fotos de la jornada junto a las piezas generadas para tener la galería en un solo lugar.

**Criterios de aceptación:**

- CA1. **Dado que** la jornada ya tiene piezas generadas, **cuando** el organizador sube las fotos y publica el álbum, **entonces** la galería de la jornada muestra fotos y piezas.

### HU-24 Generar un widget

*R2 · Administrar la página pública · Prioridad media*

Como organizador, quiero generar el código de un widget para mostrar el torneo en la página web que ya tenemos.

**Criterios de aceptación:**

- CA1. **Dado que** el organizador elige el tipo de widget y la categoría, **cuando** pulsa «Copiar código», **entonces** obtiene un fragmento listo para pegar que muestra ese contenido con la marca de la organización.

### HU-25 Administrar los patrocinadores

*R3 · Patrocinar · Prioridad alta*

Como organizador, quiero asignar espacios a cada patrocinador con fechas de vigencia para cumplirle lo que se acordó con él.

**Criterios de aceptación:**

- CA1. **Dado que** el organizador asignó el banner principal a un patrocinador hasta una fecha, **cuando** llega el día siguiente a esa fecha, **entonces** el banner deja de mostrarse sin que nadie lo quite a mano.

### HU-26 Consultar las métricas de patrocinio

*R3 · Patrocinar · Prioridad media*

Como organizador, quiero ver las impresiones y los clics de cada patrocinador para rendirle cuentas y renovar el patrocinio.

**Criterios de aceptación:**

- CA1. **Dado que** un patrocinador tiene espacios activos, **cuando** el organizador abre sus métricas del mes, **entonces** ve impresiones y clics por espacio y puede descargarlas.

### HU-27 Administrar los productos de la tienda

*R4 · Comprar en la tienda · Prioridad media*

Como organizador, quiero cargar los productos con sus tallas y existencias para venderlos en línea.

**Criterios de aceptación:**

- CA1. **Dado que** el organizador creó un producto con existencias, **cuando** lo activa, **entonces** el producto aparece en la tienda.
- CA2. **Dado que** un producto se queda sin existencias, **cuando** un aficionado lo ve en la tienda, **entonces** aparece como «Agotado» y no se puede agregar al carrito.

### HU-28 Gestionar los pedidos

*R4 · Comprar en la tienda · Prioridad media*

Como organizador, quiero ver los pedidos pagados y marcarlos como entregados para llevar el control de la tienda.

**Criterios de aceptación:**

- CA1. **Dado que** hay pedidos pagados, **cuando** el organizador marca uno como «Entregado», **entonces** el pedido cambia de estado y el aficionado lo ve así en su cuenta.

### HU-29 Configurar las reservas de fotos y video

*R4 · Reservar fotos y video · Prioridad alta*

Como organizador, quiero definir los paquetes de fotos y video y asignar el fotógrafo de cada partido para atender las reservas.

**Criterios de aceptación:**

- CA1. **Dado que** un partido tiene reservas pagadas, **cuando** el organizador le asigna un fotógrafo, **entonces** el partido aparece en el panel de ese fotógrafo con sus reservas.
- CA2. **Dado que** un partido con reservas se reprograma, **cuando** se aprueba la nueva fecha, **entonces** los aficionados que reservaron y el fotógrafo reciben un aviso con el nuevo horario.

### HU-30 Revisar las preinscripciones

*R4 · Inscribirse al próximo torneo · Prioridad baja*

Como organizador, quiero aprobar o rechazar las preinscripciones para armar el próximo torneo con los clubes que cumplen.

**Criterios de aceptación:**

- CA1. **Dado que** hay una preinscripción pendiente, **cuando** el organizador la aprueba, **entonces** se crean los equipos en el torneo y el club recibe la invitación para registrar a su delegado.
- CA2. **Dado que** hay una preinscripción pendiente, **cuando** el organizador la rechaza con un motivo, **entonces** el club recibe un correo con ese motivo.

## Fotógrafo o videógrafo

### HU-31 Ver mis partidos asignados

*R4 · Reservar fotos y video · Prioridad alta*

Como fotógrafo, quiero ver los partidos que me asignaron con sus reservas para saber a dónde ir y a quién cubrir.

**Criterios de aceptación:**

- CA1. **Dado que** el fotógrafo tiene partidos asignados, **cuando** abre su panel, **entonces** ve fecha, hora, cancha y los jugadores o equipos de cada reserva, y no ve reservas de otros fotógrafos.

### HU-32 Cargar el link de entrega

*R4 · Reservar fotos y video · Prioridad alta*

Como fotógrafo, quiero cargar el link del material de cada reserva para entregarlo sin mandarlo por chat.

**Criterios de aceptación:**

- CA1. **Dado que** el partido ya se jugó, **cuando** el fotógrafo pega un link válido y pulsa «Entregar», **entonces** la reserva queda «Entregada» y el cliente recibe el aviso.
- CA2. **Dado que** el fotógrafo deja el link vacío o con un formato inválido, **cuando** pulsa «Entregar», **entonces** el sistema no guarda y le indica el error.

## Patrocinador

### HU-33 Ver las métricas de mi marca

*R3 · Patrocinar · Prioridad media*

Como patrocinador, quiero consultar cuántas veces se vio mi marca y cuántos clics recibió para medir el retorno de mi patrocinio.

**Criterios de aceptación:**

- CA1. **Dado que** el patrocinador inicia sesión con su cuenta, **cuando** abre «Mis métricas», **entonces** ve impresiones y clics de sus espacios por mes y no ve datos de otros patrocinadores.

### HU-34 Descargar el informe de mi patrocinio

*R3 · Patrocinar · Prioridad baja*

Como patrocinador, quiero descargar un informe del periodo para presentarlo dentro de mi empresa.

**Criterios de aceptación:**

- CA1. **Dado que** el patrocinador eligió un rango de fechas, **cuando** pulsa «Descargar informe», **entonces** obtiene un PDF con impresiones, clics y espacios en ese periodo.
