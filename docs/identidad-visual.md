# Identidad visual de las miniaturas

Un sistema, no dieciséis imágenes sueltas: todas comparten fondo, retícula, tipografía y componentes, y cada proyecto aporta solo dos colores de acento. Así la colección se reconoce de un vistazo y cada caso mantiene su identidad.

## Principios

- **Software empresarial, no ciencia ficción.** Nada de robots, cerebros brillantes, pantallas inventadas ni fondos futuristas.
- **Solo lo verificado.** Cada texto sale de `assets/portfolio/generador/proyectos.json`, contrastado con el código, el historial de git y respuestas HTTP. No hay cifras sin evidencia.
- **Sin logotipos ajenos.** El nombre de cada proyecto va tipografiado; no se imitan ni alteran identidades corporativas.
- **El estado es honesto.** «En producción», «Producción por verificar» o «En desarrollo», según la evidencia.

## Fondo y retícula

| Elemento | Valor |
|---|---|
| Fondo | Degradado vertical `#0D1733` → `#070C1A` (azul marino profundo) |
| Retícula | Líneas cada 48 px, blanco al 3,5 % |
| Brillos | Acento 1 desde la esquina superior derecha (20 %); acento 2 desde la inferior izquierda (12 %) |
| Márgenes | 72 px a los lados; pie separado por una línea al 10 % |

## Tipografía

| Uso | Familia | Tamaño |
|---|---|---|
| Nombre del proyecto | SF Pro Display, negrita (respaldo: Inter, Segoe UI, Helvetica) | 76 px (A) · 50 px (B) |
| Propuesta de valor | SF Pro, 500 | 32 px |
| Problema y capacidades | SF Pro | 15–19 px |
| Etiquetas, estado, enlaces | SF Mono (respaldo: JetBrains Mono, Menlo) en mayúsculas espaciadas | 11–13 px |

Los PNG se exportan con las fuentes del sistema macOS. Los SVG son editables y usan las mismas pilas de fuentes con respaldo.

## Acentos por proyecto

| Caso | Acento 1 | Acento 2 | Origen |
|---|---|---|---|
| Apple Boss | `#C6CB36` lima | `#8F95D6` periwinkle | Paleta `ab` de su Tailwind |
| Burrow Prospect | `#4FA3E0` azul | `#FCEA10` amarillo | Marca Burrow Labs |
| Odessa Oil | `#E04A63` | `#5B8DEF` | Banner de su README |
| Moldpack | `#EC458B` rosa | `#F7A8CB` | CSS de su sitio (`#EC458B`, `#5D1C38`) |
| Locoton | `#FB923C` | `#F43F5E` | Banner de su README |
| Ninth Group | `#C9AD7E` dorado | `#E9DCC2` | Banner de su README |
| AIQ | `#F04452` | `#5B93F2` | Banner de su README |
| CalendarioW | `#3B8FD9` | `#FCE301` | Hero de su README |

Los acentos se aclararon lo necesario para leerse sobre el azul marino.

## Componentes

**Comunes:** barra superior con «CASO 0N · CATEGORÍA» y una píldora de estado (verde, ámbar o celeste), y un pie con el enlace de destino a la izquierda y la firma a la derecha.

**A · Producto** (para el enlace a la aplicación o al caso público):

1. Nombre y barra de acento.
2. Propuesta de valor en una línea.
3. Cuatro capacidades en píldoras.
4. **El problema** que resuelve, en una línea.
5. **Flujo principal**: el proceso real del sistema en cuatro pasos, como diagrama mínimo.

**B · Arquitectura** (para el enlace a la ficha técnica en GitHub):

1. Nombre y bajada «Arquitectura simplificada · stack verificado en el código».
2. Diagrama de tres columnas: usuarios y canales → aplicación (framework y módulos) → datos y servicios externos (estos con borde punteado).
3. Panel derecho con el **stack verificado** y tres **capacidades verificadas**.

## Formatos

| Archivo | Uso |
|---|---|
| `producto.svg`, `arquitectura.svg` | Maestro editable, 1200 × 675 |
| `*-1200x630.svg` | La misma información adaptada a 1200 × 630 |
| `*-1200x675.png` | README, presentaciones y publicaciones 16:9 |
| `*-1200x630.png` | **Miniaturas de enlaces en LinkedIn** y vista previa social |

Cada PNG se exporta renderizando su propio archivo SVG con Chrome headless, así que SVG y PNG coinciden por construcción; el QA lo comprobó volviendo a renderizar y comparando los archivos byte a byte.

## Regenerar o agregar un proyecto

```bash
python3 assets/portfolio/generador/miniaturas.py            # SVG + PNG
python3 assets/portfolio/generador/miniaturas.py --solo-svg # solo SVG
```

Para agregar un proyecto, se suma una entrada a `proyectos.json` con datos verificados. El generador **falla con un mensaje claro** si un texto no entra en su espacio, si las capacidades chocan con el flujo o si una columna del diagrama no cabe, en lugar de producir una imagen desbordada. Requiere Google Chrome (variable `CHROME` si está en otra ruta).

El catálogo visual de las 16 miniaturas está en [`assets/portfolio/catalogo.html`](../assets/portfolio/catalogo.html).
