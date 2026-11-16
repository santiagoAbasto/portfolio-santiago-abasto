# Auditoría del portafolio

**Fecha:** 16-11-2026 · **Repositorio:** `santiagoAbasto/portfolio-santiago-abasto` (rama `main`)
**Alcance:** el README maestro (61 fichas), sus diagramas, imágenes y enlaces, y la verificación de los ocho casos que representan el trabajo en LinkedIn.

## Método

Nada de lo que se afirma en el portafolio sale solo de los README de cada proyecto. Cada dato se contrastó con una fuente que se puede repetir:

| Fuente | Qué se verificó |
|---|---|
| `composer.json`, `package.json`, `pubspec.yaml`, `docker-compose*.yml` | Stack y versiones reales |
| Historial de git (`git shortlog`, identidades de autor) | Participación: quién escribió el código |
| Peticiones HTTP a cada enlace (una por URL) | Que el enlace responde y a qué lleva |
| Configuración de despliegue en cada repositorio | Evidencia de producción cuando el sistema es privado |
| Ejecución de pruebas (Apple Boss) | Cifra de pruebas publicada |
| `mermaid.parse` sobre los 251 diagramas | Validez de cada diagrama |
| Captura aportada por el autor (AIQ) | Asesor con IA funcionando en producción |

Los proyectos originales **no se modificaron**: todas las correcciones viven en este repositorio.

## Estado inicial

- Rama `main` sincronizada con el remoto, sin cambios pendientes.
- README de 8 412 líneas: 61 fichas en 5 bloques, 251 diagramas Mermaid, 60 desplegables y 263 imágenes.
- Recursos gráficos: íconos, etiquetas y botones SVG en `docs/readme/` y miniaturas sociales en `docs/social/`.
- Faltaban una sección orientada al cliente, los casos destacados y la evidencia de participación y producción por proyecto.

## Hallazgos y correcciones

| # | Problema | Evidencia | Impacto | Corrección |
|---|---|---|---|---|
| 1 | El producto **Locoton** figuraba como «Mahiki — Restaurante y bar», con Mahiki presentado como cliente | La ficha decía «El local trabaja hoy con Siesam», «**MAHIKI** reproduce…» y «Qué hace en MAHIKI». El código no menciona «Locoton» (`APP_NAME=Laravel`, repositorio `Mahiki`) | Atribución de cliente sin respaldo contractual | Ficha renombrada a **Locoton — POS y gestión gastronómica**; Mahiki queda como referencia de investigación en *Procedencia*; ancla `#locoton` con el alias `#mahiki-restaurante-y-bar` |
| 2 | Producción de Locoton sin evidencia | La documentación del propio repositorio (15-11-2026) dice que «corre solo en local» | Afirmar producción sin pruebas | Estado: **producción por verificar**; URL pendiente |
| 3 | Nombre «Burrow Prospects» | El título oficial en burrowlabs.com.bo es **Burrow Prospect** | Nombre inconsistente con el producto | Renombrado; ancla `#burrow-prospect` con el alias `#burrow-prospects` |
| 4 | AIQ sin producción confirmada | El README del proyecto marca «producción no verificada» | Se subestimaba el caso | `aiq.com.ar/zona-clientes` responde 302 al login en producción y el autor aportó una captura del asesor funcionando: **asesor en producción** |
| 5 | «CRM» en el mensaje de Burrow Prospect | El README solo documenta «métricas de embudo», no un CRM | Capacidad exagerada | Reemplazado por **WhatsApp** (API oficial de Meta, verificada) |
| 6 | Cifras viejas en el README de Apple Boss | Decía 827 pruebas y 113 fichas; hoy son 915 y 160 | Datos desactualizados | Corregido en su repositorio (commits `053c6e6` y `0d2d956`), con la suite ejecutada completa |
| 7 | El enlace de GitLab de Tigo lleva al inicio de sesión | `gitlab.com/…/p13-arquitectura-tickets-soporte` → 302 a `/users/sign_in` | El visitante encuentra un muro de acceso | **Pendiente**: hacer público el repositorio o marcarlo como privado |
| 8 | No había entrada orientada al cliente | — | Quien llega desde LinkedIn no ve rápido qué problemas se resuelven | Secciones **Casos destacados** y **Qué problemas resuelvo** antes del índice |
| 9 | Sin participación ni evidencia por proyecto | — | No se distinguía trabajo propio, colaboración ni estado real | Bloque **Participación y evidencia** en los 8 casos y leyenda de lectura (fichas 1–55 propias, 56–61 colaboraciones) |
| 10 | Miniaturas genéricas o rotas en LinkedIn | Vistas previas automáticas de GitHub | Presentación poco profesional | Sistema visual nuevo: 16 diseños (ver `identidad-visual.md`) |

El enlace de LinkedIn responde 999 a cualquier petición automática (bloqueo de bots de LinkedIn); la URL sale del propio perfil de GitHub del autor.

## Verificación de los ocho casos

| Caso | Nombre oficial | Producción (evidencia) | Código | Participación | Stack verificado |
|---|---|---|---|---|---|
| Apple Boss | Apple Boss | appleboss.com.bo → 200 | Público | Desarrollo integral, fundador; 193 commits | Laravel 13 · PHP 8.5 · React 19 · Inertia 3 · PostgreSQL 18 |
| Burrow Prospect | Burrow Prospect | Caso público → 200; aplicación con login → 200 | Privado | Producto de Burrow Labs; único autor, 84 commits | Laravel 13 · React 19 · TS 6 · Tailwind 4 · PostgreSQL 18 |
| Odessa Oil | Odessa Oil | sistema.odessaoil.com → 200 (login); configuración de despliegue en el repo | Público | Único autor, 49 commits | Laravel 13 · React 19 · TS 7 · Tailwind 4 · MariaDB |
| Moldpack | Moldpack | moldpack.com.ar → 200; sus recursos coinciden con el repo | Privado | Único autor, 14 commits del sistema vigente | Laravel 13 · PHP 8.5 · React 19 · Inertia 3 · MySQL 8 |
| Locoton | Locoton (según el autor) | **Pendiente**: la documentación dice que corre en local | Privado | Desarrollo integral | Laravel 13 · Vue 3.5 · Inertia 3 · TS · MySQL 9.6 |
| Ninth Group | Ninth Group | ninthgroup.bo → 200 | Privado | Único autor, 42 commits | Laravel 13 · PHP 8.5 · React 19 · MySQL 8.4 · Redis 8 |
| AIQ | AIQ | aiq.com.ar → 200; zona de clientes → login; captura del autor | Público | Único autor | Laravel 12 · Vue 3 · Inertia 2 · MySQL · Gemini |
| CalendarioW | CalendarioW | **Sin despliegue**: corre en local | Privado | Producto de BurrowLabs; único autor | Laravel 13 · React 19 · Flutter · PostgreSQL 17 · Supabase |

**Identidades de git.** En Apple Boss aparecen «User» y «AppleBoss» además del nombre del autor: «User» sale de las mismas máquinas que también firman como el autor (nombre de git sin configurar) y «AppleBoss» es el equipo de su empresa. Los otros siete repositorios tienen un solo autor. No se encontró trabajo en colaboración en los ocho casos.

**Confidencialidad.** El código de cinco casos es privado; el portafolio describe arquitectura y capacidades sin exponer datos, credenciales ni pantallas internas. La captura del asesor de AIQ muestra conversaciones y métricas personales del autor y **no se publica**.

## Contadores después de las correcciones

61 fichas · 251 diagramas (todos válidos) · 8 casos destacados con dos miniaturas cada uno. La corrección de Locoton no tocó ningún diagrama.
