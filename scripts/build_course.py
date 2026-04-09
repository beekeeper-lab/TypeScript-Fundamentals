#!/usr/bin/env python3
"""Build the TypeScript Fundamentals course from markdown source to HTML."""

import argparse
import base64
import json
import re
from pathlib import Path

try:
    import markdown
    from markdown.extensions.codehilite import CodeHiliteExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.toc import TocExtension
except ImportError:
    print("ERROR: markdown package not installed. Run: pip install markdown pygments")
    raise SystemExit(1)


PROJECT_ROOT = Path(__file__).parent.parent
SOURCE_DIR = PROJECT_ROOT / "source"
IMAGES_DIR = PROJECT_ROOT / "images"
AUDIO_DIR = PROJECT_ROOT / "audio"
HTML_DIR = PROJECT_ROOT / "html"

# Module ordering and metadata
MODULES = [
    {"file": "module-00-what-is-typescript.md", "short": "Module 0", "title": "What Is TypeScript", "hero": "module-00/m00-hero.png", "tier": "Start Here", "tier_css": "tier-start-here"},
    {"file": "module-01-variables-and-types.md", "short": "Module 1", "title": "Variables and Types", "hero": "module-01/m01-hero.png", "tier": "Start Here", "tier_css": "tier-start-here"},
    {"file": "module-02-arrays-tuples-objects.md", "short": "Module 2", "title": "Arrays, Tuples, and Objects", "hero": "module-02/m02-hero.png", "tier": "Start Here", "tier_css": "tier-start-here"},
    {"file": "module-03-functions.md", "short": "Module 3", "title": "Functions and Type Signatures", "hero": "module-03/m03-hero.png", "tier": "Start Here", "tier_css": "tier-start-here"},
    {"file": "module-04-control-flow.md", "short": "Module 4", "title": "Control Flow", "hero": "module-04/m04-hero.png", "tier": "Start Here", "tier_css": "tier-start-here"},
    {"file": "module-05-type-aliases-and-unions.md", "short": "Module 5", "title": "Type Aliases and Unions", "hero": "module-05/m05-hero.png", "tier": "Useful Soon", "tier_css": "tier-useful-soon"},
    {"file": "module-06-interfaces.md", "short": "Module 6", "title": "Interfaces", "hero": "module-06/m06-hero.png", "tier": "Useful Soon", "tier_css": "tier-useful-soon"},
    {"file": "module-07-classes.md", "short": "Module 7", "title": "Classes", "hero": "module-07/m07-hero.png", "tier": "Useful Soon", "tier_css": "tier-useful-soon"},
    {"file": "module-08-generics.md", "short": "Module 8", "title": "Generics", "hero": "module-08/m08-hero.png", "tier": "Useful Soon", "tier_css": "tier-useful-soon"},
    {"file": "module-09-enums-and-utility-types.md", "short": "Module 9", "title": "Enums and Utility Types", "hero": "module-09/m09-hero.png", "tier": "Useful Soon", "tier_css": "tier-useful-soon"},
    {"file": "module-10-type-narrowing.md", "short": "Module 10", "title": "Type Narrowing", "hero": "module-10/m10-hero.png", "tier": "When You're Ready", "tier_css": "tier-when-ready"},
    {"file": "module-11-modules-and-imports.md", "short": "Module 11", "title": "Modules and Imports", "hero": "module-11/m11-hero.png", "tier": "When You're Ready", "tier_css": "tier-when-ready"},
    {"file": "module-12-async-await.md", "short": "Module 12", "title": "Async/Await and Promises", "hero": "module-12/m12-hero.png", "tier": "When You're Ready", "tier_css": "tier-when-ready"},
    {"file": "module-13-error-handling.md", "short": "Module 13", "title": "Error Handling", "hero": "module-13/m13-hero.png", "tier": "When You're Ready", "tier_css": "tier-when-ready"},
    {"file": "module-14-json-and-apis.md", "short": "Module 14", "title": "JSON and APIs", "hero": "module-14/m14-hero.png", "tier": "When You're Ready", "tier_css": "tier-when-ready"},
    {"file": "module-15-npm-and-packages.md", "short": "Module 15", "title": "npm and Package Management", "hero": "module-15/m15-hero.png", "tier": "Advanced", "tier_css": "tier-advanced"},
    {"file": "module-16-tsconfig.md", "short": "Module 16", "title": "tsconfig and Build Configuration", "hero": "module-16/m16-hero.png", "tier": "Advanced", "tier_css": "tier-advanced"},
    {"file": "module-17-testing.md", "short": "Module 17", "title": "Testing with Vitest", "hero": "module-17/m17-hero.png", "tier": "Advanced", "tier_css": "tier-advanced"},
    {"file": "module-18-advanced-patterns.md", "short": "Module 18", "title": "Decorators and Advanced Patterns", "hero": "module-18/m18-hero.png", "tier": "Advanced", "tier_css": "tier-advanced"},
    {"file": "module-19-capstone-project.md", "short": "Module 19", "title": "Capstone: Task Tracker CLI", "hero": "module-19/m19-hero.png", "tier": "Advanced", "tier_css": "tier-advanced"},
]

