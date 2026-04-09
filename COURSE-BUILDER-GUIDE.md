# Course Builder Guide

**How to transform a folder of Markdown files into a complete, self-contained course website using Claude Code.**

This guide documents the full pipeline used by the Agentic Engineering 101 course. Give this file to Claude Code alongside your Markdown source files and it will build you the same kind of course: illustrated, narrated, paginated, dark-mode-ready, and distributable as a single zip.

---

## Quick Start

Tell Claude Code:

> I have course content in Markdown files in `source/`. Use the Course Builder Guide at `COURSE-BUILDER-GUIDE.md` to transform them into a complete course website.

Claude will scaffold the project, generate images and narration, build the HTML, and package it for distribution.

---

## 1. Project Structure

Your project should end up looking like this:

```
your-course/
├── source/                      # Your markdown source files (you write these)
│   ├── module-00-intro.md
│   ├── module-01-basics.md
│   └── ...
├── scripts/                     # Build tools (Claude creates these)
│   ├── build_course.py          # Markdown → HTML converter
│   ├── deploy.py                # Packaging for distribution
│   ├── generate_narration.py    # ElevenLabs TTS integration
│   └── module_template.html     # HTML page template
├── images/                      # Generated illustrations
│   ├── module-00/
│   │   ├── image-name.png
│   │   └── image-name.json      # Generation metadata
│   └── ...
├── audio/                       # Generated narration audio
│   ├── module-00-intro/
│   │   ├── manifest.json        # Audio metadata & text
│   │   └── 01_module-00-intro.mp3
│   └── ...
├── html/                        # Generated individual module HTML files
├── dist/                        # Distribution packages (zip files)
├── index.html                   # Generated landing page
├── .env                         # API keys (never commit this)
└── COURSE-BUILDER-GUIDE.md      # This file
```

---

## 2. Writing Source Markdown

Each module is a single Markdown file in `source/`. Use these conventions:

### File naming

```
module-00-your-topic.md
module-01-next-topic.md
reference-glossary.md
crash-course-overview.md
```

### Required structure

```markdown
# Module 0: Your Title Here

## First Section

Your content here. Regular markdown: **bold**, *italic*, `code`, [links](url).

## Second Section

More content. Each H2 becomes a new "page" in the web view.

### Subsection

H3 headings appear in the sidebar TOC under their parent H2.
```

### Special markers (emoji-prefixed blockquotes)

These markers get converted into styled interactive components in the HTML output.

#### Narration blocks (converted to audio players)

```markdown
> 🎙️ This text will be spoken aloud by ElevenLabs TTS and displayed with a play button. Students can listen or read. Multi-line narrations continue on the next line of the same blockquote.
> This is still part of the same narration block.
```

#### Tier/difficulty badges

```markdown
> 🏷️ Start Here
```

Available tiers: `Start Here`, `Useful Soon`, `When You're Ready`, `Advanced`. Each gets a distinct color badge.

#### Teaching intent (what students should learn from this section)

```markdown
> 🎯 **Teach:** What students should understand after this section.
> **See:** What examples or illustrations they'll encounter.
> **Feel:** What emotional response or motivation they should have.
```

#### Cycle/context anchors (where content fits in a bigger picture)

```markdown
> 🔄 **Where this fits:** Explains how this section connects to the overall course framework or learning path.
```

#### Key takeaway callouts

```markdown
> 💡 **Remember this one thing:** The single most important point from this section that students must retain.
```

### Images

Reference images from your markdown like this:

```markdown
![Caption describing the image](../images/module-00/image-name.png)
*Caption displayed below the image*
```

Images are embedded as base64 in the final HTML so the course works completely offline.

---

## 3. Generating Illustrations

### What Claude Code can do

Claude Code can generate illustrations using Google's Gemini image generation API. Each image gets:
- A PNG file in `images/module-XX/`
- A JSON metadata file tracking the prompt, model, generation time, and token usage

