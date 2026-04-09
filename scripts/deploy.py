#!/usr/bin/env python3
"""Build and package the TypeScript Fundamentals course for student distribution.

Usage:
    # Build + package with auto-generated version (git short hash + date):
    uv run --with markdown --with pygments python scripts/deploy.py

    # Build + package with explicit version tag:
    uv run --with markdown --with pygments python scripts/deploy.py --version 1.0

    # Package only (skip rebuild, use existing html/):
    uv run --with markdown --with pygments python scripts/deploy.py --skip-build

    # Custom output directory:
    uv run --with markdown --with pygments python scripts/deploy.py --out ~/Desktop

Output:
    dist/typescript-fundamentals-v{VERSION}.zip
    A self-contained zip that students unpack and open index.html in a browser.
"""

import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
HTML_DIR = PROJECT_ROOT / "html"
DIST_DIR = PROJECT_ROOT / "dist"


def get_version_auto() -> str:
    """Generate a version string from git short hash + date."""
    try:
        short_hash = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=PROJECT_ROOT, text=True,
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        short_hash = "unknown"

    date_stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"{date_stamp}-{short_hash}"


def build_course() -> bool:
    """Run the course build script. Returns True on success."""
    build_script = PROJECT_ROOT / "scripts" / "build_course.py"
    print("=" * 60)
    print("Step 1: Building course from source")
    print("=" * 60)
    result = subprocess.run(
        [sys.executable, str(build_script)],
        cwd=PROJECT_ROOT,
    )
    return result.returncode == 0


def package_course(version: str, out_dir: Path) -> Path:
    """Package index.html + html/ into a versioned zip. Returns zip path."""
    print()
    print("=" * 60)
    print(f"Step 2: Packaging v{version}")
    print("=" * 60)

    out_dir.mkdir(parents=True, exist_ok=True)

    folder_name = f"typescript-fundamentals-v{version}"
    zip_stem = out_dir / folder_name

    staging = out_dir / f".staging-{folder_name}"
    if staging.exists():
        shutil.rmtree(staging)

    staging_inner = staging / folder_name
    staging_inner.mkdir(parents=True)

    # Copy index.html
    index_src = PROJECT_ROOT / "index.html"
    if not index_src.exists():
        print(f"  ERROR: {index_src} not found. Run build first.")
        sys.exit(1)
    shutil.copy2(index_src, staging_inner / "index.html")
    print(f"  Copied: index.html")

    # Copy html/ directory
    if not HTML_DIR.exists():
        print(f"  ERROR: {HTML_DIR} not found. Run build first.")
        sys.exit(1)
    shutil.copytree(HTML_DIR, staging_inner / "html")
    html_count = len(list((staging_inner / "html").glob("*.html")))
    print(f"  Copied: html/ ({html_count} files)")

    # Write a VERSION file inside the package
    version_file = staging_inner / "VERSION"
    version_file.write_text(
        f"TypeScript Fundamentals\n"
        f"Version: {version}\n"
        f"Built: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n"
    )
    print(f"  Created: VERSION")

    # Create zip
    zip_path = shutil.make_archive(
        str(zip_stem),
        "zip",
        root_dir=str(staging),
        base_dir=folder_name,
    )
    zip_path = Path(zip_path)

    # Clean up staging
    shutil.rmtree(staging)

    # Report
    size_mb = zip_path.stat().st_size / (1024 * 1024)
    print()
    print("=" * 60)
    print(f"Done! Package ready:")
    print(f"  {zip_path}")
    print(f"  Size: {size_mb:.1f} MB")
    print(f"  Contents: index.html + {html_count} module pages")
    print()
    print("Student instructions:")
    print(f"  1. Unzip {zip_path.name}")
    print(f"  2. Open {folder_name}/index.html in a browser")
    print("=" * 60)

    return zip_path


def main():
    parser = argparse.ArgumentParser(
        description="Build and package the course for student distribution.",
    )
    parser.add_argument(
        "--version", "-v",
        help="Version tag (default: auto-generated from git hash + date)",
    )
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="Skip the build step; package existing html/ directly",
    )
    parser.add_argument(
        "--out", "-o",
        type=Path,
        default=DIST_DIR,
        help=f"Output directory for the zip (default: {DIST_DIR})",
    )
    args = parser.parse_args()

    version = args.version or get_version_auto()

    if not args.skip_build:
        if not build_course():
            print("\nBuild failed. Fix errors above and retry.")
            sys.exit(1)
    else:
        print("Skipping build (--skip-build)")

    package_course(version, args.out)


if __name__ == "__main__":
    main()