EXTRAS = []

REFERENCES = []


def image_to_base64(image_path: Path) -> str | None:
    """Convert an image file to a base64 data URI."""
    if not image_path.exists():
        return None
    data = base64.b64encode(image_path.read_bytes()).decode()
    return f"data:image/png;base64,{data}"


def resolve_image_path(src: str) -> Path | None:
    """Resolve a markdown image src to an absolute path."""
    clean = src.replace("../images/", "").replace("images/", "")
    candidate = IMAGES_DIR / clean
    if candidate.exists():
        return candidate
    return None


def embed_images(html_content: str) -> str:
    """Replace image src paths with base64-embedded data URIs."""
    def replace_img(match):
        full_tag = match.group(0)
        src = match.group(1)
        img_path = resolve_image_path(src)
        if img_path:
            data_uri = image_to_base64(img_path)
            if data_uri:
                return full_tag.replace(src, data_uri)
        return full_tag

    return re.sub(r'<img[^>]+src="([^"]+)"', replace_img, html_content)


def process_narration_blocks(html_content: str, module_stem: str) -> str:
    """Convert narration blockquotes into audio player widgets."""
    audio_module_dir = AUDIO_DIR / module_stem

    manifest_path = audio_module_dir / "manifest.json"
    audio_files = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for entry in manifest:
            audio_files[entry["index"]] = entry

    narration_counter = 0

    def replace_narration(match):
        nonlocal narration_counter
        narration_counter += 1
        content = match.group(1)

        display_text = re.sub(r'🎙️\s*', '', content)
        if not display_text.strip().startswith('<p>'):
            display_text = f'<p>{display_text.strip()}</p>'

        audio_entry = audio_files.get(narration_counter)
        audio_html = ""
        if audio_entry:
            audio_path = audio_module_dir / audio_entry["audio_file"]
            if audio_path.exists():
                audio_b64 = base64.b64encode(audio_path.read_bytes()).decode()
                audio_html = f'''
                <button class="narration-play" onclick="playNarration(this)" aria-label="Play narration">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M8 5v14l11-7z"/>
                    </svg>
                </button>
                <audio preload="none">
                    <source src="data:audio/mpeg;base64,{audio_b64}" type="audio/mpeg">
                </audio>'''

        return f'''<div class="narration-block">
            <div class="narration-icon">🎙️</div>
            <div class="narration-content">{display_text}</div>
            {audio_html}
        </div>'''

    html_content = re.sub(
        r'<blockquote>\s*((?:<p>)*🎙️.*?)\s*</blockquote>',
        replace_narration,
        html_content,
        flags=re.DOTALL,
    )

    html_content = re.sub(
        r'<p>(🎙️.*?)</p>',
        replace_narration,
        html_content,
        flags=re.DOTALL,
    )

    return html_content


def process_tier_badges(html_content: str) -> str:
    """Convert tier markers into styled badge elements."""
    tier_classes = {
        "Start Here": "tier-start-here",
        "Useful Soon": "tier-useful-soon",
        "When You're Ready": "tier-when-ready",
        "Advanced": "tier-advanced",
    }

    def replace_tier(match):
        content = match.group(1)
        text = re.sub(r'🏷️\s*', '', content).strip()
        tier_name = text.split('.')[0].split(':')[0].strip()
        css_class = tier_classes.get(tier_name, "tier-start-here")
        rest = text[len(tier_name):].lstrip('.:').strip()
        readiness = f'<div class="readiness-note">{rest}</div>' if rest else ''
        return f'<div class="tier-badge {css_class}">{tier_name}</div>{readiness}'

    html_content = re.sub(
        r'<blockquote>\s*(?:<p>)*(🏷️.*?)(?:</p>)*\s*</blockquote>',
        replace_tier, html_content, flags=re.DOTALL,
    )
    html_content = re.sub(
        r'<p>(🏷️.*?)</p>',
        replace_tier, html_content, flags=re.DOTALL,
    )
    return html_content