### Setup

Add your Gemini API key to `.env`:

```
GEMINI_API_KEY=your-key-here
```

### How to ask Claude Code to generate images

Tell Claude:

> Generate illustrations for module-00. Use the Head First book illustration style -- clean lines, slightly whimsical, warm colors, educational. Aspect ratio 16:9, white background. Read the module content and create images that illustrate the key concepts.

Or for a specific image:

> Generate an illustration for module-03 showing a developer looking at a map vs. wandering lost. Head First style, 16:9 aspect ratio.

### Image generation parameters used by this project

| Parameter | Value |
|-----------|-------|
| Model | `nanobanana-pro` (resolves to `gemini-3-pro-image-preview`) |
| Quality mode | `final` |
| Style | Head First book illustration: clean lines, whimsical, warm colors, educational |
| Aspect ratio | 16:9 |
| Background | white |
| Text in image | minimal |
| Avoid | photorealistic, dark, scary |
| Cost estimate | ~$0.14 per image at final quality |

### Prompt structure

Each image prompt is assembled from:

```
Goal: "editorial illustration for a programming book"
Scene description: (your specific prompt)
Style: "Head First book illustration style, clean lines, slightly whimsical and humorous, warm colors, educational"
Aspect ratio: "16:9"
Background: "white"
Text in image: "minimal"
Negative constraints: "photorealistic, dark, scary"
```

---

## 4. Generating Narration Audio

### Setup

Add your ElevenLabs API key to `.env`:

```
ELEVENLABS_API_KEY=your-key-here
```

### How it works

The narration generator (`scripts/generate_narration.py`):

1. Scans markdown files for `🎙️` blockquotes
2. Cleans markdown formatting (strips bold, italic, links, code markers) for natural speech
3. Sends text to ElevenLabs API
4. Saves MP3 files and a `manifest.json` per module

### Commands

```bash
# Generate audio for all modules (skips existing files):
uv run --with elevenlabs python scripts/generate_narration.py

# Generate for a single module:
uv run --with elevenlabs python scripts/generate_narration.py source/module-03-your-topic.md

# Regenerate only changed narrations (compares text to manifest):
uv run --with elevenlabs python scripts/generate_narration.py --regenerate-changed

# Force regenerate ALL audio for a module:
uv run --with elevenlabs python scripts/generate_narration.py source/module-03-your-topic.md --force

# Include crash courses and references:
uv run --with elevenlabs python scripts/generate_narration.py --all

# Dry run (show what would be generated):
uv run --with elevenlabs python scripts/generate_narration.py --dry-run

# Use a different voice:
uv run --with elevenlabs python scripts/generate_narration.py --voice drew
```

### Available voices

| Name | ID | Notes |
|------|----|-------|
| rachel | 21m00Tcm4TlvDq8ikWAM | Default, female |
| drew | 29vD33N1CtxCmqQRPOHJ | Male |
| paul | 5Q0t7uMcjvnagumLfvZi | Male |
| sarah | EXAVITQu4vr4xnSDxMaL | Female |
| emily | LcfcDJNUP1GQjkzn1xUU | Female |
| charlie | IKne3meq5aSn9XLyUdCD | Male |
| george | JBFqnCBsd6RMkjVDRZzb | Male |
| matilda | XrExE9yKIg1WjnnlVkGX | Female |

### Audio specs

- Model: `eleven_multilingual_v2`
- Format: `mp3_44100_128` (44.1 kHz, 128 kbps)
- Storage: embedded as base64 in final HTML

---

## 5. Building the Course HTML

### What the build does

`scripts/build_course.py` transforms your source markdown into a fully interactive course:

1. **Markdown to HTML** using Python `markdown` library with extensions:
   - FencedCodeExtension (fenced code blocks with syntax highlighting)
   - CodeHiliteExtension (syntax highlighting via Pygments)
   - TableExtension (markdown tables)
   - TocExtension (auto-generated table of contents, depth 2-3)
   - md_in_html (markdown inside HTML blocks)

