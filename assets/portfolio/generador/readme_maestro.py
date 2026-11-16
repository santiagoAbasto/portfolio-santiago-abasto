#!/usr/bin/env python3
"""Genera el README maestro del portafolio desde los README de cada proyecto (en ~/Projects).

Uso: python3 assets/portfolio/generador/readme_maestro.py assets/portfolio/generador/manifiesto.tsv
Las correcciones de identidad (FIXES), la evidencia (EVIDENCE) y los casos destacados salen de acá y de proyectos.json."""
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path.home() / "Projects"
MAN = Path(sys.argv[1])
OUT = BASE / "portfolio-santiago-abasto" / "README.md"

# Bloques a medida para los README que usan otra estructura (modelos insignia y casos chicos).
OVERRIDES = {
    "CalendarioW": {
        "desc": "SaaS de agenda, caja y reservas para negocios de servicios — web, iOS y Android.",
        "problema": "Peluquerías, spas, consultorios y veterinarias llevaban su agenda, su caja y sus reservas entre planillas y WhatsApp: dobles reservas, cobros sin control y clientes que se perdían.",
        "stack": "Laravel 13 · PHP 8.5 · React 19 + Inertia · Tailwind 4 · Flutter 3.47 (iOS/Android) · PostgreSQL 17 · Supabase Realtime. Monorepo con 408 pruebas Pest y 93.7% de cobertura.",
        "solucion": "Una sola plataforma —agenda + caja + pagos + clientes + marketing— por web y por celular, en bolivianos y zona horaria de Bolivia, con las reglas de dinero y de reservas hechas en serio: sin dobles reservas y sin confundir un comprobante con un pago.",
    },
    "Burrow Labs": {
        "desc": "Sitio del estudio de software: identidad, casos de estudio y captación de clientes.",
        "problema": "El estudio necesitaba una presencia propia que mostrara su trabajo con nivel y convirtiera visitas en clientes, no una plantilla más.",
        "stack": "Next.js 16 · React 19 · TypeScript estricto · Tailwind 4 · three.js (React Three Fiber) · GSAP ScrollTrigger · PostgreSQL 18 · Drizzle ORM · Docker. 159 pruebas Vitest y 62 E2E Playwright.",
        "solucion": "Sitio en producción (burrowlabs.com.bo) con hero 3D, casos de estudio, planes, diagnóstico express, panel de administración y SEO con búsqueda asistida por IA.",
    },
    "Ninth Group": {
        "desc": "CRM inmobiliario, sitio público y seguimiento de proyectos en preventa.",
        "problema": "Una inmobiliaria con proyectos en preventa necesitaba unir el sitio público, el CRM, el avance de obra, los planes de pago y las comisiones del equipo en un solo sistema.",
        "stack": "Laravel 13 · PHP 8.5 · React 19 · TypeScript estricto · MySQL 8.4 · Redis · Docker. Pruebas con Pest, Vitest y Playwright.",
        "solucion": "Plataforma en producción (ninthgroup.bo) con 26 módulos de dominio: sitio público, fichas de proyectos en preventa con avance de obra y plan de pago, CRM y reparto de comisiones.",
    },
    "Carlos — Bolsa de Valores": {
        "desc": "Análisis institucional de acciones y motor de tesis de inversión asistido por IA.",
        "problema": "Evaluar una acción con criterio institucional —estados financieros, ratios, márgenes y una tesis clara de asignación de capital— es lento y disperso de hacer a mano.",
        "stack": "Python · APIs de datos financieros · LLM (Gemini / Anthropic) · dashboards HTML/CSS · motor 'sentinel-engine' (Next.js en el frontend).",
        "solucion": "Un motor que reúne los datos financieros de una empresa, calcula indicadores (Altman Z, capital de trabajo, etc.) y arma con un LLM una tesis de inversión razonada, con dashboards por caso (MCD, NVO, UBER).",
    },
    "21 — Regalo para Sharol": {
        "desc": "Página de regalo personalizada, con mensajes y animaciones.",
        "problema": "Hacer un regalo digital distinto: una página hecha a mano para una persona, no una tarjeta genérica.",
        "stack": "HTML y CSS, animaciones propias, una sola página estática.",
        "solucion": "Una página de regalo con mensajes que se revelan por interacción y estados animados, pensada para abrirse desde el celular.",
    },
}

