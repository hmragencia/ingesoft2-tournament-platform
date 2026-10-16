# 2. Requisitos no funcionales

| ID | Atributo | Requisito |
|---|---|---|
| RNF-01 | Rendimiento | Las páginas públicas deben mostrar su contenido principal en menos de 2,5 segundos en un celular con red 4G, y responder a las acciones del usuario en menos de 2 segundos. |
| RNF-02 | Actualización de datos | Un resultado o una programación aprobada debe verse en la página, la aplicación y los widgets en máximo 1 minuto. |
| RNF-03 | Escalabilidad | El módulo debe soportar al menos 2.000 visitantes simultáneos en un día de jornada sin afectar el tiempo de respuesta del panel de la organización; las consultas públicas se sirven desde caché y no consultan la base de datos en cada visita. |
| RNF-04 | Privacidad | La vista pública no debe exponer documento, fecha de nacimiento, foto de carnet, datos de contacto ni saldos de ningún participante; la mayoría son menores de edad y aplica la Ley 1581 de 2012 de protección de datos personales. |
| RNF-05 | Seguridad | Las cuentas de aficionado, patrocinador y fotógrafo solo deben acceder a sus propios datos, con seguridad a nivel de fila (RLS) en la base de datos y no solo en la interfaz. |
| RNF-06 | Seguridad de pagos | Los pagos deben procesarse en una pasarela certificada PCI DSS; el sistema no almacena datos de tarjetas y confirma cada pago una sola vez aunque la pasarela notifique varias veces. |
| RNF-07 | Usabilidad | El diseño debe ser móvil primero, funcionar desde 360 px de ancho sin desplazamiento horizontal, y cualquier dato del torneo debe quedar a máximo tres toques desde el inicio. |
| RNF-08 | Accesibilidad | Las páginas públicas deben cumplir WCAG 2.1 nivel AA: contraste suficiente, textos alternativos en imágenes y navegación completa con teclado. |
| RNF-09 | Disponibilidad | El módulo debe tener una disponibilidad mensual del 99,5 %, sin mantenimientos programados los días de jornada. |
| RNF-10 | Compatibilidad | La aplicación debe funcionar en Android 10 o superior, en iOS 16.4 o superior (versión desde la que iOS permite notificaciones push en PWA) y en las dos últimas versiones de Chrome, Safari, Edge y Firefox. |
| RNF-11 | Mantenibilidad | Habilitar una nueva liga con su propia marca debe hacerse solo por configuración, sin cambios de código ni despliegues. |
| RNF-12 | Visibilidad en buscadores | Cada equipo, partido y noticia debe tener una dirección propia y una vista previa (Open Graph) al compartirse por WhatsApp o redes sociales. |
