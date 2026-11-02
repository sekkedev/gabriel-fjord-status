"""Build standalone pages: prototype/<page>.html + base.css + data.json + assets -> dist/.

- prototype/template.html -> dist/index.html (the fjord status page)
- prototype/gabby.html    -> dist/gabby/index.html (Gabby's demo daily-post profile)
- prototype/screen.html   -> dist/screen/index.html (a silent rotating screen for Bybanen)

Images and fonts are inlined as data URIs, so the pages need no network.

Run from the project root:  python scripts/build.py
"""
import base64
import re
import shutil
from pathlib import Path

root = Path(__file__).resolve().parent.parent
proto = root / "prototype"
base_css = (proto / "base.css").read_text(encoding="utf-8")
data = (proto / "data.json").read_text(encoding="utf-8")
assets = proto / "assets"
MIME = {".webp": "image/webp", ".png": "image/png", ".svg": "image/svg+xml", ".woff2": "font/woff2"}
PAGES = {"template.html": "index.html", "gabby.html": "gabby/index.html", "screen.html": "screen/index.html"}


def inline_asset(match):
    """Replace __ASSET_name__ with a data URI so the page stays one self-contained file."""
    name = match.group(1)
    hits = [p for p in assets.glob(name + ".*") if p.suffix in MIME]
    if len(hits) != 1:
        raise SystemExit(f"Asset '{name}' missing or ambiguous in {assets}: {[p.name for p in hits]}")
    p = hits[0]
    return f"data:{MIME[p.suffix]};base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"


for src, dst in PAGES.items():
    # base.css first, since it holds __ASSET_font-*__ placeholders of its own
    body = (proto / src).read_text(encoding="utf-8").replace("/*__BASE_CSS__*/", base_css)
    body = re.sub(r"__ASSET_([a-z0-9-]+)__", inline_asset, body).replace("__DATA__", data)

    # The templates have no <html>/<head>/<body> of their own (the first was a Claude artifact),
    # so wrap them here for a normal browser.
    page = (
        '<!doctype html>\n<html lang="nb">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        "</head>\n<body>\n" + body + "\n</body>\n</html>\n"
    )
    out = root / "dist" / dst
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out} ({out.stat().st_size // 1024} KB)")

# Response headers for the Cloudflare deploy (see wrangler.toml).
shutil.copyfile(proto / "_headers", root / "dist" / "_headers")

# The fonts are embedded in every page, so their licence texts ship with the site (the footers link to them).
(root / "dist" / "licenses").mkdir(exist_ok=True)
for ofl in assets.glob("font-*-OFL.txt"):
    shutil.copyfile(ofl, root / "dist" / "licenses" / ofl.name)
