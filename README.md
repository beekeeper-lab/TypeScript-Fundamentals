# TypeScript Fundamentals

A structured, self-paced course in TypeScript for developers. 20 modules covering everything from basic types to a complete capstone project.

## Course Structure

### Foundations (Start Here)
| Module | Topic | Key Concepts |
|--------|-------|-------------|
| 0 | What Is TypeScript | TypeScript vs JavaScript, tsc compiler, type checking |
| 1 | Variables and Types | let/const, primitives, type inference, any vs unknown |
| 2 | Arrays, Tuples, Objects | Typed arrays, tuples, object types, destructuring |
| 3 | Functions | Type signatures, optional/default/rest params, arrow functions |
| 4 | Control Flow | if/else, loops, map/filter/reduce, type narrowing in conditionals |

### Intermediate (Useful Soon)
| Module | Topic | Key Concepts |
|--------|-------|-------------|
| 5 | Type Aliases and Unions | Union types, discriminated unions, intersection types |
| 6 | Interfaces | Extending, method signatures, interface vs type |
| 7 | Classes | Access modifiers, inheritance, abstract classes |
| 8 | Generics | Generic functions, classes, constraints, keyof |
| 9 | Enums and Utility Types | String/numeric enums, Partial, Pick, Omit, Record |

### Applied (When You're Ready)
| Module | Topic | Key Concepts |
|--------|-------|-------------|
| 10 | Type Narrowing | typeof, instanceof, in, custom type guards, assertNever |
| 11 | Modules and Imports | ES modules, barrel files, multi-file projects |
| 12 | Async/Await | Promises, Promise.all/race/allSettled, retry patterns |
| 13 | Error Handling | Custom errors, Result type pattern, async error handling |
| 14 | JSON and APIs | Type guards for external data, schema validators, typed fetch |

### Advanced
| Module | Topic | Key Concepts |
|--------|-------|-------------|
| 15 | npm and Packages | npm init, scripts, semantic versioning, npx |
| 16 | tsconfig | Compiler options, strict mode, declarations, source maps |
| 17 | Testing with Vitest | describe/it/expect, mocking, async tests, coverage |
| 18 | Advanced Patterns | Decorators, builder/singleton, mapped/conditional/template literal types |
| 19 | Capstone Project | Task Tracker CLI tying all modules together |

## Building the Course

### Prerequisites

- Python 3.10+ with [uv](https://docs.astral.sh/uv/)
- API keys in `.env` (for images and narration)

### Build Commands

```bash
# Build the full course website:
uv run --with markdown --with pygments python scripts/build_course.py

# Build a single module (for testing):
uv run --with markdown --with pygments python scripts/build_course.py --module module-00-what-is-typescript

# Generate narration audio:
uv run --with elevenlabs python scripts/generate_narration.py

# Package for distribution:
uv run --with markdown --with pygments python scripts/deploy.py --version 1.0
```

### Viewing

After building, open `index.html` in any browser. The course runs entirely locally with no server needed.

## Project Structure

```
TypeScript_Fundamentals/
├── source/                 # Markdown source files (20 modules)
├── scripts/                # Build tools
│   ├── build_course.py     # Markdown → HTML converter
│   ├── deploy.py           # Packaging for distribution
│   ├── generate_narration.py  # ElevenLabs TTS integration
│   └── module_template.html   # HTML page template
├── images/                 # Generated illustrations
├── audio/                  # Generated narration audio
├── html/                   # Generated HTML modules
├── dist/                   # Distribution packages
├── index.html              # Generated landing page
├── .env                    # API keys
├── COURSE-BUILDER-GUIDE.md # Build system documentation
└── README.md               # This file
```
