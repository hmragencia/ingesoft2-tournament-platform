# 1. Requisitos funcionales

## Consulta pública del torneo

| ID | Requisito | Descripción |
|---|---|---|
| RF-01 | Consultar la programación | El sistema debe permitir al visitante consultar, sin iniciar sesión, la programación aprobada de cada jornada filtrando por torneo, categoría y grupo, con fecha, hora, cancha y equipos de cada partido. |
| RF-02 | Consultar los resultados | El sistema debe permitir al visitante consultar el marcador y los goleadores de cada partido jugado, marcando como «provisional» el resultado que la organización todavía no ha aprobado. |
| RF-03 | Consultar la tabla de posiciones | El sistema debe mostrar al visitante la tabla de posiciones de cada grupo (PJ, PG, PE, PP, GF, GC, DG y puntos), calculada con los criterios de desempate del reglamento y con los equipos retirados al final. |
| RF-04 | Consultar goleadores y valla menos vencida | El sistema debe mostrar al visitante la tabla de goleadores y la de valla menos vencida de cada categoría, acumuladas durante todo el torneo. |
| RF-05 | Consultar los documentos públicos | El sistema debe permitir al visitante ver y descargar el reglamento, las resoluciones y los comunicados que la organización haya marcado como públicos. |
| RF-06 | Ver la ficha de un equipo | El sistema debe mostrar una ficha por equipo con su escudo, categoría, grupo, posición actual, próximos partidos y resultados. |
| RF-07 | Ver la ficha de un club | El sistema debe mostrar una ficha por club con todos sus equipos en el torneo, agrupados por categoría. |
| RF-08 | Buscar equipos y clubes | El sistema debe permitir al visitante buscar un equipo o un club por su nombre desde cualquier página. |
| RF-09 | Leer las noticias | El sistema debe mostrar las noticias publicadas por la organización, ordenadas de la más reciente a la más antigua. |
| RF-10 | Ver la galería de la jornada | El sistema debe mostrar por jornada las piezas de programación y resultados que ya genera la plataforma y las fotos que la organización publique. |

## Canales: página, widgets y aplicación

| ID | Requisito | Descripción |
|---|---|---|
| RF-11 | Instalar la aplicación | El sistema debe poder instalarse como aplicación web progresiva (PWA) en Android e iOS, con el nombre, el ícono y los colores de la organización. |
| RF-12 | Generar widgets insertables | El sistema debe permitir al organizador generar el código de widgets (tabla de posiciones, próximos partidos, últimos resultados) para insertarlos en la página web actual de la organización. |
| RF-13 | Configurar la marca de la organización | El sistema debe permitir al organizador configurar el logo, los colores y el dominio de su página pública; cada organización se ve con su propia marca (marca blanca). |
| RF-14 | Elegir qué se publica | El sistema debe permitir al organizador decidir qué torneos y qué secciones (noticias, galería, tienda, reservas, preinscripción) se muestran en su página pública. |
| RF-15 | Publicar noticias y galería | El sistema debe permitir al organizador crear noticias y álbumes de fotos por jornada, guardarlos como borrador y publicarlos. |

## Aficionado registrado

| ID | Requisito | Descripción |
|---|---|---|
| RF-16 | Crear una cuenta de aficionado | El sistema debe permitir al visitante crear una cuenta de aficionado con correo electrónico o con Google; esta cuenta no da acceso a los paneles de delegado ni de organización. |
| RF-17 | Seguir equipos favoritos | El sistema debe permitir al aficionado seguir uno o varios equipos y ver primero, al abrir la aplicación, el próximo partido y el último resultado de cada uno. |
| RF-18 | Notificar a los seguidores | El sistema debe enviar una notificación push al aficionado cuando se publica la programación o se aprueba el resultado de un equipo que sigue. |

## Patrocinio

| ID | Requisito | Descripción |
|---|---|---|
| RF-19 | Administrar patrocinadores | El sistema debe permitir al organizador registrar patrocinadores y asignarles espacios en la página, la aplicación y las piezas de jornada, con fecha de inicio y fin. |
| RF-20 | Medir la exposición de la marca | El sistema debe registrar las impresiones y los clics de cada espacio de patrocinio, sin guardar datos personales del visitante. |
| RF-21 | Consultar métricas de patrocinio | El sistema debe permitir al patrocinador, con su cuenta, consultar y descargar las métricas de sus propios espacios por periodo. |

## Comercio: tienda, reservas y preinscripción

| ID | Requisito | Descripción |
|---|---|---|
| RF-22 | Administrar el catálogo de la tienda | El sistema debe permitir al organizador crear productos con foto, descripción, tallas y existencias, y activarlos o desactivarlos. |
| RF-23 | Comprar en línea | El sistema debe permitir al aficionado armar un carrito y pagarlo a través de una pasarela de pagos; el pedido solo se confirma cuando la pasarela aprueba el pago. |
| RF-24 | Gestionar pedidos | El sistema debe permitir al organizador ver los pedidos pagados y marcarlos como listos para recoger o entregados. |
| RF-25 | Reservar fotos o video de un partido | El sistema debe permitir al aficionado reservar un paquete de fotos o de video para un partido programado y pagarlo en línea. |
| RF-26 | Asignar el fotógrafo a una reserva | El sistema debe permitir al organizador asignar un fotógrafo o videógrafo a cada partido con reservas. |
| RF-27 | Entregar el material por link | El sistema debe permitir al fotógrafo cargar el link de entrega de una reserva y avisar al cliente por correo y por notificación. |
| RF-28 | Preinscribir un equipo | El sistema debe permitir a un club interesado enviar una preinscripción para el próximo torneo, y al organizador aprobarla o rechazarla. |