def process_cycle_anchor_blocks(html_content: str) -> str:
    """Convert cycle anchor blockquotes into styled anchor blocks."""

    def replace_anchor(match):
        content = match.group(1)
        display_text = re.sub(r'🔄\s*', '', content)
        if not display_text.strip().startswith('<'):
            display_text = f'<p>{display_text.strip()}</p>'
        return f'''<div class="cycle-anchor">
            <div class="cycle-anchor-icon">🔄</div>
            <div>{display_text}</div>
        </div>'''

    html_content = re.sub(
        r'<blockquote>\s*((?:<p>)*🔄.*?)\s*</blockquote>',
        replace_anchor, html_content, flags=re.DOTALL,
    )
    html_content = re.sub(
        r'<p>(🔄.*?)</p>',
        replace_anchor, html_content, flags=re.DOTALL,
    )
    return html_content


def process_remember_blocks(html_content: str) -> str:
    """Convert remember-one-thing blockquotes into styled callout blocks."""

    def replace_remember(match):
        content = match.group(1)
        display_text = re.sub(r'💡\s*', '', content)
        if not display_text.strip().startswith('<'):
            display_text = f'<p>{display_text.strip()}</p>'
        return f'''<div class="remember-one-thing">
            <div class="remember-icon">💡</div>
            <div class="remember-content">{display_text}</div>
        </div>'''

    html_content = re.sub(
        r'<blockquote>\s*((?:<p>)*💡.*?)\s*</blockquote>',
        replace_remember, html_content, flags=re.DOTALL,
    )
    html_content = re.sub(
        r'<p>(💡.*?)</p>',
        replace_remember, html_content, flags=re.DOTALL,
    )
    return html_content


def process_teaching_intent_blocks(html_content: str) -> str:
    """Convert teaching intent blockquotes into styled intent blocks."""

    def replace_intent(match):
        content = match.group(1)
        display_text = re.sub(r'🎯\s*', '', content)
        if not display_text.strip().startswith('<p>') and not display_text.strip().startswith('<strong>'):
            display_text = f'<p>{display_text.strip()}</p>'

        return f'''<div class="teaching-intent">
            <div class="intent-icon">🎯</div>
            <div class="intent-content">{display_text}</div>
        </div>'''

    html_content = re.sub(
        r'<blockquote>\s*((?:<p>)*🎯.*?)\s*</blockquote>',
        replace_intent,
        html_content,
        flags=re.DOTALL,
    )

    html_content = re.sub(
        r'<p>(🎯.*?)</p>',
        replace_intent,
        html_content,
        flags=re.DOTALL,
    )

    return html_content


def convert_markdown_to_html(source_path: Path) -> tuple[str, str]:
    """Convert a markdown file to HTML content. Returns (title, html_body, toc)."""
    text = source_path.read_text()

    title_match = re.match(r'^#\s+(.+)', text, re.MULTILINE)
    title = title_match.group(1) if title_match else source_path.stem

    md = markdown.Markdown(
        extensions=[
            FencedCodeExtension(),
            CodeHiliteExtension(css_class="highlight", guess_lang=False),
            TableExtension(),
            TocExtension(permalink=False, toc_depth="2-3"),
            "md_in_html",
        ]
    )

    html_body = md.convert(text)
    toc = md.toc

    return title, html_body, toc


def split_into_pages(html_body: str) -> list[str]:
    """Split HTML body into pages at each <h2> boundary."""
    parts = re.split(r'(?=<h2[ >])', html_body)
    pages = []
    for i, part in enumerate(parts):
        part = part.strip()
        if not part:
            continue
        if i == 0 and not part.startswith('<h2'):
            if len(parts) > 1:
                parts[1] = part + "\n" + parts[1]
                continue
        pages.append(f'<div class="page" data-page="{len(pages)}">{part}</div>')
    return pages if pages else [f'<div class="page" data-page="0">{html_body}</div>']