2. **Special block processing** (in this order):
   - `🏷️` → tier badges (color-coded by difficulty level)
   - `🔄` → cycle anchor blocks
   - `💡` → remember-one-thing callout boxes
   - `🎯` → teaching intent blocks
   - `🎙️` → narration audio players with embedded MP3

3. **Image embedding** → all `<img>` src paths replaced with base64 data URIs

4. **Pagination** → HTML split at H2 boundaries into navigable pages

5. **Template wrapping** → content inserted into `module_template.html` with:
   - Sidebar with table of contents
   - Light/dark theme toggle
   - Narration mute toggle
   - Page navigation (prev/next buttons, keyboard arrows)
   - Module-to-module navigation links
   - Mobile-responsive sidebar

6. **Index page generation** → landing page with module cards organized by tier

### Commands

```bash
# Build the full course:
uv run --with markdown --with pygments python scripts/build_course.py

# Build a single module (for testing):
uv run --with markdown --with pygments python scripts/build_course.py --module module-00-intro

# Build without embedding images (faster, links instead):
uv run --with markdown --with pygments python scripts/build_course.py --no-embed
```

### Module registry

The build script needs a list of modules with metadata. This is defined as a Python list in `build_course.py`:

```python
MODULES = [
    {
        "file": "module-00-intro.md",       # Source filename
        "short": "Module 0",                # Short label for nav
        "title": "Introduction",            # Full title for cards
        "hero": "module-00/hero-image.png", # Hero image for index card
        "tier": "Start Here",               # Difficulty tier
        "tier_css": "tier-start-here",      # CSS class for badge
    },
    # ... more modules
]

EXTRAS = [
    {"file": "crash-course.md", "short": "Crash Course", "title": "Quick Overview", "hero": "..."},
]

REFERENCES = [
    {"file": "reference-glossary.md", "short": "Reference", "title": "Glossary", "hero": "..."},
]
```

When adding new modules, update this registry.

---

## 6. HTML Features

The generated course website includes:

### Interactive features
- **Light/dark theme** toggle (persisted in localStorage)
- **Page pagination** at H2 boundaries with Previous/Next buttons
- **Keyboard navigation** (arrow keys for pages)
- **Sidebar TOC** with click-to-jump and active section highlighting
- **Narration audio players** with play/pause, auto-chain to next block
- **Auto-play narration** on page advance (respectable mute toggle)
- **Guided tour mode** (right/left arrows, space, Esc)
- **Module visit tracking** in localStorage

### Styling
- System font stack for fast rendering
- Responsive design (mobile sidebar toggle at 900px)
- Print-friendly stylesheet (hides nav, audio, sidebar)
- Syntax highlighting for code blocks via Pygments
- Styled callout blocks for each marker type
- Color-coded tier badges

### Self-contained
- ALL images embedded as base64 data URIs
- ALL audio embedded as base64 data URIs
- Single HTML file per module (no external dependencies)
- Works completely offline in any browser

---

## 7. Packaging for Distribution

`scripts/deploy.py` creates a versioned zip file for student distribution.

### Commands

```bash
# Build + package with auto-generated version (git hash + date):
uv run --with markdown --with pygments python scripts/deploy.py

# Build + package with explicit version:
uv run --with markdown --with pygments python scripts/deploy.py --version 1.0

# Package only (skip rebuild, use existing html/):
uv run --with markdown --with pygments python scripts/deploy.py --skip-build

# Custom output directory:
uv run --with markdown --with pygments python scripts/deploy.py --out ~/Desktop
```

### What gets packaged

```
your-course-v1.0/
├── index.html        # Self-contained landing page (all assets embedded)
├── html/             # Individual module pages
│   ├── module-00-intro.html
│   ├── module-01-basics.html
│   └── ...
└── VERSION           # Build metadata
```

