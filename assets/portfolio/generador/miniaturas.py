#!/usr/bin/env python3
"""Generador de miniaturas del portafolio: un sistema visual reusable.

Dos diseños por proyecto, con la misma identidad y propósitos distintos:
  A · producto      propuesta de valor, capacidades y flujo principal   -> enlace al producto o caso público
  B · arquitectura  arquitectura simplificada, stack y capacidades     -> enlace a la ficha técnica del README
Cada diseño sale en SVG (1200×675 maestro y 1200×630) y se exporta a PNG renderizando el
propio archivo SVG con Chrome headless, así SVG y PNG coinciden por construcción.

Uso:
  python3 miniaturas.py              # SVG + PNG + catálogo
  python3 miniaturas.py --solo-svg   # sin exportar PNG
Los datos viven en proyectos.json (verificados; no agregar cifras sin evidencia).
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from html import escape
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                      # assets/portfolio
SALIDA = RAIZ / "projects"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
W, M = 1200, 72
SANS = "-apple-system,'SF Pro Display','Inter','Segoe UI',Helvetica,Arial,sans-serif"
MONO = "'SF Mono','JetBrains Mono',ui-monospace,Menlo,Consolas,monospace"
ESTADO = {"prod": ("EN PRODUCCIÓN", "#22C55E"), "pend": ("PRODUCCIÓN POR VERIFICAR", "#F59E0B"),
          "dev": ("EN DESARROLLO", "#38BDF8")}
FIRMA = "SANTIAGO ABASTO · INGENIERO DE SOFTWARE"
REPO = "github.com/santiagoAbasto/portfolio-santiago-abasto"

# ---------- métricas de texto (Helvetica por 1000 em; margen para SF Pro) ----------
_LO = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556, 556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500]))
_LOB = dict(zip("abcdefghijklmnopqrstuvwxyz", [556, 611, 556, 611, 556, 333, 611, 611, 278, 278, 556, 278, 889, 611, 611, 611, 611, 389, 556, 333, 611, 556, 778, 556, 556, 500]))
_UP = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_UPB = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [722, 722, 722, 722, 667, 611, 778, 722, 278, 556, 722, 611, 833, 722, 778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611]))
_OT = {" ": 278, ".": 278, ",": 278, "·": 278, "-": 333, "—": 1000, "/": 278, ":": 278, "«": 556, "»": 556, "+": 584, "(": 333, ")": 333}


def tw(s, size, bold=False):
    t = 0
    for ch in s:
        b = unicodedata.normalize("NFD", ch)[0]
        t += (_UPB if bold else _UP).get(b) or (_LOB if bold else _LO).get(b) or (556 if b.isdigit() else _OT.get(b, 600))
    return t * size / 1000 * 1.06


def mw(s, size, ls=0.0):
    return len(s) * 0.602 * size + max(0, len(s) - 1) * ls


def wrap(s, size, maxw, bold=False, maxlines=2, mono=False, ls=0.0):
    medir = (lambda t: mw(t, size, ls)) if mono else (lambda t: tw(t, size, bold))
    # una tecnología no se separa de su versión ("Vue 3.5" -> "Vue\u00a03.5")
    s = re.sub(r"(?<=[A-Za-zÁ-úñ+#]) (?=\d)", "\u00a0", s)
    lines, cur = [], ""
    for word in [w for w in s.split(" ") if w]:
        t = f"{cur} {word}".strip(" ")
        if medir(t) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    # ningún separador "·" queda colgando al borde de una línea
    lines = [l.strip(" ").removesuffix(" ·").removeprefix("· ").strip(" ") for l in lines]
    if len(lines) > maxlines:
        raise ValueError(f"no entra en {maxlines} líneas de {maxw}px: «{s}»")
    return lines


def T(x, y, s, size, fill, weight=400, fam=SANS, ls=0, anchor="start", op=1):
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{fam}" font-size="{size}" font-weight="{weight}" '
            f'letter-spacing="{ls}" fill="{fill}" fill-opacity="{op}" text-anchor="{anchor}">{escape(s)}</text>')


# ---------- componentes ----------
def defs(p):
    a1, a2 = p["acento"]
    return f'''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D1733"/><stop offset="1" stop-color="#070C1A"/></linearGradient>
<radialGradient id="g1" cx="1" cy="0" r=".75"><stop offset="0" stop-color="{a1}" stop-opacity=".20"/><stop offset="1" stop-color="{a1}" stop-opacity="0"/></radialGradient>
<radialGradient id="g2" cx="0" cy="1" r=".7"><stop offset="0" stop-color="{a2}" stop-opacity=".12"/><stop offset="1" stop-color="{a2}" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="48" height="48" patternUnits="userSpaceOnUse"><path d="M48 0H0V48" fill="none" stroke="#FFFFFF" stroke-opacity=".035"/></pattern>
<linearGradient id="acc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a1}" stop-opacity=".75"/><stop offset="1" stop-color="{a2}" stop-opacity=".45"/></linearGradient>
<marker id="ar" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1.5 1.5 8.5 5 1.5 8.5" fill="none" stroke="{a2}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></marker>
</defs>'''


def fondo(H):
    return "".join(f'<rect width="{W}" height="{H}" fill="url(#{i})"/>' for i in ("bg", "grid", "g1", "g2"))


def barra(p, etiqueta):
    txt, col = ESTADO[p["estado"]]
    pw = mw(txt, 12, 1.4) + 46
    px = W - M - pw
    return (T(M, 76, f'CASO {p["n"]:02d} · {etiqueta}', 13, p["acento"][0], 600, MONO, 3)
            + f'<rect x="{px:.1f}" y="54" width="{pw:.1f}" height="32" rx="16" fill="#FFFFFF" fill-opacity=".05" stroke="#FFFFFF" stroke-opacity=".14"/>'
            + f'<circle cx="{px + 19:.1f}" cy="70" r="8" fill="{col}" fill-opacity=".18"/><circle cx="{px + 19:.1f}" cy="70" r="4.2" fill="{col}"/>'
            + T(px + 33, 74.5, txt, 12, "#E2E8F0", 600, MONO, 1.4))


def pie(H, izq):
    return (f'<line x1="{M}" y1="{H - 80}" x2="{W - M}" y2="{H - 80}" stroke="#FFFFFF" stroke-opacity=".10"/>'
            + T(M, H - 44, izq, 13, "#94A3B8", 500, MONO)
            + T(W - M, H - 44, FIRMA, 12, "#64748B", 500, MONO, 2, "end"))


def chips(items, x, y, h, size, fill_col, maxx):
    out = []
    for s in items:
        w = tw(s, size, True) + 34
        if x + w > maxx:
            raise ValueError(f"chips desbordan: {items}")
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" fill="{fill_col}" fill-opacity=".10" stroke="{fill_col}" stroke-opacity=".55"/>'
                   + T(x + w / 2, y + h / 2 + size * 0.36, s, size, "#E2E8F0", 600, anchor="middle"))
        x += w + 10
    return "".join(out)


def svg(H, cuerpo, p, titulo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(titulo)}">\n'
            f'{defs(p)}\n{fondo(H)}\n{cuerpo}\n</svg>\n')


# ---------- diseño A · producto ----------
def producto(p, H):
    a1, a2 = p["acento"]
    yN = 176 if H == 675 else 164
    o = [barra(p, p["categoria"]),
         T(M, yN, p["nombre"], 76, "#F8FAFC", 700, ls=-1.6),
         f'<rect x="{M}" y="{yN + 24}" width="72" height="5" rx="2.5" fill="url(#acc)"/>']
    yH = yN + (76 if H == 675 else 72)
    lin = wrap(p["mensaje"], 32, W - 2 * M, maxlines=2)
    o += [T(M, yH + i * 41, l, 32, "#E2E8F0", 500) for i, l in enumerate(lin)]
    yC = yH + (len(lin) - 1) * 41 + (34 if H == 675 else 30)
    o.append(chips(p["chips"], M, yC, 36, 15, a1, W - M))
    yP = yC + 36 + (40 if H == 675 else 34)
    o.append(T(M, yP, "EL PROBLEMA", 11, "#64748B", 700, MONO, 2.6))
    pl = wrap(p["problema"], 19, W - 2 * M, maxlines=2)
    o += [T(M, yP + 26 + i * 25, l, 19, "#CBD5E1", 400) for i, l in enumerate(pl)]
    finP = yP + 26 + (len(pl) - 1) * 25 + 6
    # flujo principal (proceso real del sistema)
    nh = 84 if H == 675 else 78
    bot = H - 122
    top, gap = bot - nh, 44
    nw = (W - 2 * M - 3 * gap) / 4
    if top - 16 < finP + 24:
        raise ValueError(f"{p['slug']}: el flujo choca con las capacidades en {H}")
    o.append(T(M, top - 16, "FLUJO PRINCIPAL", 12, "#64748B", 600, MONO, 3))
    for i, paso in enumerate(p["flujo"]):
        x = M + i * (nw + gap)
        o.append(f'<rect x="{x:.1f}" y="{top}" width="{nw:.1f}" height="{nh}" rx="14" fill="#0E1730" stroke="url(#edge)" stroke-width="1.3"/>')
        o.append(T(x + 18, top + 25, f"{i + 1:02d}", 12, a1, 700, MONO, 1.5))
        pl = wrap(paso, 16, nw - 36, True, 2)
        o += [T(x + 18, top + 49 + j * 20, l, 16, "#F1F5F9", 600) for j, l in enumerate(pl)]
        if i < 3:
            ya = top + nh / 2
            o.append(f'<line x1="{x + nw + 8:.1f}" y1="{ya}" x2="{x + nw + gap - 9:.1f}" y2="{ya}" stroke="{a2}" stroke-width="1.6" stroke-opacity=".9" marker-end="url(#ar)"/>')
    izq = ("↗ " if p["enlace"] else "○ ") + p["enlace_txt"]
    o.append(pie(H, izq))
    return svg(H, "\n".join(o), p, f'{p["nombre"]} — {p["mensaje"]}')


# ---------- diseño B · arquitectura ----------
def caja(x, y, w, lines, size, fill, stroke, dash=False, color="#E2E8F0", weight=500, op_fill=".05", op_stroke=".16", pad=18, lh=17):
    h = pad + lh * len(lines)
    d = ' stroke-dasharray="4 3"' if dash else ""
    s = f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="9" fill="{fill}" fill-opacity="{op_fill}" stroke="{stroke}" stroke-opacity="{op_stroke}"{d}/>'
    base = y + pad / 2 + size * 0.95
    s += "".join(T(x + 13, base + j * lh, l, size, color, weight) for j, l in enumerate(lines))
    return s, h


def flecha(x1, y1, x2, y2, col):
    xm = (x1 + x2) / 2
    path = f"M{x1:.1f} {y1:.1f}H{xm:.1f}V{y2:.1f}H{x2:.1f}" if abs(y1 - y2) > .5 else f"M{x1:.1f} {y1:.1f}H{x2:.1f}"
    return f'<path d="{path}" fill="none" stroke="{col}" stroke-width="1.4" stroke-opacity=".75" marker-end="url(#ar)"/>'


def arquitectura(p, H):
    a1, a2 = p["acento"]
    yN = 148 if H == 675 else 138
    o = [barra(p, "ARQUITECTURA Y EVIDENCIA"),
         T(M, yN, p["nombre"], 50, "#F8FAFC", 700, ls=-1),
         T(M, yN + 34, "Arquitectura simplificada · stack verificado en el código", 18, "#94A3B8", 500)]
    lab = yN + 80
    top, bot = lab + 22, H - 108
    C1, C2, C3 = (M, 188), (M + 230, 252), (M + 524, 170)
    for (x, _), t in zip((C1, C2, C3), ("USUARIOS Y CANALES", "APLICACIÓN", "DATOS E INTEGRACIONES")):
        o.append(T(x, lab, t, 11, "#64748B", 700, MONO, 2.4))
    # columna 1: canales
    bloques = [wrap(c, 13.5, C1[1] - 26, maxlines=2) for c in p["canales"]]
    alto = sum(18 + 17 * len(b) for b in bloques) + 12 * (len(bloques) - 1)
    y = top + (bot - top - alto) / 2
    c1 = []
    for b in bloques:
        s, h = caja(C1[0], y, C1[1], b, 13.5, "#FFFFFF", "#FFFFFF")
        o.append(s)
        c1.append(y + h / 2)
        y += h + 12
    # columna 2: aplicación
    hl = wrap(p["app"], 12, C2[1] - 28, maxlines=2, mono=True, ls=.3)
    hh = 16 + 16 * len(hl)
    ah = hh + 12 + 34 * len(p["modulos"]) + 6
    ay = top + (bot - top - ah) / 2
    o.append(f'<rect x="{C2[0]}" y="{ay:.1f}" width="{C2[1]}" height="{ah:.1f}" rx="12" fill="#0E1730" stroke="url(#edge)" stroke-width="1.4"/>')
    o += [T(C2[0] + 14, ay + 22 + j * 16, l, 12, a1, 700, MONO, .3) for j, l in enumerate(hl)]
    o.append(f'<line x1="{C2[0] + 14}" y1="{ay + hh:.1f}" x2="{C2[0] + C2[1] - 14}" y2="{ay + hh:.1f}" stroke="#FFFFFF" stroke-opacity=".12"/>')
    for j, mod in enumerate(p["modulos"]):
        yy = ay + hh + 12 + j * 34
        wrap(mod, 14, C2[1] - 44, True, 1)
        o.append(f'<rect x="{C2[0] + 14}" y="{yy + 6:.1f}" width="7" height="7" rx="1.5" fill="{a2}"/>')
        o.append(T(C2[0] + 30, yy + 14, mod, 14, "#F1F5F9", 600))
    # columna 3: datos e integraciones
    items = [("d", wrap(d, 12.5, C3[1] - 26, maxlines=2)) for d in p["datos"]] + [("i", wrap(i, 12.5, C3[1] - 26, maxlines=2)) for i in p["integraciones"]]
    alto3 = sum(14 + 16 * len(b) for _, b in items) + 8 * (len(items) - 1) + 22
    y = top + (bot - top - alto3) / 2
    c3, sep = [], False
    for kind, b in items:
        if kind == "i" and not sep:
            o.append(T(C3[0], y + 11, "EXTERNOS", 10, "#64748B", 700, MONO, 2))
            y += 22
            sep = True
        if kind == "d":
            s, h = caja(C3[0], y, C3[1], b, 12.5, a2, a2, op_fill=".10", op_stroke=".45", pad=14, lh=16)
        else:
            s, h = caja(C3[0], y, C3[1], b, 12.5, "#FFFFFF", "#FFFFFF", dash=True, op_fill=".02", op_stroke=".30", pad=14, lh=16)
        o.append(s)
        c3.append(y + h / 2)
        y += h + 8
    if y - 8 > bot + 1:
        raise ValueError(f"{p['slug']}: la columna de datos no entra en {H}")
    clamp = lambda v: min(max(v, ay + 18), ay + ah - 18)
    o += [flecha(C1[0] + C1[1] + 4, cy, C2[0] - 3, clamp(cy), a2) for cy in c1]
    o += [flecha(C2[0] + C2[1] + 4, clamp(cy), C3[0] - 3, cy, a2) for cy in c3]
    # panel derecho: stack y capacidades
    PX, PW = 806, W - M - 806
    o.append(T(PX, lab, "STACK VERIFICADO", 11, "#64748B", 700, MONO, 2.4))
    compacto = H == 630
    ch, g = (30, 8) if compacto else (32, 9)
    bs, blh, bg = (14, 18, 10) if compacto else (15, 20, 12)
    cw = (PW - 10) / 2
    for k, s in enumerate(p["stack"]):
        x, yy = PX + (k % 2) * (cw + 10), top + (k // 2) * (ch + g)
        if tw(s, 14, True) > cw - 16:
            raise ValueError(f"chip de stack demasiado largo: {s}")
        o.append(f'<rect x="{x:.1f}" y="{yy:.1f}" width="{cw:.1f}" height="{ch}" rx="8" fill="#FFFFFF" fill-opacity=".05" stroke="{a1}" stroke-opacity=".40"/>')
        o.append(T(x + cw / 2, yy + ch / 2 + 5, s, 14, "#E2E8F0", 600, anchor="middle"))
    yy = top + ((len(p["stack"]) + 1) // 2) * (ch + g) + (26 if compacto else 30)
    o.append(T(PX, yy, "CAPACIDADES VERIFICADAS", 11, "#64748B", 700, MONO, 2.4))
    yy += 24 if compacto else 26
    for cap in p["capacidades"]:
        cl = wrap(cap, bs, PW - 20, maxlines=2)
        o.append(f'<rect x="{PX}" y="{yy - 10:.1f}" width="7" height="7" rx="1.5" fill="{a1}"/>')
        o += [T(PX + 18, yy + j * blh, l, bs, "#CBD5E1", 500) for j, l in enumerate(cl)]
        yy += blh * len(cl) + bg
    yy -= bg - 12
    if yy - 12 > bot + 8:
        raise ValueError(f"{p['slug']}: las capacidades no entran en {H} ({yy:.0f} > {bot + 8})")
    o.append(pie(H, f"↗ {REPO}#{p['ancla']}"))
    return svg(H, "\n".join(o), p, f'{p["nombre"]} — arquitectura y stack verificado')


# ---------- salida ----------
def exportar_png(svg_path, png_path, H):
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>html,body{{margin:0;background:#070C1A}}img{{display:block}}</style></head><body><img src="{svg_path.name}" width="{W}" height="{H}"></body></html>'
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=svg_path.parent, delete=False, encoding="utf-8") as f:
        f.write(html)
        tmp = Path(f.name)
    prof = Path(tempfile.gettempdir()) / "miniaturas-chrome"
    try:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        f"--user-data-dir={prof}", "--allow-file-access-from-files", "--virtual-time-budget=3000",
                        f"--window-size={W},{H}", f"--screenshot={png_path}", tmp.as_uri()],
                       check=True, capture_output=True, timeout=90)
    finally:
        tmp.unlink(missing_ok=True)


def main():
    datos = json.loads((AQUI / "proyectos.json").read_text(encoding="utf-8"))["proyectos"]
    solo_svg = "--solo-svg" in sys.argv
    for p in datos:
        d = SALIDA / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        for nombre, fn in (("producto", producto), ("arquitectura", arquitectura)):
            for H, sufijo in ((675, ""), (630, "-1200x630")):
                f = d / f"{nombre}{sufijo}.svg"
                f.write_text(fn(p, H), encoding="utf-8")
                if not solo_svg:
                    exportar_png(f, d / f"{nombre}-1200x{H}.png", H)
        print(f"  {p['slug']}: listo")
    print(f"{len(datos)} proyectos · {len(datos) * 2} diseños · {len(datos) * 4} SVG · {0 if solo_svg else len(datos) * 4} PNG")


if __name__ == "__main__":
    main()