def build_module_html(
    source_path: Path,
    prev_module: dict | None,
    next_module: dict | None,
    module_index: int,
    total_modules: int,
    embed_media: bool = True,
) -> str:
    """Build a complete HTML page for a module."""
    title, body, toc = convert_markdown_to_html(source_path)
    module_stem = source_path.stem

    # Process special blocks
    body = process_tier_badges(body)
    body = process_cycle_anchor_blocks(body)
    body = process_remember_blocks(body)
    body = process_teaching_intent_blocks(body)

    # Process narration blocks
    body = process_narration_blocks(body, module_stem)

    # Embed images
    if embed_media:
        body = embed_images(body)

    # Split into pages
    pages = split_into_pages(body)
    paginated_body = "\n".join(pages)

    # Navigation
    prev_link = ""
    if prev_module:
        prev_file = prev_module["file"].replace(".md", ".html")
        prev_link = f'<a href="{prev_file}" class="nav-prev">← {prev_module["short"]}: {prev_module["title"]}</a>'

    next_link = ""
    if next_module:
        next_file = next_module["file"].replace(".md", ".html")
        next_link = f'<a href="{next_file}" class="nav-next">{next_module["short"]}: {next_module["title"]} →</a>'

    template_path = Path(__file__).parent / "module_template.html"
    template = template_path.read_text()

    return (template
        .replace("{{TITLE}}", title)
        .replace("{{TOC}}", toc)
        .replace("{{BODY}}", paginated_body)
        .replace("{{PREV_LINK}}", prev_link)
        .replace("{{NEXT_LINK}}", next_link)
    )


def _build_card(mod: dict, prefix: str = "html/") -> str:
    """Build a single module card with embedded hero thumbnail."""
    html_file = prefix + mod["file"].replace(".md", ".html")
    hero_path = IMAGES_DIR / mod.get("hero", "")
    thumb = image_to_base64(hero_path) if hero_path.exists() else ""
    thumb_html = f'<img class="card-thumb" src="{thumb}" alt="">' if thumb else ""
    tier = mod.get("tier", "")
    tier_css = mod.get("tier_css", "")
    tier_html = f'<span class="card-tier {tier_css}">{tier}</span>' if tier else ""
    return f'''
            <a href="{html_file}" class="module-card">
                {thumb_html}
                <div class="card-text">
                    <div class="module-number">{mod["short"]} {tier_html}</div>
                    <div class="module-title">{mod["title"]}</div>
                </div>
                <div class="module-progress"></div>
            </a>'''


def build_index_html() -> str:
    """Build the course landing/index page."""
    sections = {
        "foundations": list(range(0, 5)),
        "intermediate": list(range(5, 10)),
        "advanced": list(range(10, 15)),
        "expert": list(range(15, 20)),
    }
    section_cards = {}
    for section_name, indices in sections.items():
        cards = [_build_card(MODULES[i]) for i in indices if i < len(MODULES)]
        section_cards[section_name] = "\n".join(cards)

    return INDEX_TEMPLATE.format(
        cards_foundations=section_cards["foundations"],
        cards_intermediate=section_cards["intermediate"],
        cards_advanced=section_cards["advanced"],
        cards_expert=section_cards["expert"],
    )


INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TypeScript Fundamentals</title>
<style>
*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

:root {{
    --bg: #ffffff;
    --bg-secondary: #f8f9fa;
    --bg-code: #f4f4f4;
    --text: #1a1a2e;
    --text-secondary: #555;
    --border: #e0e0e0;
    --accent: #3178c6;
    --accent-light: #d6e4f0;
    --narration-bg: #fef3c7;
    --narration-border: #f59e0b;
    --shadow: 0 1px 3px rgba(0,0,0,0.1);
    --font-body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    --font-mono: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
}}

[data-theme="dark"] {{
    --bg: #0f172a;
    --bg-secondary: #1e293b;
    --bg-code: #1e293b;
    --text: #e2e8f0;
    --text-secondary: #94a3b8;
    --border: #334155;
    --accent: #60a5fa;
    --accent-light: #1e3a5f;
    --narration-bg: #422006;
    --narration-border: #d97706;
    --shadow: 0 1px 3px rgba(0,0,0,0.3);
}}

body {{
    font-family: var(--font-body);
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    font-size: 17px;
    transition: background 0.3s, color 0.3s;
}}

.theme-toggle {{
    position: fixed;
    top: 1rem;
    right: 1rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.3rem 0.5rem;
    cursor: pointer;
    font-size: 16px;
    color: var(--text);
    z-index: 100;
}}

.main-content {{
    max-width: 820px;
    margin: 0 auto;
    padding: 2rem 2rem 4rem;
}}