### Student experience

1. Download zip
2. Unzip
3. Open `index.html` in any browser
4. Course runs entirely locally, no server needed

---

## 8. Full Workflow (End to End)

Here's the complete process for turning Markdown into a distributed course:

### Step 1: Write your content

Create Markdown files in `source/` using the conventions in Section 2. Use the special markers for narration, teaching intent, callouts, etc.

### Step 2: Generate illustrations

Ask Claude Code to generate images for each module. Review and regenerate any that don't look right.

```
Generate illustrations for all modules. Use Head First book style -- clean, whimsical, educational. 16:9 aspect ratio, white background.
```

### Step 3: Generate narration

```bash
uv run --with elevenlabs python scripts/generate_narration.py --all
```

Or ask Claude Code to run it for you.

### Step 4: Build the course

```bash
uv run --with markdown --with pygments python scripts/build_course.py
```

Open `index.html` to preview.

### Step 5: Package for distribution

```bash
uv run --with markdown --with pygments python scripts/deploy.py --version 1.0
```

The zip file in `dist/` is ready to send to students.

---

## 9. Adapting for a New Course

When starting a new course project, tell Claude Code:

> I have Markdown course files in `source/`. I want to set up a course builder following the COURSE-BUILDER-GUIDE.md pattern. Please:
> 1. Read my source files to understand the content
> 2. Create the `scripts/` directory with build_course.py, deploy.py, generate_narration.py, and module_template.html
> 3. Update the MODULES list in build_course.py to match my actual files
> 4. Set up .env with placeholder API keys
> 5. Generate illustrations for each module
> 6. Generate narration audio
> 7. Build the course and package it

### What to customize

| Item | Where | What to change |
|------|-------|----------------|
| Course name | `build_course.py`, `deploy.py` | Title in templates, zip folder name |
| Module list | `build_course.py` MODULES list | File paths, titles, tiers, hero images |
| Tier system | `build_course.py` + `module_template.html` | Tier names, colors, CSS classes |
| Landing page | `build_course.py` INDEX_TEMPLATE | Layout, sections, branding |
| Color scheme | `module_template.html` CSS variables | `--accent`, `--narration-bg`, etc. |
| Voice | `generate_narration.py` --voice flag | Any ElevenLabs voice |
| Image style | Image generation prompts | Style description, aspect ratio |
| localStorage keys | `module_template.html` JS | Prefix to avoid conflicts between courses |

### Dependencies

The build pipeline uses `uv` for dependency management with inline deps:

```bash
# Build (needs markdown + pygments):
uv run --with markdown --with pygments python scripts/build_course.py

# Narration (needs elevenlabs):
uv run --with elevenlabs python scripts/generate_narration.py

# Images (needs google-genai):
# Claude Code generates these directly via API calls
```

No `requirements.txt` or virtual environment setup needed -- `uv run --with` handles it.

---

## 10. Tips and Gotchas

- **File size**: Base64 encoding increases size ~33%. A course with many images and narrations can easily reach 100+ MB. This is fine -- the zip compresses it.
- **Narration text cleaning**: Bold, italic, links, and code markers are stripped before sending to ElevenLabs. Write narration text as natural speech.
- **Image paths**: In source markdown, use `../images/module-XX/name.png`. The build script resolves these relative to the `images/` directory.
- **Orphan cleanup**: The narration generator removes audio files for blocks that no longer exist in the source.
- **Incremental builds**: Both narration and image generation skip existing files by default. Use `--force` to regenerate everything.
- **Single-module builds**: Use `--module module-name` for faster iteration when editing one module.
- **Dark mode**: All styled components have dark mode variants. If you customize colors, add `[data-theme="dark"]` overrides.
- **H2 = page break**: Every H2 heading starts a new page in the web view. Plan your content structure accordingly.
- **TOC depth**: The table of contents shows H2 and H3 headings. Deeper headings are not included.
