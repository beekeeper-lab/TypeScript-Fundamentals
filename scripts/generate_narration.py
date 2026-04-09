#!/usr/bin/env python3
"""Generate narration audio from markdown narration markers using ElevenLabs TTS.

Usage:
    # Generate audio for all modules (skips existing files):
    uv run --with elevenlabs python scripts/generate_narration.py

    # Generate for a single module:
    uv run --with elevenlabs python scripts/generate_narration.py source/module-03-functions.md

    # Regenerate changed narrations (compares text to manifest):
    uv run --with elevenlabs python scripts/generate_narration.py --regenerate-changed

    # Force regenerate ALL audio for a module:
    uv run --with elevenlabs python scripts/generate_narration.py source/module-03-functions.md --force

    # Include all source files:
    uv run --with elevenlabs python scripts/generate_narration.py --all

    # Dry run (show what would be generated, no API calls):
    uv run --with elevenlabs python scripts/generate_narration.py --dry-run

    # Use a different voice:
    uv run --with elevenlabs python scripts/generate_narration.py --voice drew
"""

import json
import os
import re
import sys
from pathlib import Path

def find_narration_blocks(markdown_text: str) -> list[dict]:
    """Extract narration blocks marked with 🎙️ from markdown."""
    blocks = []
    pattern = re.compile(
        r'(?:^|\n)(?:> 🎙️ .+(?:\n> .+)*)',
        re.MULTILINE
    )
    for i, match in enumerate(pattern.finditer(markdown_text)):
        raw = match.group().strip()
        # Remove blockquote markers and emoji
        text = re.sub(r'^> ?', '', raw, flags=re.MULTILINE)
        text = text.replace('🎙️ ', '').replace('🎙️', '').strip()
        # Clean up markdown formatting for speech
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # italic
        text = re.sub(r'`(.+?)`', r'\1', text)  # inline code
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)  # links
        blocks.append({
            "index": i,
            "text": text,
            "position": match.start(),
        })
    return blocks


def generate_audio(text: str, output_path: Path, voice: str = "rachel") -> int:
    """Generate audio using ElevenLabs TTS. Returns file size in bytes."""
    try:
        from elevenlabs import ElevenLabs
    except ImportError:
        print("ERROR: elevenlabs package not installed. Run: pip install elevenlabs")
        sys.exit(1)

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        # Try .env file
        env_path = Path(__file__).parent.parent / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("ELEVENLABS_API_KEY="):
                    api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not api_key:
        print("ERROR: ELEVENLABS_API_KEY not set")
        sys.exit(1)

    # Voice name to ID mapping
    voice_map = {
        "rachel": "21m00Tcm4TlvDq8ikWAM",
        "drew": "29vD33N1CtxCmqQRPOHJ",
        "paul": "5Q0t7uMcjvnagumLfvZi",
        "sarah": "EXAVITQu4vr4xnSDxMaL",
        "emily": "LcfcDJNUP1GQjkzn1xUU",
        "charlie": "IKne3meq5aSn9XLyUdCD",
        "george": "JBFqnCBsd6RMkjVDRZzb",
        "matilda": "XrExE9yKIg1WjnnlVkGX",
    }

    voice_id = voice_map.get(voice, voice)
    client = ElevenLabs(api_key=api_key)

    audio_gen = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    audio_bytes = b"".join(audio_gen)
    output_path.write_bytes(audio_bytes)
    return len(audio_bytes)


def load_existing_manifest(module_audio_dir: Path) -> dict[int, dict]:
    """Load existing manifest and index by block number."""
    manifest_path = module_audio_dir / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        entries = json.loads(manifest_path.read_text())
        return {e["index"]: e for e in entries}
    except (json.JSONDecodeError, KeyError):
        return {}


