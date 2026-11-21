#!/usr/bin/env python3
"""Render the README charts in docs/ from committed benchmark data."""
import argparse
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAC_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS = (
    "https://fonts.googleapis.com/css2?family=Figtree:wght@400;600;700"
    "&family=Space+Mono:ital,wght@0,400;0,700;1,400"
    "&family=Zilla+Slab:wght@700&display=swap"
)
THEMES = ("light", "dark")
QUOTE = "why waste time say lot word when few word do trick?"

PALETTE = {
    "light": {
        "bg": "#f4f1ea", "ink": "#1b1a16", "muted": "#5f5a4e", "faint": "#8a8474",
        "rule": "#dcd6c8", "normal": "#cbc2b0", "normal_line": "#a89f8c",
        "normal_ink": "#6b6455", "kevin": "#4a8bc2", "kevin_ink": "#2f6a9e",
        "gap": "rgba(74,139,194,0.10)", "on_kevin": "#ffffff", "grid": "#e0dbce",
    },
    "dark": {
        "bg": "#1b1a16", "ink": "#f1ece0", "muted": "#a39c8b", "faint": "#7d7767",
        "rule": "#3a382f", "normal": "#cbc2b0", "normal_line": "#a89f8c",
        "normal_ink": "#8a8372", "kevin": "#4a8bc2", "kevin_ink": "#4a8bc2",
        "gap": "rgba(74,139,194,0.10)", "on_kevin": "#ffffff", "grid": "#34322a",
    },
}

CSS = """
:root{--bg:%(bg)s;--ink:%(ink)s;--muted:%(muted)s;--faint:%(faint)s;--rule:%(rule)s;
--normal:%(normal)s;--normal-line:%(normal_line)s;--normal-ink:%(normal_ink)s;
--kevin:%(kevin)s;--kevin-ink:%(kevin_ink)s;--gap:%(gap)s;--on-kevin:%(on_kevin)s;--grid:%(grid)s}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx;background:var(--bg);overflow:hidden}
body{color:var(--ink);font-family:'Figtree',sans-serif;-webkit-font-smoothing:antialiased}
.stage{position:relative;width:%(w)dpx;height:%(h)dpx}
.mono{font-family:'Space Mono',monospace}
.slab{font-family:'Zilla Slab',serif;font-weight:700}
svg{position:absolute;left:0;top:0}
svg text{font-family:'Space Mono',monospace}
"""


def page(theme, width, height, body, extra_css=""):
    css = CSS % {**PALETTE[theme], "w": width, "h": height}
    return (
        f'<!doctype html><html><head><meta charset="utf-8">'
        f'<link rel="preconnect" href="https://fonts.googleapis.com">'
        f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link href="{FONTS}" rel="stylesheet">'
        f"<style>{css}{extra_css}</style></head>"
        f'<body><div class="stage">{body}</div></body></html>'
    )