LOC = "Locoton — POS y gestión gastronómica"
# Correcciones de identidad: texto exacto de origen -> texto corregido (fallan si el origen cambia)
FIXES = {
    LOC: [
        ("desc", "El sistema de gestión de un restaurante y bar boliviano, de la receta al cobro:",
                 "Sistema POS, inventario y gestión integral para restaurantes y bares, de la receta al cobro:"),
        ("problema", "El local trabaja hoy con **Siesam**, un sistema genérico multi-rubro (sirve igual a un hotel, una distribuidora o un taller). Para un restaurante y bar eso se traduce en:",
                     "Locoton parte de una investigación de procesos en un restaurante y bar en operación (ver *Procedencia*), que trabaja con **Siesam**, un sistema genérico multi-rubro (sirve igual a un hotel, una distribuidora o un taller). Ese relevamiento mostró lo que eso significa para el rubro:"),
        ("solucion", "**MAHIKI** reproduce la lógica de negocio que el local ya conoce (los mismos nombres de módulos, roles y permisos que Siesam)",
                     "**Locoton** toma la lógica de negocio que el rubro ya conoce (los nombres de módulos, roles y permisos de Siesam, relevados en la investigación)"),
        ("solucion", "| Rol | Qué hace en MAHIKI |", "| Rol | Qué hace en Locoton |"),
    ],
}
# Ancla principal y alias (las anclas viejas siguen funcionando)
ANCHORS = {LOC: ("locoton", ["mahiki-restaurante-y-bar"]), "Burrow Prospect": ("burrow-prospect", ["burrow-prospects"])}
# Participación y evidencia de los 8 casos bandera (verificado el 16-11-2026)
EVIDENCE = {
    "Apple Boss": [
        "**Participación:** desarrollo integral, como fundador de Apple Boss. 193 commits entre mayo de 2025 y noviembre de 2026.",
        "**Producción:** [appleboss.com.bo](https://appleboss.com.bo) responde (verificado el 16-11-2026).",
        "**Código:** [público en GitHub](https://github.com/santiagoAbasto/ApplebBoss-Laravel). La suite de 915 pruebas pasó completa el 16-11-2026.",
    ],
    "Burrow Prospect": [
        "**Participación:** desarrollo integral; producto propio de Burrow Labs, único autor en el historial de git (84 commits).",
        "**Producción:** aplicación en [prospect.burrowlabs.com.bo](https://prospect.burrowlabs.com.bo/login) (acceso con usuario) y caso público en [burrowlabs.com.bo](https://burrowlabs.com.bo/proyectos/burrow-prospect).",
        "**Código:** privado.",
    ],
    "Odessa Oil": [
        "**Participación:** desarrollo integral; único autor en el historial de git (49 commits).",
        "**Producción:** [sistema.odessaoil.com](https://sistema.odessaoil.com) (acceso con usuario); la configuración de despliegue está en el repositorio.",
        "**Código:** [público en GitHub](https://github.com/santiagoAbasto/odessa).",
    ],
    "Moldpack": [
        "**Participación:** desarrollo integral; único autor en el historial de git del sistema vigente (14 commits).",
        "**Producción:** [moldpack.com.ar](https://www.moldpack.com.ar): el sitio público sale de este código (sus recursos y su dominio coinciden con el repositorio).",
        "**Código:** privado.",
    ],
    LOC: [
        "**Procedencia:** la investigación de procesos del restaurante y bar Mahiki, que opera con Siesam, fue la referencia de diseño. Mahiki no figura como cliente: no hay evidencia contractual en el repositorio.",
        "**Implementado (verificado en local):** las 11 fases del plan, desde la base y el inventario hasta la venta de restaurante, la caja, multi-sede, los reportes y el delivery, cada una con sus pruebas.",
        "**Pendiente:** conexión real con el SIAT (hoy con simulador), la app del repartidor en un celular real y las impresoras térmicas reales.",
        "**Producción:** reportada por el autor; la documentación del repositorio (15-11-2026) indica ejecución local. URL pública pendiente de verificar.",
        "**Código:** privado. Conserva el nombre interno `mahiki` de la etapa de investigación (por ejemplo, `config/mahiki.php`).",
    ],
    "Ninth Group": [
        "**Participación:** desarrollo integral; único autor en el historial de git (42 commits).",
        "**Producción:** [ninthgroup.bo](https://ninthgroup.bo/).",
        "**Código:** privado.",
    ],
    "AIQ": [
        "**Participación:** desarrollo integral; único autor en el historial de git.",
        "**Producción:** sitio en [aiq.com.ar](https://aiq.com.ar/); el asesor con IA funciona en la zona privada de clientes (`/zona-clientes`, con usuario), verificado el 16-11-2026.",
        "**Código:** [público en GitHub](https://github.com/santiagoAbasto/AIQ).",
    ],
    "CalendarioW": [
        "**Participación:** desarrollo integral; único autor en el historial de git.",
        "**Estado:** en desarrollo; corre en local, sin despliegue a producción ni publicación en tiendas.",
        "**Código:** privado.",
    ],
}