def process_module(
    source_path: Path,
    audio_dir: Path,
    voice: str = "rachel",
    dry_run: bool = False,
    force: bool = False,
    regenerate_changed: bool = False,
):
    """Process a single markdown module file."""
    module_name = source_path.stem
    text = source_path.read_text()
    blocks = find_narration_blocks(text)

    if not blocks:
        print(f"  {module_name}: no narration blocks found, skipping")
        return []

    module_audio_dir = audio_dir / module_name
    existing = load_existing_manifest(module_audio_dir)
    manifest = []
    generated = 0
    skipped = 0
    changed = 0

    for block in blocks:
        idx = block["index"] + 1
        audio_filename = f"{idx:02d}_{module_name}.mp3"
        audio_path = module_audio_dir / audio_filename

        entry = {
            "index": idx,
            "module": module_name,
            "audio_file": audio_filename,
            "text": block["text"],
        }

        needs_generation = False
        reason = ""

        if force:
            needs_generation = True
            reason = "forced"
        elif not audio_path.exists():
            needs_generation = True
            reason = "new"
        elif regenerate_changed and idx in existing:
            old_text = existing[idx].get("text", "")
            if old_text.strip() != block["text"].strip():
                needs_generation = True
                reason = "text changed"
                changed += 1

        if dry_run:
            status = f"WOULD GENERATE ({reason})" if needs_generation else "exists, skip"
            print(f"  [{module_name}] Block {idx}: {status}")
            print(f"    {block['text'][:80]}...")
            entry["size_bytes"] = audio_path.stat().st_size if audio_path.exists() else 0
        elif needs_generation:
            print(f"  [{module_name}] Block {idx}: generating ({reason})...")
            size = generate_audio(block["text"], audio_path, voice)
            entry["size_bytes"] = size
            generated += 1
            print(f"    → {audio_filename} ({size:,} bytes)")
        else:
            entry["size_bytes"] = audio_path.stat().st_size if audio_path.exists() else 0
            skipped += 1

        manifest.append(entry)

    # Remove orphaned audio files
    expected_files = {e["audio_file"] for e in manifest}
    if not dry_run and module_audio_dir.exists():
        for mp3 in module_audio_dir.glob("*.mp3"):
            if mp3.name not in expected_files:
                print(f"  [{module_name}] Removing orphan: {mp3.name}")
                mp3.unlink()

    # Write manifest
    manifest_path = module_audio_dir / "manifest.json"
    if not dry_run:
        module_audio_dir.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest, indent=2))

    summary = f"{module_name}: {len(blocks)} blocks"
    if generated:
        summary += f", {generated} generated"
    if changed:
        summary += f" ({changed} changed)"
    if skipped:
        summary += f", {skipped} skipped"
    print(f"  {summary}")
    return manifest


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Generate narration audio from markdown using ElevenLabs TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("source", nargs="?", help="Single source file (e.g. source/module-03-functions.md)")
    parser.add_argument("--voice", default="rachel", help="ElevenLabs voice name or ID (default: rachel)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated without making API calls")
    parser.add_argument("--force", action="store_true", help="Regenerate ALL audio, even if files already exist")
    parser.add_argument("--regenerate-changed", action="store_true",
                        help="Regenerate audio only for narrations whose text changed since last generation")
    parser.add_argument("--all", action="store_true",
                        help="Process all source files (not just modules)")
    parser.add_argument("--audio-dir", default=None, help="Audio output directory (default: audio/)")
    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    source_dir = project_root / "source"
    audio_dir = Path(args.audio_dir) if args.audio_dir else project_root / "audio"

    if args.source:
        source_path = Path(args.source)
        if not source_path.exists():
            source_path = source_dir / args.source
        if source_path.is_file():
            files = [source_path]
        else:
            files = sorted(source_path.glob("*.md"))
    elif args.all:
        files = sorted(source_dir.glob("*.md"))
    else:
        files = sorted(source_dir.glob("module-*.md"))

    print(f"Processing {len(files)} file(s)...")
    print(f"Audio output: {audio_dir}")
    print(f"Voice: {args.voice}")
    if args.force:
        print("FORCE MODE - all audio will be regenerated")
    if args.regenerate_changed:
        print("REGENERATE CHANGED - only narrations with edited text will be regenerated")
    if args.dry_run:
        print("DRY RUN - no audio will be generated")
    print()

    total_blocks = 0
    for f in files:
        manifest = process_module(
            f, audio_dir, args.voice, args.dry_run, args.force, args.regenerate_changed,
        )
        total_blocks += len(manifest)

    print(f"\nTotal: {total_blocks} narration blocks across {len(files)} files")
    if args.dry_run and args.regenerate_changed:
        print("Run without --dry-run to generate the audio.")


if __name__ == "__main__":
    main()
