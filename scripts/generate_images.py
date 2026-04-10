#!/usr/bin/env python3
"""Generate all course illustrations from IMAGE-PLAN.md using Google Gemini.

Usage:
    uv run --with google-genai --with Pillow python scripts/generate_images.py
    uv run --with google-genai --with Pillow python scripts/generate_images.py --dry-run
    uv run --with google-genai --with Pillow python scripts/generate_images.py --module 0
"""

import argparse
import json
import os
import re
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
IMAGE_PLAN = PROJECT_ROOT / "IMAGE-PLAN.md"
IMAGES_DIR = PROJECT_ROOT / "images"
COST_LOG = IMAGES_DIR / "cost-log.md"

# Approximate cost per image at "final" quality
COST_PER_IMAGE = 0.04


def load_api_key() -> str:
    env_path = PROJECT_ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            if line.startswith("GEMINI_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not found in .env or environment")
    return key


def parse_image_plan() -> list[dict]:
    """Parse IMAGE-PLAN.md into a list of image entries."""
    text = IMAGE_PLAN.read_text()
    entries = []

    # Split by ### Image headers
    image_blocks = re.split(r'^### Image \d+:', text, flags=re.MULTILINE)

    current_module = "unknown"
    for block in image_blocks:
        # Track current module
        module_match = re.search(r'^## Module (\d+):', block, re.MULTILINE)
        if module_match:
            current_module = module_match.group(1)

        # Extract file path
        file_match = re.search(r'\*\*File\*\*:\s*`([^`]+)`', block)
        if not file_match:
            continue

        file_path = file_match.group(1)

        # Extract status
        status_match = re.search(r'\*\*Status\*\*:\s*(.+)', block)
        status = status_match.group(1).strip() if status_match else "Not generated"

        # Extract the prompt section
        prompt_match = re.search(r'\*\*Prompt\*\*:\s*\n((?:\s+.+\n?)+)', block)
        if not prompt_match:
            continue

        prompt_text = prompt_match.group(1)

        # Extract name from the header line
        name_match = re.search(r'^(.+?)$', block.strip().split('\n')[0])
        name = name_match.group(1).strip() if name_match else "Unknown"

        # Extract module number from file path
        mod_match = re.search(r'module-(\d+)', file_path)
        module_num = int(mod_match.group(1)) if mod_match else -1

        # Build the full prompt string from structured fields
        prompt_lines = prompt_text.strip().split('\n')
        scene = ""
        full_prompt_parts = []
        for line in prompt_lines:
            line = line.strip()
            if line.startswith("Scene:"):
                scene = line[6:].strip()
            elif line.startswith("Goal:"):
                full_prompt_parts.append(line)
            elif line.startswith("Style:"):
                full_prompt_parts.append(line)
            elif line.startswith("Aspect ratio:"):
                full_prompt_parts.append(line)
            elif line.startswith("Background:"):
                full_prompt_parts.append(line)
            elif line.startswith("Text in image:"):
                full_prompt_parts.append(line)
            elif line.startswith("Avoid:"):
                full_prompt_parts.append(line)

        full_prompt = f"{scene}\n" + "\n".join(full_prompt_parts)

        entries.append({
            "name": name,
            "file_path": file_path,
            "module_num": module_num,
            "prompt": full_prompt,
            "status": status,
        })

    return entries