def noacc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()

def slug(s):
    s = noacc(s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s

def group_anchor(g):
    gn = noacc(g)
    if "sistema" in gn: return "sistemas"
    if "commerce" in gn or "industrial" in gn: return "industria"
    if "automat" in gn: return "ia"
    if "colabora" in gn: return "colaboraciones"
    return slug(g)

def ICON(name, px):
    return f'<img src="docs/readme/ic-{name}.svg" width="{px}" height="{px}" alt="">'

GICON = {"sistemas": "sistemas", "industria": "industria", "ia": "ia", "colaboraciones": "colaboraciones"}

def gicon(g):
    return ICON(GICON.get(group_anchor(g), "web"), 26)

TAG = {k: f'<img src="docs/readme/tag-{k}.svg" height="28" alt="{v}">'
       for k, v in [("problema", "Problema"), ("stack", "Stack"), ("solucion", "Solución"), ("evidencia", "Participación y evidencia")]}

# emojis que llegan dentro del contenido extraído (p. ej. diagramas); se conserva el check (U+2713)
EMO = re.compile("(?:[\U0001F000-\U0001FAFF\u2300-\u23FF\u2600-\u2712\u2714-\u27BF\u2B00-\u2BFF\uFE0F\u200D\u20E3])+ ?")

def clean_heading(line):
    t = re.sub(r"^#{1,6}\s*", "", line)
    t = re.sub(r"<a[^>]*></a>|<img[^>]*>", "", t)
    t = re.sub(r"[^\w\sáéíóúñ/]", "", t, flags=re.IGNORECASE)  # quita emojis/símbolos
    return t.strip()

DROP = re.compile(r"^\s*(<img|<div|</div>|<br|<p align|<a id|<a name|<picture|</picture|<source|<!--)")

def clean_body(lines):
    out = []
    for l in lines:
        if DROP.match(l):
            continue
        out.append(l.rstrip())
    txt = "\n".join(out)
    # quitar <img>/<picture>/<source> inline (evita imágenes relativas rotas)
    txt = re.sub(r"<picture>.*?</picture>", "", txt, flags=re.DOTALL)
    txt = re.sub(r"<img[^>]*>", "", txt)
    txt = re.sub(r"</?(source|picture|div|p)[^>]*>", "", txt)
    txt = re.sub(r"[ \t]+\n", "\n", txt)
    txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
    return txt

def parse(path):
    raw = (BASE / path).read_text(encoding="utf-8", errors="replace")
    lines = raw.split("\n")
    # descriptor: primer **...** en las primeras 40 líneas
    desc = ""
    for l in lines[:40]:
        m = re.match(r"^\*\*(.+?)\*\*\s*$", l.strip())
        if m:
            desc = m.group(1).strip()
            break
    if not desc:
        m = re.search(r'alt="[^"]*?[—-]\s*([^"]+)"', raw)
        if m:
            desc = m.group(1).strip()
    # secciones por ##
    sections = {}
    cur, buf = None, []
    for l in lines:
        if re.match(r"^##\s", l) and not re.match(r"^###", l):
            if cur is not None:
                sections[cur] = buf
            cur = clean_heading(l)
            buf = []
        else:
            if cur is not None:
                buf.append(l)
    if cur is not None:
        sections[cur] = buf
    def find(*keys):
        for h, b in sections.items():
            hn = noacc(h)
            if any(k in hn for k in keys):
                return clean_body(b)
        return ""
    problema = find("problema")
    solucion = find("solucion")
    stack = find("stack", "tecnolog")
    # mermaid con etiqueta (### previo)
    mer = []
    label = ""
    i = 0
    while i < len(lines):
        if re.match(r"^###\s", lines[i]):
            label = clean_heading(lines[i])
        if lines[i].strip().startswith("```mermaid"):
            block = [lines[i]]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i]); i += 1
            if i < len(lines):
                block.append(lines[i])
            mer.append((label, "\n".join(block)))
        i += 1
    return desc, problema, solucion, stack, mer

