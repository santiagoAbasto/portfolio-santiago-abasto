# Control de calidad del portafolio

**Fecha:** 16-11-2026. Cada punto indica cómo se comprobó. Lo que no se pudo ejecutar figura como pendiente; ninguna prueba se da por hecha sin haberla corrido.

| # | Verificación | Resultado | Cómo se comprobó |
|---|---|---|---|
| 1 | Rutas de imágenes | ✅ 37 rutas locales distintas, 0 faltantes | Cada `src` del README contra el disco |
| 2 | Enlaces externos | ✅ 19 de 21 responden 200 · ⚠️ 2 explicados | Una petición HTTP por URL (ver abajo) |
| 3 | Anclas internas | ✅ 147 enlaces a 68 destinos, 0 rotos | Anclas calculadas como las genera GitHub y anclas explícitas `<a name>` |
| 4 | Diagramas Mermaid | ✅ 251 de 251 válidos | `mermaid.parse` (Mermaid 11.4.1) en Chrome headless |
| 5 | Revisión visual de las miniaturas | ✅ 16 diseños revisados en 1200 × 675 y los casos más ajustados en 1200 × 630 | Render y lectura de cada PNG; ver correcciones |
| 6 | Textos, tildes y nombres | ✅ | Revisión de los textos nuevos; nombres oficiales verificados (Burrow Prospect, Locoton según el autor) |
| 7 | Contraste, tamaños y móvil | ✅ | Textos claros sobre azul marino (mínimo 11 px en etiquetas y 14 px en contenido); README revisado a 375 px: miniaturas de a dos y leyendas en texto real legibles |
| 8 | SVG y PNG coinciden | ✅ idénticos byte a byte | Cada PNG se renderiza desde su SVG; se volvió a renderizar y se compararon los archivos |
| 9 | Archivos privados | ✅ ninguno | 0 correos o teléfonos en lo publicado; `evidencias/` en `.gitignore`; sin capturas de paneles privados |
| 10 | README en GitHub | ✅ | Verificado en vivo después de publicar (ver abajo) |

## Detalle de enlaces externos

| Estado | Enlace | Nota |
|---|---|---|
| 200 | appleboss.com.bo · burrowlabs.com.bo · /proyectos/burrow-prospect · ninthgroup.bo · aiq.com.ar · moldpack.com.ar | Sitios públicos |
| 200 | prospect.burrowlabs.com.bo/login · sistema.odessaoil.com | Pantallas de acceso de sistemas en producción, **no** demos públicas |
| 200 | Repositorios públicos de GitHub (AIQ, ApplebBoss-Laravel, odessa y los de terceros) · Figma · shields.io | |
| 403 | gitlab.com/…/p13-arquitectura-tickets-soporte | Redirige al inicio de sesión de GitLab: repositorio privado. **Pendiente de decisión** |
| 999 | linkedin.com/in/santiagoabasto | LinkedIn rechaza toda petición automática; la URL sale del perfil de GitHub del autor |

## Correcciones que surgieron del QA

- **Faltaba el problema en la miniatura A.** El brief pide explicar el problema empresarial; se agregó el bloque «El problema», con textos tomados de cada README.
- **Desborde en la miniatura B.** El texto monoespaciado se medía con métricas proporcionales; ahora usa métricas monoespaciadas.
- **Versiones partidas y separadores colgando.** «Vue / 3.5» y «PostgreSQL 17 ·» al cortar línea; ahora la versión no se separa de su tecnología y ningún «·» queda al borde.
- **Capacidad sin respaldo.** «CRM» en Burrow Prospect se cambió por «WhatsApp».

## Verificación en GitHub (16-11-2026, después de publicar)

- README renderizado con 292 imágenes y **0 rotas**.
- Casos destacados: las 8 miniaturas A cargan; las 8 imágenes B cargan dentro de sus fichas.
- **Anclas presentes:** `#apple-boss`, `#burrow-prospect`, `#odessa-oil`, `#moldpack`, `#locoton`, `#ninth-group`, `#aiq` y `#calendariow` (los destinos de los elementos B en LinkedIn), los alias `#burrow-prospects` y `#mahiki-restaurante-y-bar`, y `#casos-destacados` y `#problemas`.
- Títulos en vivo: «1. Locoton — POS y gestión gastronómica» y «36. Burrow Prospect».
- Lectura en móvil (375 px): `#casos-destacados` abre en su sección; miniaturas de a dos y leyendas legibles.

**No verificado desde aquí:** LinkedIn. Las imágenes y la guía están listas, pero el perfil se actualiza a mano (ver `linkedin-reinsercion-miniaturas.md`).
