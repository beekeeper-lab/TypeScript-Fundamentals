#!/usr/bin/env python3
"""Generate course illustrations using Google Gemini image generation API.

Reads IMAGE-PLAN.md and generates each planned image. Skips images that
already exist unless --force is used.

API key lookup order:
  1. GEMINI_API_KEY environment variable
  2. <course>/.env file
  3. <course>/../.env file (parent Course_Material/.env)

Usage:
    uv run --with google-genai python scripts/generate_images.py
    uv run --with google-genai python scripts/generate_images.py --dry-run
    uv run --with google-genai python scripts/generate_images.py --force
    uv run --with google-genai python scripts/generate_images.py --filter module-01
"""

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images"
IMAGE_PLAN = ROOT / "IMAGE-PLAN.md"

MODEL = "gemini-3-pro-image-preview"

# API quota is 20 requests/minute/model. Target ~18/min for headroom.
MIN_INTERVAL_SECONDS = 60.0 / 18
MAX_RETRIES_ON_429 = 3


def load_api_key():
    """Find GEMINI_API_KEY via env var, course .env, or parent .env."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key.strip()

    for candidate in (ROOT / ".env", ROOT.parent / ".env"):
        if candidate.exists():
            for line in candidate.read_text().splitlines():
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    print("ERROR: GEMINI_API_KEY not found in environment or any .env file")
    print(f"  Checked: $GEMINI_API_KEY, {ROOT}/.env, {ROOT.parent}/.env")
    sys.exit(1)


def parse_frontmatter(text):
    """Extract plan-level defaults from top-of-file **Key:** value lines."""
    defaults = {}
    keys = {
        "style": r"^\*\*Style:\*\*\s*(.+)$",
        "branding": r"^\*\*Branding:\*\*\s*(.+)$",
        "aspect_ratio": r"^\*\*Aspect ratio:\*\*\s*(.+)$",
        "background": r"^\*\*Background:\*\*\s*(.+)$",
        "text_in_image": r"^\*\*Text in image:\*\*\s*(.+)$",
        "avoid": r"^\*\*Avoid:\*\*\s*(.+)$",
        "philosophy": r"^\*\*Philosophy:\*\*\s*(.+)$",
    }

    # Only look at the top of the file, before the first ## heading
    head = text.split("\n## ", 1)[0]
    for key, pattern in keys.items():
        m = re.search(pattern, head, re.MULTILINE)
        if m:
            defaults[key] = m.group(1).strip()

    return defaults


def parse_image_plan():
    """Parse IMAGE-PLAN.md into a list of image entries.

    Each entry has: short_name, module_title, file, page, description,
    and either prompt_parts (structured) or uses frontmatter defaults.
    """
    text = IMAGE_PLAN.read_text()
    defaults = parse_frontmatter(text)

    images = []
    current_module = ""
    lines = text.split("\n")

    i = 0
    while i < len(lines):
        line = lines[i]

        mod_match = re.match(r"^##\s+(?:Module|Week)\s+.+", line)
        if mod_match:
            current_module = line.lstrip("#").strip()

        img_match = re.match(r"^###\s+Image\s+\d+:\s*(.+)", line)
        if img_match:
            entry = {
                "short_name": img_match.group(1).strip(),
                "module_title": current_module,
                "file": "",
                "page": "",
                "description": "",
                "prompt_parts": {},
                "defaults": defaults,
            }

            j = i + 1
            in_prompt = False
            prompt_lines = []
            while j < len(lines):
                l = lines[j]
                if re.match(r"^###\s+Image\s+\d+:", l) or re.match(r"^##\s+", l):
                    break

                if in_prompt:
                    if re.match(r"^- \*\*", l) or re.match(r"^###\s+", l) or re.match(r"^##\s+", l) or l.strip() == "---":
                        in_prompt = False
                    else:
                        prompt_lines.append(l.strip())
                        j += 1
                        continue

                file_match = re.match(r"- \*\*File\*\*:\s*`?(.+?)`?$", l)
                if file_match:
                    entry["file"] = file_match.group(1).strip("`")

                page_match = re.match(r"- \*\*Page\*\*:\s*(.+)", l)
                if page_match:
                    entry["page"] = page_match.group(1).strip()

                desc_match = re.match(r"- \*\*Description\*\*:\s*(.+)", l)
                if desc_match:
                    entry["description"] = desc_match.group(1).strip()

                if l.strip() == "- **Prompt**:":
                    in_prompt = True

                j += 1

            prompt_text = "\n".join(prompt_lines)
            for key in ["Goal", "Scene", "Style", "Aspect ratio", "Background", "Text in image", "Avoid"]:
                m = re.search(
                    rf"{key}:\s*(.+?)(?:\n\s*(?:Goal|Scene|Style|Aspect ratio|Background|Text in image|Avoid):|$)",
                    prompt_text, re.DOTALL,
                )
                if m:
                    entry["prompt_parts"][key.lower().replace(" ", "_")] = m.group(1).strip()

            if entry["file"]:
                images.append(entry)

        i += 1

    return images


def assemble_prompt(entry):
    """Build a full prompt from structured parts, or Description + defaults."""
    parts = entry["prompt_parts"]
    defaults = entry["defaults"]

    if parts:
        sections = []
        for key in ["goal", "scene", "style", "aspect_ratio", "background", "text_in_image", "avoid"]:
            if key in parts:
                label = key.replace("_", " ").capitalize().replace("Aspect ratio", "Aspect ratio").replace("Text in image", "Text in image")
                sections.append(f"{label}: {parts[key]}")
        return "\n".join(sections)

    if not entry["description"]:
        return ""

    sections = [f"Scene: {entry['description']}"]
    if "style" in defaults:
        sections.append(f"Style: {defaults['style']}")
    if "branding" in defaults:
        sections.append(f"Branding: {defaults['branding']}")
    if "aspect_ratio" in defaults:
        sections.append(f"Aspect ratio: {defaults['aspect_ratio']}")
    if "background" in defaults:
        sections.append(f"Background: {defaults['background']}")
    if "text_in_image" in defaults:
        sections.append(f"Text in image: {defaults['text_in_image']}")
    if "avoid" in defaults:
        sections.append(f"Avoid: {defaults['avoid']}")
    return "\n".join(sections)


def _extract_retry_delay(err_str):
    """Pull retryDelay seconds from a 429 error message, fallback to 30s."""
    m = re.search(r"retryDelay['\"]?:\s*['\"]?(\d+)s", err_str)
    return int(m.group(1)) + 2 if m else 30


def generate_image(prompt, output_path, api_key):
    """Generate an image via Gemini with retry-on-429. Returns metadata dict."""
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    start_time = time.time()

    for attempt in range(MAX_RETRIES_ON_429 + 1):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE", "TEXT"],
                ),
            )
            break
        except Exception as e:
            err = str(e)
            if "429" in err and "RESOURCE_EXHAUSTED" in err and attempt < MAX_RETRIES_ON_429:
                wait_s = _extract_retry_delay(err)
                print(f" (429, retry in {wait_s}s)", end="", flush=True)
                time.sleep(wait_s)
                continue
            raise

    elapsed_ms = int((time.time() - start_time) * 1000)

    if not response.candidates or not response.candidates[0].content.parts:
        raise ValueError("No image in response")

    image_data = None
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("image/"):
            image_data = part.inline_data.data
            break

    if not image_data:
        raise ValueError("No image data found in response parts")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(image_data)

    usage = {}
    if hasattr(response, "usage_metadata") and response.usage_metadata:
        um = response.usage_metadata
        usage = {
            "prompt_tokens": getattr(um, "prompt_token_count", 0),
            "candidates_tokens": getattr(um, "candidates_token_count", 0),
            "total_tokens": getattr(um, "total_token_count", 0),
        }

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": MODEL,
        "prompt": prompt,
        "output_file": output_path.name,
        "generation_time_ms": elapsed_ms,
        "usage": usage,
    }


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Generate course illustrations")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--force", action="store_true", help="Regenerate existing images")
    parser.add_argument("--filter", help="Only generate images whose file path contains this string")
    args = parser.parse_args()

    api_key = load_api_key()
    images = parse_image_plan()

    if args.filter:
        images = [img for img in images if args.filter in img["file"]]

    print(f"Image Generator — {len(images)} images planned")
    print(f"Model: {MODEL}")
    print("=" * 60)

    total_tokens = 0
    total_time_ms = 0
    generated = 0
    skipped = 0
    errors = 0
    last_call_time = 0.0

    for idx, img in enumerate(images):
        rel = img["file"]
        if rel.startswith("images/"):
            rel = rel[len("images/"):]
        file_path = IMAGES_DIR / rel
        short = f"[{idx+1}/{len(images)}] {img['short_name']}"

        if file_path.exists() and not args.force:
            print(f"  {short} — exists, skipping")
            skipped += 1
            continue

        prompt = assemble_prompt(img)
        if not prompt:
            print(f"  {short} — no prompt (no Description and no structured Prompt block), skipping")
            skipped += 1
            continue

        if args.dry_run:
            print(f"  {short} — WOULD GENERATE → {img['file']}")
            continue

        elapsed = time.time() - last_call_time
        if elapsed < MIN_INTERVAL_SECONDS:
            time.sleep(MIN_INTERVAL_SECONDS - elapsed)

        print(f"  {short} — generating...", end="", flush=True)
        last_call_time = time.time()

        try:
            meta = generate_image(prompt, file_path, api_key)

            json_path = file_path.with_suffix(".json")
            json_path.write_text(json.dumps(meta, indent=2))

            tokens = meta.get("usage", {}).get("total_tokens", 0)
            elapsed = meta.get("generation_time_ms", 0)
            total_tokens += tokens
            total_time_ms += elapsed
            generated += 1

            size_kb = file_path.stat().st_size / 1024
            print(f" OK {size_kb:.0f} KB, {tokens} tokens, {elapsed/1000:.1f}s")

        except Exception as e:
            errors += 1
            print(f" ERROR: {e}")

    print("=" * 60)
    print(f"Generated: {generated}, Skipped: {skipped}, Errors: {errors}")
    if generated > 0:
        est_cost = total_tokens * 0.00007
        print(f"Total tokens: {total_tokens:,}")
        print(f"Total time: {total_time_ms/1000:.1f}s ({total_time_ms/1000/generated:.1f}s avg)")
        print(f"Estimated cost: ${est_cost:.2f}")

    return {
        "generated": generated,
        "skipped": skipped,
        "errors": errors,
        "total_tokens": total_tokens,
        "total_time_ms": total_time_ms,
    }


if __name__ == "__main__":
    main()
