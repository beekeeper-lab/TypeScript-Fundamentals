# Module 0: What Is TypeScript

> 🏷️ Start Here

> 🎯 **Teach:** Why static typing catches bugs that dynamic typing misses. **See:** TypeScript compile errors catching real mistakes before code runs. **Feel:** Confidence that there is a safety net between writing code and running it.

> 🔄 **Where this fits:** This is the very first step. Before you write TypeScript, you need to understand what it is, why it exists, and how to set up your environment. Everything in this course builds on this foundation.

## Why TypeScript?

> 🎯 **Teach:** Why JavaScript's dynamic typing leads to runtime bugs and how TypeScript's static type checking eliminates them before code runs. **See:** A side-by-side comparison of the same function in JavaScript (silent bug) and TypeScript (compile-time error). **Feel:** Motivated to adopt TypeScript as a safety net that catches mistakes early.

### The Problem TypeScript Solves

> 🎙️ JavaScript is the language of the web, but it has a well-known weakness: it lets you make mistakes that you won't discover until your code is running in front of users. TypeScript was created to fix that. It adds a layer of static type checking on top of JavaScript, so the compiler can catch entire categories of bugs before your code ever runs. Every valid JavaScript file is already valid TypeScript — TypeScript just adds optional type annotations that the compiler uses to verify your code is correct.

```typescript
// JavaScript — error at runtime
function add(a, b) { return a + b; }
add("hello", 5); // "hello5" — silent bug

// TypeScript — error at compile time
function add(a: number, b: number): number { return a + b; }
add("hello", 5); // ❌ Compile error: string is not assignable to number
```

### How It Works

> 🎙️ TypeScript is never executed directly. Instead, the TypeScript compiler (tsc) reads your .ts files, checks them for type errors, and then strips away all the type annotations to produce plain JavaScript. That JavaScript is what actually runs in Node.js or the browser. Think of it as a spell-checker for your code — it runs before you "publish," catches problems, and the final output is clean JavaScript.

```
TypeScript (.ts) → tsc compiler → JavaScript (.js) → Node.js / Browser
```

![TypeScript compilation flow — .ts file enters the tsc compiler, type errors are caught, and clean .js is emitted](../images/module-00/compilation-flow.png)
*TypeScript compilation flow — .ts file enters the tsc compiler, type errors are caught, and clean .js is emitted*

### Why Developers Choose TypeScript

- Catches bugs before code runs
- Better IDE support (autocomplete, refactoring)
- Self-documenting code (types serve as documentation)
- Used by most major projects (React, Angular, VS Code, Deno)

---

## Installing Your Tools

> 🎯 **Teach:** How to install and verify Node.js, npm, TypeScript, and ts-node — the complete development toolchain. **See:** Terminal commands that confirm each tool is installed and working. **Feel:** Ready to start writing TypeScript with a fully working development environment.

### Install Node.js and npm

Check if Node.js is already installed:

```bash
node --version
npm --version
```