# leer manifiesto preservando orden de grupos
groups = []
rows = []
for line in MAN.read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    g, p, n = line.split("\t")
    if g not in groups:
        groups.append(g)
    rows.append((g, p, n))

# ---------- casos destacados (misma fuente que las miniaturas) ----------
import json as _json
FEAT = _json.loads((OUT.parent / "assets/portfolio/generador/proyectos.json").read_text(encoding="utf-8"))["proyectos"]
FEAT_NAME = {"apple-boss": "Apple Boss", "burrow-prospect": "Burrow Prospect", "odessa-oil": "Odessa Oil", "moldpack": "Moldpack",
             "locoton": LOC, "ninth-group": "Ninth Group", "aiq": "AIQ", "calendariow": "CalendarioW"}
FEAT_BY_NAME = {FEAT_NAME[p["slug"]]: p for p in FEAT}
EST = {"prod": "En producción", "pend": "Producción por verificar", "dev": "En desarrollo"}

def destacados():
    out = ['<a name="casos-destacados"></a>',
           '## <img src="docs/readme/ic-destacados.svg" width="26" height="26" alt=""> Casos destacados\n',
           "Ocho sistemas que representan mi trabajo: un problema real, la solución construida y evidencia que se puede comprobar. "
           "Cada imagen lleva al producto o a su caso público; la ficha técnica completa está más abajo.\n"]
    for i in range(0, len(FEAT), 2):
        par = FEAT[i:i + 2]
        out.append("<p>")
        for p in par:
            dest = p["enlace"] or f'#{p["ancla"]}'
            out.append(f'<a href="{dest}"><img src="assets/portfolio/projects/{p["slug"]}/producto-1200x675.png" width="49%" alt="{p["nombre"]} — {p["mensaje"]}"></a>')
        out.append("</p>\n")
        for p in par:
            prod = f' · [Ver producto]({p["enlace"]})' if p["enlace"] else ""
            out.append(f'- **{p["nombre"]}** · {p["mensaje"]} *{EST[p["estado"]]}*{prod} · [Ficha técnica](#{p["ancla"]})')
        out.append("")
    out.append('<a name="problemas"></a>')
    out.append('## <img src="docs/readme/ic-resuelvo.svg" width="26" height="26" alt=""> Qué problemas resuelvo\n')
    out += [
        "| Si tu empresa… | Construyo… | Casos |",
        "|---|---|---|",
        "| Lleva ventas, stock, caja o reservas en planillas y WhatsApp | Sistemas de gestión con roles, caja, inventario y reportes | [Apple Boss](#apple-boss) · [Locoton](#locoton) · [CalendarioW](#calendariow) |",
        "| Vende a otras empresas y factura a mano | Portales B2B con logística y factura electrónica | [Moldpack](#moldpack) |",
        "| Tiene que demostrar inspecciones, certificaciones o vencimientos | Trazabilidad multiempresa con estados que salen de la evidencia | [Odessa Oil](#odessa-oil) |",
        "| Depende de que una persona responda o salga a buscar clientes | IA aplicada con reglas, contexto y aprobación humana | [AIQ](#aiq) · [Burrow Prospect](#burrow-prospect) |",
        "| Necesita unir sitio, CRM y gestión de proyectos | Plataformas integrales con módulos de dominio | [Ninth Group](#ninth-group) |",
        "",
        "**Cómo leer las fichas.** Cada una separa *problema*, *stack* y *solución*; los casos destacados suman *participación y evidencia* "
        "(producción, código y pruebas, verificados el 16-11-2026). Las fichas 1 a 55 son proyectos desarrollados en mis repositorios; "
        "las 56 a 61 son colaboraciones en repositorios de terceros, y cada una indica mi participación.\n",
    ]
    return "\n".join(out) + "\n"