def find_chrome():
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    if Path(MAC_CHROME).exists():
        return MAC_CHROME
    for name in ("google-chrome", "chromium"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit("Chrome not found: install Google Chrome or Chromium, or set CHROME to its binary")


def render(chrome, html_text, out, width, height, workdir):
    src = Path(workdir) / (out.stem + ".html")
    src.write_text(html_text, encoding="utf-8")
    out.parent.mkdir(parents=True, exist_ok=True)
    shot = Path(workdir) / (out.stem + ".png")
    result = subprocess.run(
        [
            chrome, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
            f"--window-size={width},{height}", "--virtual-time-budget=8000",
            f"--screenshot={shot}", src.as_uri(),
        ],
        capture_output=True, text=True,
    )
    # Chrome can exit nonzero from its teardown watchdog after the screenshot is already written.
    if not shot.exists():
        sys.exit(f"Chrome failed to render {out} (exit {result.returncode}):\n{result.stderr[-2000:]}")
    shutil.move(str(shot), str(out))


def esc(text):
    return html.escape(str(text), quote=True)


def display_name(model_id):
    parts = model_id.removeprefix("claude-").split("-")
    family = [p for p in parts if not p.isdigit()]
    version = [p for p in parts if p.isdigit()]
    name = " ".join(p.title() for p in family) or model_id
    return f"{name} {'.'.join(version)}" if version else name


def nice_step(value, intervals=3):
    target = value / intervals
    magnitude = 10 ** math.floor(math.log10(target))
    for mult in (1, 1.5, 2, 2.5, 3, 4, 5, 6, 7.5, 10):
        if mult * magnitude >= target:
            return mult * magnitude
    return 10 * magnitude


def tick_label(value):
    return f"{value / 1000:g}k" if value >= 1000 else f"{value:g}"


def header(title, subtitle, legend_html, width=1824):
    return (
        f'<h1 class="slab" style="position:absolute;left:99px;top:85px;font-size:56px;'
        f'line-height:70px;letter-spacing:-1.2px">{esc(title)}</h1>'
        f'<div class="mono" style="position:absolute;left:99px;top:164px;font-size:23px;'
        f'line-height:32px;color:var(--muted)">{esc(subtitle)}</div>'
        f'<div class="mono" style="position:absolute;right:99px;top:101px;font-size:23px;'
        f'line-height:32px;display:flex;gap:34px;align-items:center">{legend_html}</div>'
    )


def headline(text_html, top=227):
    return (
        f'<p style="position:absolute;left:99px;top:{top}px;width:1470px;font-size:31px;'
        f'line-height:48px">{text_html}</p>'
    )


def swatch(css_class, shape):
    var = css_class.replace("_", "-")
    if shape == "line":
        return f'<span style="display:inline-block;width:34px;height:6px;border-radius:3px;background:var(--{var})"></span>'
    return f'<span style="display:inline-block;width:27px;height:27px;border-radius:5px;background:var(--{var})"></span>'


def legend(shape, normal_class):
    gap = "12px" if shape == "box" else "10px"
    return "".join(
        f'<span style="display:flex;align-items:center;gap:{gap}">{swatch(c, shape)}{label}</span>'
        for c, label in ((normal_class, "Normal"), ("kevin", "Kevin"))
    )


def pct_change(plain, kevin):
    return round((kevin - plain) / plain * 100)


def savings_copy(rows):
    cuts = [-r["pct"] for r in rows]
    low, high = min(cuts), max(cuts)
    if low <= 0:
        lo, hi = min(r["pct"] for r in rows), max(r["pct"] for r in rows)
        span = f"{lo:+d}% to {hi:+d}%" if lo != hi else f"{lo:+d}%"
        return f"With Kevin, output tokens change by <b>{span}</b>."
    span = f"{low} to {high}%" if low != high else f"{low}%"
    text = f"Kevin cuts output tokens <b>{span}</b>."
    by_model = {}
    for r in rows:
        by_model.setdefault(r["model"], []).append(r)
    if len(by_model) > 1:
        def mean_cut(model):
            return sum(-r["pct"] for r in by_model[model]) / len(by_model[model])
        best = max(by_model, key=mean_cut)
        by_wordiness = sorted(by_model, key=lambda m: sum(r["plain"] for r in by_model[m]))
        tracks_wordiness = all(
            mean_cut(a) <= mean_cut(b) for a, b in zip(by_wordiness, by_wordiness[1:])
        )
        best_rows = by_model[best]
        cuts_best = [-r["pct"] for r in best_rows]
        if max(cuts_best) - min(cuts_best) <= 3:
            where = f"~{round(mean_cut(best))}% off both prose and code prompts"
        else:
            where = " and ".join(f"{-r['pct']}% off {r['bucket']} prompts" for r in best_rows)
        if tracks_wordiness:
            text += f" The wordier the model, the bigger the win: on {display_name(best)} it strips {where}."
        else:
            text += f" Biggest win: on {display_name(best)}, which strips {where}."
    return text


def input_tax_copy(data):
    taxes = [m["input_tax"] for m in data if m.get("input_tax")]
    if not taxes:
        return ""
    lo, hi = (int(round(f / 50.0)) * 50 for f in (min(taxes), max(taxes)))
    amount = f"{lo:,}" if lo == hi else f"{lo:,} to {hi:,}"
    return (
        f"The voice adds about {amount} input tokens to every request; "
        "prompt caching makes repeats cheaper."
    )


def savings_html(data, theme):
    rows = []
    for m in data:
        for bucket, v in m["buckets"].items():
            rows.append({
                "model": m["model"], "bucket": bucket, "plain": v["plain"], "kevin": v["kevin"],
                "pct": pct_change(v["plain"], v["kevin"]),
            })
    buckets = list(dict.fromkeys(r["bucket"] for r in rows))
    n = len(data)
    pitch, bar_h, x0, x1 = 121.5, 40, 426, 1508
    step = nice_step(max(max(r["plain"], r["kevin"]) for r in rows))
    top = step * 3
    scale = (x1 - x0) / top
    best_cut = min(r["pct"] for r in rows)

    svg, y = [], 395.0
    for bucket in buckets:
        label = f"{bucket} prompts".upper()
        lw = 34 + 17.5 * len(label)
        svg.append(
            f'<text x="99" y="{y + 8}" font-size="22" font-weight="700" letter-spacing="3.2" '
            f'fill="var(--muted)">{esc(label)}</text>'
            f'<line x1="{99 + lw}" x2="1725" y1="{y}" y2="{y}" stroke="var(--rule)" stroke-width="2"/>'
        )
        group_top = y + 48
        for i, m in enumerate(data):
            v = m["buckets"].get(bucket)
            if not v:
                continue
            gy = group_top + i * pitch
            pct = pct_change(v["plain"], v["kevin"])
            wn, wk = v["plain"] * scale, v["kevin"] * scale
            svg.append(
                f'<text x="99" y="{gy + bar_h + 6 + 13}" font-size="27" fill="var(--ink)">'
                f'{esc(display_name(m["model"]))}</text>'
                f'<rect x="{x0}" y="{gy}" width="{wn:.1f}" height="{bar_h}" rx="4" fill="var(--normal)"/>'
                f'<text x="{x0 + wn - 18:.1f}" y="{gy + 28}" font-size="24" text-anchor="end" '
                f'fill="var(--normal-ink)" style="fill:#4a463b">{v["plain"]}</text>'
                f'<rect x="{x0}" y="{gy + 53}" width="{wk:.1f}" height="{bar_h}" rx="4" fill="var(--kevin)"/>'
            )
            if wk >= 90:
                svg.append(
                    f'<text x="{x0 + wk - 18:.1f}" y="{gy + 81}" font-size="24" font-weight="700" '
                    f'text-anchor="end" fill="var(--on-kevin)">{v["kevin"]}</text>'
                )
            else:
                svg.append(
                    f'<text x="{x0 + wk + 12:.1f}" y="{gy + 81}" font-size="24" font-weight="700" '
                    f'fill="var(--kevin-ink)">{v["kevin"]}</text>'
                )
            color = "var(--kevin)" if pct == best_cut else "var(--ink)"
            svg.append(
                f'<text x="1725" y="{gy + bar_h + 6 + 14}" font-size="30" font-weight="700" '
                f'text-anchor="end" fill="{color}">{pct}%</text>'
            )
        y = group_top + n * pitch
        if bucket != buckets[-1]:
            y += 32
    axis_y = y - 1
    svg.append(f'<line x1="{x0}" x2="{x1}" y1="{axis_y}" y2="{axis_y}" stroke="var(--rule)" stroke-width="2"/>')
    for i in range(4):
        tx = x0 + (x1 - x0) * i / 3
        anchor = "start" if i == 0 else "end" if i == 3 else "middle"
        svg.append(
            f'<text x="{tx:.1f}" y="{axis_y + 35}" font-size="22" text-anchor="{anchor}" '
            f'fill="var(--muted)">{tick_label(step * i)}</text>'
        )
    svg.append(f'<text x="1725" y="{axis_y + 33}" font-size="22" text-anchor="end" fill="var(--muted)">tokens</text>')
    rule_y = axis_y + 95
    height = round(rule_y + 178)
    svg.append(f'<line x1="99" x2="1725" y1="{rule_y}" y2="{rule_y}" stroke="var(--rule)" stroke-width="2"/>')

    note = input_tax_copy(data)
    body = (
        header("Output tokens per answer", "median over real API runs · lower is better", legend("box", "normal"))
        + headline(savings_copy(rows))
        + f'<svg width="1824" height="{height}" viewBox="0 0 1824 {height}">{"".join(svg)}</svg>'
        + f'<p class="mono" style="position:absolute;left:99px;top:{rule_y + 31}px;width:1626px;'
        f'font-size:22px;line-height:34px;color:var(--muted)">{esc(note)}</p>'
    )
    return page(theme, 1824, height, body), 1824, height


def compounding_html(session, theme):
    normal = [t["cum"] for t in session["normal"]]
    kevin = [t["cum"] for t in session["kevin"]]
    n = len(normal)
    step = nice_step(max(normal + kevin))
    top = step * 3
    px0, px1, py0, py1 = 208, 1527, 982, 408
    xs = [px0 + (px1 - px0) * i / (n - 1) for i in range(n)]

    def ypos(v):
        return py0 - (py0 - py1) * v / top

    pct = round((kevin[-1] - normal[-1]) / normal[-1] * 100)
    svg = []
    for i in range(4):
        gy = ypos(step * i)
        color = "var(--rule)" if i == 0 else "var(--grid)"
        svg.append(f'<line x1="{px0}" x2="{px1}" y1="{gy:.1f}" y2="{gy:.1f}" stroke="{color}" stroke-width="2"/>')
        svg.append(
            f'<text x="189" y="{gy + 8:.1f}" font-size="21" text-anchor="end" fill="var(--faint)">'
            f'{tick_label(step * i)}</text>'
        )
    upper = [f"{x:.1f},{ypos(v):.1f}" for x, v in zip(xs, normal)]
    lower = [f"{x:.1f},{ypos(v):.1f}" for x, v in zip(xs, kevin)]
    svg.append(f'<polygon points="{" ".join(upper + lower[::-1])}" fill="var(--gap)"/>')
    for pts, color in ((upper, "var(--normal-line)"), (lower, "var(--kevin)")):
        svg.append(
            f'<polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="5" '
            f'stroke-linejoin="round" stroke-linecap="round"/>'
        )
    for series, color, ink in ((normal, "var(--normal-line)", "var(--normal-ink)"), (kevin, "var(--kevin)", "var(--kevin-ink)")):
        ey = ypos(series[-1])
        svg.append(f'<circle cx="{px1}" cy="{ey:.1f}" r="7" fill="{color}"/>')
        svg.append(
            f'<text x="1546" y="{ey + 9:.1f}" font-size="26" font-weight="700" fill="{ink}">'
            f'{series[-1]:,}</text>'
        )
    for i, x in enumerate(xs):
        svg.append(
            f'<text x="{x:.1f}" y="1017" font-size="21" fill="var(--faint)" text-anchor="middle">'
            f'{i + 1}</text>'
        )
    svg.append(f'<text x="867" y="1049" font-size="19" letter-spacing="2" text-anchor="middle" fill="var(--faint)">TURN</text>')
    mid = px0 + (px1 - px0) * 0.76
    idx = min(n - 2, int((mid - px0) / (px1 - px0) * (n - 1)))
    frac = (mid - xs[idx]) / (xs[idx + 1] - xs[idx])
    upper_v = normal[idx] + (normal[idx + 1] - normal[idx]) * frac
    lower_v = kevin[idx] + (kevin[idx + 1] - kevin[idx]) * frac
    mid_y = ypos(upper_v * 0.42 + lower_v * 0.58)
    svg.append(
        f'<text x="{mid:.1f}" y="{mid_y + 11:.1f}" font-size="32" font-weight="700" text-anchor="middle" '
        f'fill="var(--kevin)">{pct}%</text>'
    )
    subtitle = f"One {n}-turn chat on {display_name(session['model'])}. Total tokens, input + output, no caching."
    if pct < 0:
        text = (
            f"By turn {n}, Kevin uses <b>{-pct}% fewer total tokens</b>. Normal’s curve keeps "
            "accelerating: every long reply gets re-sent as history and feeds the next. "
            "Kevin’s grows far slower."
        )
    elif pct > 0:
        text = f"By turn {n}, Kevin uses <b>{pct}% more total tokens</b> than Normal."
    else:
        text = f"By turn {n}, Kevin and Normal use <b>about the same total tokens</b>."
    body = (
        header("Tokens compound over a chat", subtitle, legend("line", "normal_line"))
        + headline(text)
        + f'<svg width="1824" height="1138" viewBox="0 0 1824 1138">{"".join(svg)}</svg>'
    )
    return page(theme, 1824, 1138, body), 1824, 1138


def parse_examples(path):
    sections, current = [], None
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("## "):
            current = {"question": line[3:].strip(), "normal": [], "kevin": [], "words": {}}
            sections.append(current)
            who = None
            continue
        if current is None:
            continue
        m = re.match(r"\*\*(Normal|Kevin)\*\*(?:\s*\((\d+) words?\))?", line)
        if m:
            who = m.group(1).lower()
            if m.group(2):
                current["words"][who] = int(m.group(2))
            continue
        if who and line.startswith(">"):
            current[who].append(re.sub(r"^>\s?", "", line))
    for s in sections:
        for who in ("normal", "kevin"):
            s[who] = "\n".join(s[who]).strip()
            s["words"].setdefault(who, len(s[who].split()))
    return [s for s in sections if s["normal"] and s["kevin"]]


def inline_md(text):
    out = esc(text)
    out = re.sub(r"`([^`]+)`", r'<code>\1</code>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    return out


def markdown(text):
    blocks, para, items, kind = [], [], [], None
    code, fence_indent = None, 0

    def flush():
        nonlocal para, items, kind
        if para:
            blocks.append(f"<p>{inline_md(' '.join(para))}</p>")
        if items:
            blocks.append(f"<{kind}>{''.join(f'<li>{inline_md(i)}</li>' for i in items)}</{kind}>")
        para, items, kind = [], [], None

    for line in text.splitlines():
        stripped = line.strip()
        if code is not None:
            if stripped.startswith("```"):
                blocks.append(f"<pre><code>{esc(chr(10).join(code))}</code></pre>")
                code = None
            else:
                indent = min(fence_indent, len(line) - len(line.lstrip(" ")))
                code.append(line[indent:])
            continue
        if stripped.startswith("```"):
            flush()
            code, fence_indent = [], len(line) - len(line.lstrip(" "))
            continue
        bullet = re.match(r"[-*]\s+(.*)", stripped)
        number = re.match(r"\d+[.)]\s+(.*)", stripped)
        heading = re.match(r"#{1,6}\s+(.*)", stripped)
        if not stripped:
            flush()
        elif heading:
            flush()
            blocks.append(f"<p><b>{inline_md(heading.group(1))}</b></p>")
        elif bullet or number:
            want = "ul" if bullet else "ol"
            if para or (items and kind != want):
                flush()
            kind = want
            items.append((bullet or number).group(1))
        elif items:
            items[-1] += " " + stripped
        else:
            para.append(stripped)
    flush()
    if code is not None:
        blocks.append(f"<pre><code>{esc(chr(10).join(code))}</code></pre>")
    return "".join(blocks)


def before_after_html(example, theme):
    shown = example["question"].lower()
    tokens = shown.split(" ")
    pick = 1 if len(tokens) > 1 else 0
    question = " ".join(
        f'<mark>{esc(t)}</mark>' if i == pick else esc(t) for i, t in enumerate(tokens)
    )
    size = 26.7 if len(shown) <= 46 else max(18, round(26.7 * 46 / len(shown), 1))
    css = f"""
.hd{{position:absolute;left:60px;top:44px;font-size:15px;font-weight:700;letter-spacing:2.5px;
 display:flex;align-items:center;gap:12px;line-height:20px}}
.hd i{{width:9px;height:9px;border-radius:50%;background:var(--kevin);display:block;margin-top:1px}}
.hd span{{color:var(--muted)}}
.q{{position:absolute;right:60px;top:46px;text-align:right}}
.q em{{display:block;font-size:13px;line-height:18px;color:var(--muted)}}
.q small{{display:block;font-size:10.5px;letter-spacing:1.4px;margin-top:3px;color:var(--faint)}}
.ask{{position:absolute;left:60px;top:90px;font-size:{size}px;line-height:54px;color:var(--muted);white-space:nowrap}}
.ask mark{{background:var(--kevin);color:var(--on-kevin);font-weight:700;padding:3px 7px;border-radius:4px}}
.col{{position:absolute;top:155px;height:368px;width:492px;overflow:hidden}}
.col .t{{display:flex;justify-content:space-between;font-size:13px;line-height:18px;letter-spacing:2px;margin-bottom:12px}}
.col .t b{{font-weight:700}} .col .t span{{color:var(--faint)}}
.body{{font-size:18px;line-height:26px}}
.body p,.body ul,.body ol{{margin-bottom:14px}}
.body ul,.body ol{{padding-left:22px}}
.body code{{font-family:'Space Mono',monospace;font-size:15px;background:rgba(128,120,100,.16);padding:1px 4px;border-radius:3px}}
.body pre{{font-family:'Space Mono',monospace;font-size:14px;line-height:20px;background:rgba(128,120,100,.16);padding:8px 10px;border-radius:4px;white-space:pre;overflow:hidden;margin-bottom:14px}}
.body pre code{{background:none;padding:0;font-size:inherit}}
.fade{{position:absolute;left:0;right:0;bottom:0;height:90px;background:linear-gradient(to bottom,transparent,var(--bg))}}
.div{{position:absolute;left:600px;top:153px;height:369px;width:1px;background:var(--rule)}}
.foot{{position:absolute;left:60px;right:60px;top:536px;border-top:3px solid var(--ink)}}
.foot h2{{font-size:38px;line-height:44px;position:absolute;left:0;top:19px;letter-spacing:-.4px;white-space:nowrap}}
.foot div{{position:absolute;right:0;top:16px;font-size:13px;line-height:20px;letter-spacing:-.2px;text-align:right;color:var(--muted)}}
"""
    def column(who, label, left):
        fade = '<div class="fade"></div>'
        return (
            f'<div class="col" style="left:{left}px"><div class="t mono"><b>{label}</b>'
            f'<span>{example["words"][who]} WORDS</span></div>'
            f'<div class="body">{markdown(example[who])}</div>{fade}</div>'
        )

    body = (
        f'<div class="hd mono">KEVIN<i></i><span>CLAUDE CODE PLUGIN</span></div>'
        f'<div class="q mono"><em>"{esc(QUOTE)}"</em><small>— KEVIN MALONE, THE OFFICE</small></div>'
        f'<div class="ask mono">"{question}"</div>'
        + column("normal", "NORMAL", 60)
        + '<div class="div"></div>'
        + column("kevin", "KEVIN", 648)
        + '<div class="foot"><h2 class="slab">WHICH WOULD YOU RATHER READ?</h2>'
        '<div class="mono">same answer, fewer words.<br>prose only: code and commits stay full English.</div></div>'
    )
    return page(theme, 1200, 630, body, css), 1200, 630


def load_json(directory, name):
    path = Path(directory) / name
    if not path.exists():
        sys.exit(f"missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--only", choices=["savings", "compounding", "before-after"])
    p.add_argument("--example", default="What is a memory leak?", help="question to feature in the before-after card")
    p.add_argument("--data-dir", default=ROOT / "benchmarks" / "data")
    p.add_argument("--examples-file", default=ROOT / "examples.md")
    p.add_argument("--out-dir", default=ROOT / "docs")
    args = p.parse_args()
    out_dir = Path(args.out_dir)

    jobs = []
    if args.only in (None, "savings"):
        data = load_json(args.data_dir, "savings.json")
        jobs.append(("savings", lambda t: savings_html(data, t)))
    if args.only in (None, "compounding"):
        session = load_json(args.data_dir, "session.json")
        jobs.append(("compounding", lambda t: compounding_html(session, t)))
    if args.only in (None, "before-after"):
        examples = parse_examples(args.examples_file)
        if not examples:
            sys.exit(f"no examples in {args.examples_file}")
        if args.example:
            wanted = args.example.strip().lower()
            match = [e for e in examples if e["question"].lower() == wanted]
            if not match:
                sys.exit(f"no example titled {args.example!r}")
            example = match[0]
        else:
            example = examples[0]
        jobs.append(("before-after", lambda t: before_after_html(example, t)))

    chrome = find_chrome()
    with tempfile.TemporaryDirectory(prefix="kevin-charts-") as work:
        for name, build in jobs:
            for theme in THEMES:
                html_text, w, h = build(theme)
                out = out_dir / f"{name}-{theme}.png"
                render(chrome, html_text, out, w, h, work)
                print(out)


if __name__ == "__main__":
    main()
