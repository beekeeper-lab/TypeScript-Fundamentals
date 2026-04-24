# TypeScript Fundamentals

A 20-module TypeScript course covering typed JavaScript for web and application development.

## Course Details

- **20 modules** of content (no Day folders — content is organized as source modules only)
- **20 source files** in `source/`
- **20 quizzes** in `Quiz/`

## Build Pipeline

See `COURSE-BUILDER-GUIDE.md` for the full build pipeline documentation.

```bash
uv run --with markdown --with pygments python scripts/build_course.py
uv run --with elevenlabs python scripts/generate_narration.py
uv run --with markdown --with pygments python scripts/deploy.py --version 1.0
```

## Quizzes

20 quizzes in `Quiz/Day_01_Quiz_File/` through `Quiz/Day_20_Quiz_File/`. Run from the parent directory:

```bash
python ../quiz_app.py TypeScript_Fundamentals <day>
```

Results tracked in `Gradebook.md`.

## Note

This course does not have Day content folders with assignments — only source modules, quizzes, and the standard build pipeline outputs (html, images, audio, dist).