total = len(rows)
total_mer = 0
report = []
body_parts = []
idx = 0
for g in groups:
    body_parts.append(f'\n<img src="docs/readme/divider.svg" alt="" width="100%">\n\n<a name="{group_anchor(g)}"></a>\n\n## {gicon(g)} {g}\n')
    for gg, p, n in rows:
        if gg != g:
            continue
        idx += 1
        desc, problema, solucion, stack, mer = parse(p)
        ov = OVERRIDES.get(n)
        if ov:
            desc = desc or ov.get("desc", "")
            problema = problema or ov.get("problema", "")
            solucion = solucion or ov.get("solucion", "")
            stack = stack or ov.get("stack", "")
        for fld, old, new in FIXES.get(n, []):
            cur = {"desc": desc, "problema": problema, "solucion": solucion}[fld]
            assert cur.count(old) == 1, f"{n}: no encontré «{old[:50]}» en {fld}"
            cur = cur.replace(old, new)
            desc, problema, solucion = (cur, problema, solucion) if fld == "desc" else (desc, cur, solucion) if fld == "problema" else (desc, problema, cur)
        total_mer += len(mer)
        report.append(f"{idx:2d}. {n:38s} prob={len(problema):4d} sol={len(solucion):4d} stack={len(stack):4d} mermaid={len(mer)}" + ("  ⚠VACÍO" if not (problema and solucion and stack) else ""))
        prim, alias = ANCHORS.get(n, (slug(n), []))
        s = ["".join(f'<a name="{a}"></a>' for a in [prim] + alias), f"### {idx}. {n}"]
        if desc:
            s.append(f"> {desc}\n")
        if n in FEAT_BY_NAME:
            fp = FEAT_BY_NAME[n]
            s.append(f'<img src="assets/portfolio/projects/{fp["slug"]}/arquitectura-1200x675.png" width="100%" alt="{fp["nombre"]} — arquitectura y stack verificado">\n')
        if problema:
            s.append(f"{TAG['problema']}\n\n{problema}\n")
        if stack:
            s.append(f"{TAG['stack']}\n\n{stack}\n")
        if solucion:
            s.append(f"{TAG['solucion']}\n\n{solucion}\n")
        if n in EVIDENCE:
            s.append(f"{TAG['evidencia']}\n\n" + "\n".join(f"- {x}" for x in EVIDENCE[n]) + "\n")
        if mer:
            s.append(f"<details>\n<summary><img src='docs/readme/ic-diagramas.svg' width='16' height='16' alt=''> <b>Ver {len(mer)} diagramas y flujos</b></summary>\n<br>\n")
            for lab, blk in mer:
                if lab:
                    s.append(f"**{lab}**\n")
                s.append(blk + "\n")
            s.append("</details>\n")
        s.append("[↑ Volver al índice](#indice)\n")
        body_parts.append("\n".join(s) + "\n---\n")