h1 {{ font-size: 2rem; margin: 0 0 0.25rem; line-height: 1.3; }}
h2 {{ font-size: 1.5rem; margin: 2.5rem 0 1rem; padding-top: 1.5rem; border-top: 1px solid var(--border); }}
h3 {{ font-size: 1.2rem; margin: 2rem 0 0.75rem; }}
h2:first-of-type {{ border-top: none; padding-top: 0; }}
p {{ margin: 0.75rem 0; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
strong {{ font-weight: 600; }}

.subtitle {{
    color: var(--text-secondary);
    font-size: 1.1rem;
    margin-bottom: 1.5rem;
}}

.section-label {{
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: var(--text-secondary);
    margin: 2rem 0 0.75rem;
}}

.module-grid {{
    display: grid;
    gap: 0.6rem;
}}

.module-card {{
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.75rem 1rem;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 10px;
    text-decoration: none;
    color: var(--text);
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
    overflow: hidden;
}}

.module-card:hover {{
    border-color: var(--accent);
    box-shadow: var(--shadow);
    transform: translateY(-2px);
    text-decoration: none;
}}

.card-thumb {{
    width: 80px;
    height: 56px;
    object-fit: cover;
    border-radius: 6px;
    flex-shrink: 0;
    box-shadow: none;
    margin: 0;
}}

.card-text {{
    flex: 1;
    min-width: 0;
}}

.module-number {{
    font-weight: 700;
    font-size: 0.8rem;
    color: var(--accent);
    white-space: nowrap;
}}

.module-title {{
    font-size: 0.95rem;
    line-height: 1.3;
}}

.card-tier {{
    font-size: 0.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.15rem 0.45rem;
    border-radius: 100px;
    margin-left: 0.4rem;
    vertical-align: middle;
}}

.tier-start-here {{ background: #dcfce7; color: #166534; border: 1px solid #86efac; }}
.tier-useful-soon {{ background: #dbeafe; color: #1e40af; border: 1px solid #93c5fd; }}
.tier-when-ready {{ background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }}
.tier-advanced {{ background: #f3e8ff; color: #6b21a8; border: 1px solid #c4b5fd; }}

[data-theme="dark"] .tier-start-here {{ background: #052e16; color: #86efac; border-color: #166534; }}
[data-theme="dark"] .tier-useful-soon {{ background: #172554; color: #93c5fd; border-color: #1e40af; }}
[data-theme="dark"] .tier-when-ready {{ background: #451a03; color: #fcd34d; border-color: #92400e; }}
[data-theme="dark"] .tier-advanced {{ background: #3b0764; color: #c4b5fd; border-color: #6b21a8; }}

.module-progress {{
    margin-left: auto;
    font-size: 0.85rem;
    color: var(--text-secondary);
    flex-shrink: 0;
}}

.outcomes {{
    padding-left: 1.75rem;
}}
.outcomes li {{
    margin: 0.4rem 0;
}}

.quick-ref {{
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1.5rem 0;
}}

.quick-ref h3 {{ margin: 0 0 0.75rem; }}

.quick-ref pre {{
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem;
    font-family: var(--font-mono);
    font-size: 0.85rem;
    overflow-x: auto;
    line-height: 1.8;
    margin: 0;
}}

.footer {{
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--text-secondary);
    font-size: 0.85rem;
    border-top: 1px solid var(--border);
    margin-top: 2.5rem;
}}

@media (max-width: 600px) {{
    .main-content {{ padding: 1.5rem 1.25rem 3rem; }}
}}

@media print {{
    .main-content {{ padding: 0; }}
    .theme-toggle {{ display: none !important; }}
}}
</style>
</head>
<body>

<button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">🌓</button>

<main class="main-content">
        <h1>TypeScript Fundamentals</h1>
        <p class="subtitle">A structured, self-paced course in TypeScript for developers</p>

        <h2>What you'll learn</h2>

        <p>This course takes you from zero TypeScript to building complete, well-structured projects. Each module builds on the last, with hands-on code examples you can run immediately.</p>

        <ul class="outcomes">
            <li>TypeScript's <strong>type system</strong> — primitives, arrays, tuples, objects, unions, intersections</li>
            <li>Functions, classes, interfaces, and generics with <strong>full type safety</strong></li>
            <li>Advanced patterns: <strong>type narrowing, discriminated unions, utility types</strong></li>
            <li>Async/await, error handling, and working with <strong>JSON and APIs</strong></li>
            <li>Real-world tooling: <strong>npm, tsconfig.json, testing with Vitest</strong></li>
            <li>Decorators, mapped types, conditional types, and <strong>template literal types</strong></li>
            <li>A complete <strong>capstone project</strong> tying all 20 modules together</li>
        </ul>

        <h2>Self-Study Modules</h2>

        <div class="section-label">Foundations (Start Here)</div>
        <div class="module-grid">
            {cards_foundations}
        </div>

        <div class="section-label">Intermediate (Useful Soon)</div>
        <div class="module-grid">
            {cards_intermediate}
        </div>

        <div class="section-label">Applied (When You're Ready)</div>
        <div class="module-grid">
            {cards_advanced}
        </div>

        <div class="section-label">Advanced</div>
        <div class="module-grid">
            {cards_expert}
        </div>

        <h2>Your Practice Path</h2>

        <div class="quick-ref">
            <pre>After Modules 0-4:   You can write typed functions, arrays, and control flow
After Modules 5-9:   You can model complex data with interfaces, generics, and utility types
After Modules 10-14: You can handle async code, errors, and external data safely
After Modules 15-19: You can set up, test, and structure a complete TypeScript project</pre>
        </div>

    </main>

<script>
function toggleTheme() {{
    const html = document.documentElement;
    const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
}}

(function() {{
    const saved = localStorage.getItem('theme');
    if (saved) document.documentElement.setAttribute('data-theme', saved);
    else if (window.matchMedia('(prefers-color-scheme: dark)').matches)
        document.documentElement.setAttribute('data-theme', 'dark');

    // Mark visited modules with checkmarks
    const visited = JSON.parse(localStorage.getItem('tsfund_visited') || '[]');
    visited.forEach(v => {{
        const card = document.querySelector(`a[href="html/${{v}}.html"]`);
        if (card) {{
            const prog = card.querySelector('.module-progress');
            if (prog) prog.textContent = '✓';
        }}
    }});
}})();
</script>

</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Build TypeScript Fundamentals course HTML")
    parser.add_argument("--no-embed", action="store_true", help="Link images instead of embedding")
    parser.add_argument("--module", help="Build only a specific module (e.g., module-00-what-is-typescript)")
    args = parser.parse_args()

    HTML_DIR.mkdir(parents=True, exist_ok=True)
    embed = not args.no_embed

    if args.module:
        source_path = SOURCE_DIR / f"{args.module}.md"
        if not source_path.exists():
            print(f"ERROR: {source_path} not found")
            return

        idx = next((i for i, m in enumerate(MODULES) if m["file"].startswith(args.module)), -1)
        prev_mod = MODULES[idx - 1] if idx > 0 else None
        next_mod = MODULES[idx + 1] if idx < len(MODULES) - 1 else None

        html = build_module_html(source_path, prev_mod, next_mod, idx, len(MODULES), embed)
        out_path = HTML_DIR / f"{args.module}.html"
        out_path.write_text(html)
        print(f"Built: {out_path}")
        return

    # Build all modules
    print(f"Building {len(MODULES)} modules...")
    for i, mod in enumerate(MODULES):
        source_path = SOURCE_DIR / mod["file"]
        if not source_path.exists():
            print(f"  SKIP: {mod['file']} not found")
            continue

        prev_mod = MODULES[i - 1] if i > 0 else None
        next_mod = MODULES[i + 1] if i < len(MODULES) - 1 else None

        html = build_module_html(source_path, prev_mod, next_mod, i, len(MODULES), embed)
        out_path = HTML_DIR / mod["file"].replace(".md", ".html")
        out_path.write_text(html)
        print(f"  Built: {out_path.name}")

    # Build extras
    for ex in EXTRAS:
        source_path = SOURCE_DIR / ex["file"]
        if not source_path.exists():
            continue
        html = build_module_html(source_path, None, None, -1, len(MODULES), embed)
        out_path = HTML_DIR / ex["file"].replace(".md", ".html")
        out_path.write_text(html)
        print(f"  Built: {out_path.name}")

    # Build references
    for ref in REFERENCES:
        source_path = SOURCE_DIR / ref["file"]
        if not source_path.exists():
            continue
        html = build_module_html(source_path, None, None, -1, len(MODULES), embed)
        out_path = HTML_DIR / ref["file"].replace(".md", ".html")
        out_path.write_text(html)
        print(f"  Built: {out_path.name}")

    # Build index at project root
    index_html = build_index_html()
    index_path = PROJECT_ROOT / "index.html"
    index_path.write_text(index_html)
    print(f"  Built: index.html (project root)")

    print(f"\nDone. Open index.html to view the course.")


if __name__ == "__main__":
    main()