def generate_image(client, prompt: str, output_path: Path) -> dict:
    """Generate an image using Gemini and save it. Returns metadata."""
    from google.genai import types

    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = client.models.generate_content(
        model="nano-banana-pro-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    # Extract image from response
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            output_path.write_bytes(image_data)
            return {
                "size_bytes": len(image_data),
                "model": "nano-banana-pro-preview",
            }

    raise RuntimeError("No image data in Gemini response")


def update_plan_status(file_path: str, new_status: str):
    """Update the status of an image in IMAGE-PLAN.md."""
    text = IMAGE_PLAN.read_text()
    lines = text.split('\n')
    # Find the line with this file path, then find the next Status line
    found_file = False
    for i, line in enumerate(lines):
        if f'`{file_path}`' in line:
            found_file = True
        elif found_file and '**Status**:' in line:
            lines[i] = f'- **Status**: {new_status}'
            break
    IMAGE_PLAN.write_text('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description="Generate course illustrations from IMAGE-PLAN.md")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    parser.add_argument("--module", type=int, help="Only generate for a specific module number")
    parser.add_argument("--force", action="store_true", help="Regenerate even if file exists")
    args = parser.parse_args()

    entries = parse_image_plan()
    print(f"Found {len(entries)} images in IMAGE-PLAN.md")

    if args.module is not None:
        entries = [e for e in entries if e["module_num"] == args.module]
        print(f"Filtered to {len(entries)} images for module {args.module}")

    # Filter out already-generated unless --force
    if not args.force:
        to_generate = []
        for e in entries:
            out_path = IMAGES_DIR.parent / e["file_path"]
            if out_path.exists() and "Generated" in e["status"]:
                print(f"  SKIP (exists): {e['file_path']}")
            else:
                to_generate.append(e)
        entries = to_generate

    print(f"Will generate {len(entries)} images")
    estimated_cost = len(entries) * COST_PER_IMAGE
    print(f"Estimated cost: ${estimated_cost:.2f}")

    if args.dry_run:
        for e in entries:
            print(f"  WOULD GENERATE: {e['file_path']}")
            print(f"    Prompt: {e['prompt'][:100]}...")
        print(f"\nDry run complete. {len(entries)} images, ~${estimated_cost:.2f}")
        return

    if not entries:
        print("Nothing to generate.")
        return

    api_key = load_api_key()
    from google import genai
    client = genai.Client(api_key=api_key)

    generated = 0
    failed = 0
    total_bytes = 0
    results = []

    for i, entry in enumerate(entries):
        out_path = IMAGES_DIR.parent / entry["file_path"]
        print(f"\n[{i+1}/{len(entries)}] Generating: {entry['file_path']}")
        print(f"  Name: {entry['name']}")

        try:
            meta = generate_image(client, entry["prompt"], out_path)
            generated += 1
            total_bytes += meta["size_bytes"]
            size_kb = meta["size_bytes"] / 1024
            print(f"  OK: {size_kb:.0f} KB")

            # Update status in plan
            update_plan_status(entry["file_path"], f"Generated ({size_kb:.0f} KB)")
            results.append({"file": entry["file_path"], "size_kb": size_kb, "status": "ok"})

            # Rate limit: Gemini has limits, be conservative
            if i < len(entries) - 1:
                time.sleep(5)

        except Exception as ex:
            failed += 1
            print(f"  FAILED: {ex}")
            update_plan_status(entry["file_path"], f"Failed: {ex}")
            results.append({"file": entry["file_path"], "size_kb": 0, "status": f"failed: {ex}"})
            time.sleep(2)

    # Summary
    actual_cost = generated * COST_PER_IMAGE
    total_mb = total_bytes / (1024 * 1024)

    print(f"\n{'='*60}")
    print(f"Generation complete!")
    print(f"  Generated: {generated}")
    print(f"  Failed: {failed}")
    print(f"  Total size: {total_mb:.1f} MB")
    print(f"  Estimated cost: ${actual_cost:.2f}")
    print(f"{'='*60}")

    # Write cost log
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    cost_lines = [
        f"# Image Generation Cost Log\n\n",
        f"Total images generated: {generated}\n",
        f"Total images failed: {failed}\n",
        f"Total size: {total_mb:.1f} MB\n",
        f"Estimated cost: ${actual_cost:.2f} ({generated} images x ${COST_PER_IMAGE}/image)\n\n",
        f"## Details\n\n",
        f"| File | Size | Status |\n",
        f"|------|------|--------|\n",
    ]
    for r in results:
        cost_lines.append(f"| `{r['file']}` | {r['size_kb']:.0f} KB | {r['status']} |\n")

    COST_LOG.write_text("".join(cost_lines))
    print(f"Cost log written to: {COST_LOG}")

    # Update total in IMAGE-PLAN.md
    plan_text = IMAGE_PLAN.read_text()
    # Append or update cost summary at end
    cost_marker = "\n---\n\n## Cost Summary\n"
    if cost_marker in plan_text:
        plan_text = plan_text[:plan_text.index(cost_marker)]
    plan_text += (
        f"{cost_marker}"
        f"- Total images generated: {generated}\n"
        f"- Total images failed: {failed}\n"
        f"- Total size: {total_mb:.1f} MB\n"
        f"- Estimated cost: **${actual_cost:.2f}** ({generated} images x ${COST_PER_IMAGE}/image)\n"
    )
    IMAGE_PLAN.write_text(plan_text)


if __name__ == "__main__":
    main()