# índice
index = [f"<a name=\"indice\"></a>\n## {ICON('indice', 26)} Índice\n", "**Empezá por acá:** [Casos destacados](#casos-destacados) · [Qué problemas resuelvo](#problemas) · [Contacto](#contacto)\n"]
for g in groups:
    index.append(f"**{g}**  ")
    links = []
    for gg, p, n in rows:
        if gg == g:
            links.append(f"[{n}](#{ANCHORS.get(n, (slug(n), []))[0]})")
    index.append(" · ".join(links) + "\n")

head = f"""<div align="center">

<img src="docs/readme/banner.svg" alt="Portafolio — Ing. Santiago Abasto" width="100%">

<br/>

**Ingeniero de software · {total} proyectos · Bolivia**
Sistemas de gestión y POS, e-commerce, IA y datos, apps móviles y sitios web — de principio a fin.

![Proyectos](https://img.shields.io/badge/proyectos-{total}-0ea5e9?style=for-the-badge)
![Diagramas](https://img.shields.io/badge/diagramas-{total_mer}-22c55e?style=for-the-badge)
![Stack](https://img.shields.io/badge/full--stack-Laravel·React·Flutter·Next·IA-6366f1?style=for-the-badge)

</div>

<div align="center">

### ¿Tu empresa depende de Excel, WhatsApp o procesos manuales?

**Diseño y desarrollo sistemas que convierten esos procesos en operaciones controladas, integradas y preparadas para crecer.**
Casos reales de sistemas empresariales, POS, CRM, industria, e-commerce, automatización e IA.

**{total} proyectos · {total_mer} diagramas · Laravel · React · Flutter · APIs · IA**

<a href="#sistemas"><img src="docs/readme/btn-sistemas.svg" height="46" alt="Sistemas empresariales"></a>
<a href="#ia"><img src="docs/readme/btn-ia.svg" height="46" alt="IA y automatización"></a>
<a href="#industria"><img src="docs/readme/btn-industria.svg" height="46" alt="Industria y B2B"></a>
<a href="#contacto"><img src="docs/readme/btn-contacto.svg" height="46" alt="Contactarme"></a>

</div>

Este documento reúne mi trabajo en un solo lugar. Cada proyecto dice **qué problema resolvía**, **con qué stack** y **qué solución le dimos**, con sus **diagramas de arquitectura y flujos** (se despliegan al hacer clic). Desarrollo de **Ing. Santiago Abasto**; las colaboraciones están marcadas al final.

"""

foot = f"""
<img src="docs/readme/divider.svg" alt="" width="100%">

<a name="contacto"></a>

## {ICON('contacto', 26)} Contacto

**Ing. Santiago Abasto** — Ingeniero de software full-stack.
Diseño, construyo y despliego el producto completo: backend, frontend, móvil, datos e IA.

<a href="https://www.linkedin.com/in/santiagoabasto/"><img src="docs/readme/btn-linkedin.svg" height="46" alt="LinkedIn"></a>
<a href="https://burrowlabs.com.bo"><img src="docs/readme/btn-burrow.svg" height="46" alt="Burrow Labs"></a>

> Portafolio generado el 2026-11-16. {total} proyectos · {total_mer} diagramas. Cada ficha enlaza su arquitectura y flujos reales; las cifras de pruebas y el estado de producción son los documentados en cada repositorio.

<div align="center"><br/>

**¿Hablamos de tu proyecto?**

</div>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
md = head + destacados() + "\n".join(index) + "\n" + "\n".join(body_parts) + foot
md = "\n".join(EMO.sub("", l).rstrip() if EMO.search(l) else l for l in md.split("\n"))
OUT.write_text(md, encoding="utf-8")
print("\n".join(report))
print(f"\nTOTAL proyectos={total}  diagramas={total_mer}  -> {OUT}  ({OUT.stat().st_size} bytes)")