If not installed, download from [nodejs.org](https://nodejs.org) (LTS version) or use a package manager:

```bash
# macOS
brew install node

# Ubuntu/Debian
sudo apt install nodejs npm

# Or use nvm (Node Version Manager) — recommended
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

### Install TypeScript Globally

```bash
npm install -g typescript
tsc --version
```

### Install ts-node for Direct Execution

```bash
npm install -g ts-node
```

`ts-node` lets you run `.ts` files directly without manually compiling first.

---

## Your First TypeScript Program

> 🎯 **Teach:** How to create, compile, and run a TypeScript file — the core write-compile-run workflow. **See:** A `.ts` file compiled to `.js` with type annotations stripped away, and the same file run directly with ts-node. **Feel:** The satisfaction of writing and running your first TypeScript program from scratch.

### Create and Compile a TypeScript File

```bash
mkdir ~/ts-practice
cd ~/ts-practice
```

Create `hello.ts`:

```typescript
const greeting: string = "Hello, TypeScript!";
const year: number = 2026;
const isLearning: boolean = true;

console.log(greeting);
console.log(`Year: ${year}`);
console.log(`Currently learning: ${isLearning}`);
```

Compile and run:

```bash
tsc hello.ts
ls          # You should see hello.js alongside hello.ts
cat hello.js  # See the compiled JavaScript — type annotations are gone
node hello.js
```

### Run Directly with ts-node

```bash
ts-node hello.ts
```

Same output, no intermediate `.js` file needed. Use `ts-node` during development.

---

## See Type Checking in Action

> 🎯 **Teach:** How TypeScript's compiler catches type errors with clear, actionable error messages — and how the same mistakes silently pass in JavaScript. **See:** Intentional type errors that produce compiler messages, compared with equivalent JavaScript that runs without complaint but produces wrong output. **Feel:** Convinced that TypeScript error messages are a helpful guide, not an obstacle.

### The Type Error Demo

> 🎙️ This is the moment where TypeScript's value becomes concrete. You are going to write code with intentional mistakes and watch the compiler catch every single one. In plain JavaScript, these mistakes would silently produce wrong results. In TypeScript, you get a clear error message telling you exactly what is wrong and exactly where it is. Pay attention to the error messages — learning to read them is a skill that will save you hours of debugging.

Create `type_errors.ts` — write code with intentional type errors:

```typescript
let name: string = "Campbell";
let age: number = 20;

// Uncomment each line one at a time and try to compile:

// age = "twenty";          // Error: string not assignable to number
// name = 42;               // Error: number not assignable to string
// let count: number = "5"; // Error: string not assignable to number

// This works — TypeScript allows valid operations
age = age + 1;
name = name.toUpperCase();
console.log(`${name}, age ${age}`);
```

Try to compile with the errors uncommented:

```bash
tsc type_errors.ts
```

Read the error messages — they tell you exactly what's wrong and where.

### Compare with JavaScript

Create `no_types.js` (plain JavaScript):

```javascript
let age = 20;
age = "twenty"; // No error!
console.log(age + 1); // "twenty1" — silent bug!
```

```bash
node no_types.js
```

It runs without complaint but produces wrong output. This is exactly the kind of bug TypeScript prevents.

---

## Initialize a TypeScript Project

> 🎯 **Teach:** How to set up a proper TypeScript project with `package.json`, `tsconfig.json`, and local dependencies. **See:** The commands that scaffold a real project structure and the files they create. **Feel:** Confident initializing a professional TypeScript project from an empty directory.

### Create a Proper Project

```bash
mkdir ~/ts-project
cd ~/ts-project
npm init -y
npm install --save-dev typescript ts-node @types/node
npx tsc --init
```

This creates:
- `package.json` — Project configuration and dependencies
- `tsconfig.json` — TypeScript compiler configuration
- `node_modules/` — Installed packages

Create `src/index.ts`:

```bash
mkdir src
```

```typescript
// src/index.ts
function greet(name: string): string {
    return `Hello, ${name}! Welcome to TypeScript.`;
}

const message = greet("Campbell");
console.log(message);
console.log(`Node.js version: ${process.version}`);
```

Run it:

```bash
npx ts-node src/index.ts
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to apply everything from this module through hands-on practice. **See:** Exercises that walk through creating files, compiling, reading errors, and initializing projects. **Feel:** Capable of completing each task independently, solidifying the concepts from this module.

> ✏️ Sharpen Your Pencil

1. Create a file called `hello.ts` with three typed variables (string, number, boolean) and log them.
2. Compile it with `tsc` and examine the generated `.js` file. What is different? What is the same?
3. Create `type_errors.ts` with at least three intentional type errors. Uncomment them one at a time and read each compiler error.
4. Create the equivalent bugs in a plain `.js` file and run it with `node`. Compare the experience.
5. Initialize a TypeScript project with `npm init` and `tsc --init`. Run a simple program with `npx ts-node`.

---

> 💡 **Remember this one thing:** TypeScript catches bugs at compile time that JavaScript misses at runtime.

---

## Up Next

> 🎯 **Teach:** What comes next in the learning path and why it matters. **See:** A preview of Module 1's focus on TypeScript's type vocabulary. **Feel:** Eager to move forward with a solid foundation in place.

In **Module 1: Variables and Types**, you will learn TypeScript's full vocabulary of types — primitives, special types, type inference, and when to annotate versus when to let the compiler figure it out.
