# Module 15: npm and Package Management

> 🏷️ Advanced

> 🎯 **Teach:** How npm manages dependencies, scripts, and project metadata through package.json. **See:** A complete npm workflow from initialization through installing packages, writing scripts, and understanding semantic versioning. **Feel:** Confident that you can set up and manage any TypeScript project's dependencies and build pipeline.

> 🔄 **Where this fits:** You have been writing TypeScript files and compiling them by hand. Real projects use npm to manage dependencies, automate builds, and share code. This module introduces the tooling layer that turns individual .ts files into a professional project.

## What Is npm?

> 🎯 **Teach:** What npm is and the three things it manages -- dependencies, scripts, and metadata. **See:** A package.json file with dependencies, devDependencies, and scripts sections. **Feel:** Clear on why npm is the foundation of every professional TypeScript project.

### The JavaScript Ecosystem's Package Manager

> 🎙️ npm is the default package manager for Node.js, and it is the gateway to the largest software registry in the world. Every serious TypeScript project uses npm to manage three things: dependencies (the packages your project needs), scripts (the commands you run to build, test, and deploy), and metadata (your project's name, version, and configuration). The package.json file is the heart of every Node.js and TypeScript project.

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js"
  },
  "dependencies": {
    "axios": "^1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0"
  }
}
```

### dependencies vs devDependencies

- **dependencies** -- packages needed at runtime (`axios`, `express`)
- **devDependencies** -- packages needed only for development (`typescript`, `vitest`, `@types/node`)

![npm package.json at the center of a project, with arrows connecting to node_modules, scripts, and the npm registry](../images/module-15/npm-ecosystem.png)
*package.json is the heart of every Node.js project*

---

## Initializing a Project

> 🎯 **Teach:** How to create a new project with `npm init` and what each prompt means. **See:** Interactive and quick (`-y`) initialization side by side, producing a package.json. **Feel:** Comfortable starting any new project from an empty directory.

### Interactive Init with npm init

> 🎙️ Every project starts with npm init. This command walks you through creating a package.json file by asking a series of questions: project name, version, description, entry point, and license. You can also skip the questions entirely with the dash-y flag, which accepts all the defaults. Either way, you end up with a package.json that defines your project.

```bash
mkdir ~/npm-practice
cd ~/npm-practice
npm init
```

Walk through each prompt:
- **name:** `npm-practice`
- **version:** `1.0.0`
- **description:** `Learning npm and package management`
- **entry point:** `dist/index.js`
- **test command:** leave blank for now
- **keywords:** `typescript, learning`
- **author:** your name
- **license:** `MIT`

Open `package.json` and examine the result.

### Quick Init with -y

Create a second project using the `-y` flag to accept all defaults:

```bash
mkdir ~/npm-quick
cd ~/npm-quick
npm init -y
```

Compare the generated `package.json` to the one you created interactively. Notice the defaults.

---

## Installing Packages

> 🎯 **Teach:** How to install runtime and dev dependencies, and what node_modules and the lock file do. **See:** `npm install` adding packages, the updated package.json, and a TypeScript file using lodash. **Feel:** Confident that you know exactly where packages go and why the lock file matters.

### Adding Dependencies

> 🎙️ Installing packages is where npm really shines. The npm install command downloads a package from the registry, saves it into node_modules, and records it in your package.json. Use the save-dev flag for packages that are only needed during development, like TypeScript itself or type definition packages. The node_modules directory can contain thousands of files -- that is normal. Never commit it to version control.

Back in `~/npm-practice`:

```bash
cd ~/npm-practice

# Install a runtime dependency
npm install chalk@5

# Install dev dependencies
npm install --save-dev typescript ts-node @types/node

# Install type definitions for a library
npm install lodash
npm install --save-dev @types/lodash
```

After installing, examine the results:

```bash
# Check what was added to package.json
cat package.json

# Look at node_modules directory
ls node_modules | head -20

# Check the lock file
ls package-lock.json
```

### Understanding the Lock File

Open `package-lock.json` and observe:
- It pins exact versions of every dependency (and their sub-dependencies)
- It ensures everyone on a team gets identical installs
- **Never delete it** -- commit it to version control

### Using Installed Packages

Create `show_packages.ts`:

```typescript
// show_packages.ts
import _ from "lodash";

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Use lodash functions
const chunked = _.chunk(numbers, 3);
console.log("Chunked:", chunked);

const shuffled = _.shuffle(numbers);
console.log("Shuffled:", shuffled);

const grouped = _.groupBy(numbers, n => n % 2 === 0 ? "even" : "odd");
console.log("Grouped:", grouped);

// Show package info
import { readFileSync } from "fs";
const pkg = JSON.parse(readFileSync("./package.json", "utf-8"));
console.log(`\nProject: ${pkg.name} v${pkg.version}`);
console.log("Dependencies:", Object.keys(pkg.dependencies || {}));
console.log("Dev Dependencies:", Object.keys(pkg.devDependencies || {}));
```

Run it:

```bash
npx ts-node show_packages.ts
```

---

## npm Scripts

> 🎯 **Teach:** How to define and use npm scripts as your project's command center. **See:** A scripts section with build, start, dev, clean, and prebuild commands working together. **Feel:** Empowered to automate your entire build-and-run workflow with short, memorable commands.

### Your Project's Command Center

> 🎙️ npm scripts are custom commands you define in package.json. Instead of remembering long compiler flags or complex shell commands, you give them short names like build, start, and dev. This is how every professional project works: the scripts section of package.json is the single source of truth for how to build, run, and test the project. Anyone who clones your repo can look at the scripts and immediately know how to work with it.

Edit `package.json` to add these scripts:

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "clean": "rm -rf dist",
    "prebuild": "npm run clean",
    "typecheck": "tsc --noEmit"
  }
}
```

Notice `prebuild` -- npm automatically runs scripts prefixed with `pre` before the matching script. So `npm run build` will first run `clean`, then `tsc`.

### Building a Task Manager with lodash

Create the directory structure and `src/index.ts`:

```bash
mkdir src
```

```typescript
// src/index.ts
import _ from "lodash";

interface Task {
    id: number;
    title: string;
    priority: "low" | "medium" | "high";
}

const tasks: Task[] = [
    { id: 1, title: "Learn npm", priority: "high" },
    { id: 2, title: "Write tests", priority: "medium" },
    { id: 3, title: "Deploy app", priority: "high" },
    { id: 4, title: "Update docs", priority: "low" },
    { id: 5, title: "Fix bug", priority: "medium" },
];

const byPriority = _.groupBy(tasks, "priority");

console.log("Tasks by priority:");
for (const [priority, group] of Object.entries(byPriority)) {
    console.log(`  ${priority}: ${group.map(t => t.title).join(", ")}`);
}

console.log(`\nTotal tasks: ${tasks.length}`);
console.log(`High priority: ${byPriority["high"]?.length ?? 0}`);
```

Initialize TypeScript and build:

```bash
npx tsc --init --outDir dist --rootDir src --strict
npm run build
npm start
```

Test the dev script:

```bash
npm run dev
```

---

## npx: Run Without Installing

> 🎯 **Teach:** How npx runs packages without installing them globally. **See:** npx executing one-off commands and running local project tools like tsc and ts-node. **Feel:** Relieved that you don't need to install everything globally to use it.

### One-Off Commands

> 🎙️ npx is npm's companion tool for running packages without installing them globally. When you type npx followed by a command, it first checks your local node_modules, then checks if the package is installed globally, and finally downloads it temporarily if needed. This is how you run project-local tools like tsc or ts-node, and it is how you try out packages without cluttering your global installation.

```bash
# Run a one-off command
npx cowsay "Hello from npx!"

# Run the local tsc
npx tsc --version

# Run ts-node from local install
npx ts-node src/index.ts
```

---

## Semantic Versioning

> 🎯 **Teach:** How semantic versioning works and what caret, tilde, and pinned specifiers mean. **See:** A breakdown of MAJOR.MINOR.PATCH with real package examples and a reference table. **Feel:** Confident reading version specifiers in any package.json without guessing.

### Understanding Version Numbers

> 🎙️ Every npm package follows semantic versioning, or SemVer. Version numbers have three parts: major dot minor dot patch. A major version bump means breaking changes. A minor bump means new features that are backward compatible. A patch bump means bug fixes. The symbols in front of version numbers in package.json control how much npm is allowed to update automatically. The caret allows minor and patch updates. The tilde allows only patch updates. And a bare version number means that exact version, no updates at all.

Create `versioning.ts`:

```typescript
// versioning.ts
// Demonstrate understanding of semantic versioning

interface PackageVersion {
    name: string;
    specifier: string;
    meaning: string;
}

const examples: PackageVersion[] = [
    {
        name: "typescript",
        specifier: "^5.3.0",
        meaning: "Any version >= 5.3.0 and < 6.0.0 (caret: minor + patch updates)",
    },
    {
        name: "lodash",
        specifier: "~4.17.21",
        meaning: "Any version >= 4.17.21 and < 4.18.0 (tilde: patch updates only)",
    },
    {
        name: "express",
        specifier: "4.18.2",
        meaning: "Exactly version 4.18.2 (pinned: no updates)",
    },
    {
        name: "react",
        specifier: ">=18.0.0",
        meaning: "Any version 18.0.0 or higher (range: risky in production)",
    },
    {
        name: "vitest",
        specifier: "^1.0.0",
        meaning: "Any version >= 1.0.0 and < 2.0.0 (caret: standard choice)",
    },
];

console.log("Semantic Versioning Examples\n");
console.log("Format: MAJOR.MINOR.PATCH\n");

for (const pkg of examples) {
    console.log(`${pkg.name} @ ${pkg.specifier}`);
    console.log(`  → ${pkg.meaning}\n`);
}

// Useful npm commands reference
const commands = [
    ["npm install <pkg>", "Install as dependency"],
    ["npm install -D <pkg>", "Install as devDependency"],
    ["npm uninstall <pkg>", "Remove a package"],
    ["npm update", "Update packages within semver range"],
    ["npm outdated", "Show packages needing updates"],
    ["npm list --depth=0", "Show top-level installed packages"],
    ["npm audit", "Check for security vulnerabilities"],
];

console.log("\nUseful npm Commands:");
for (const [cmd, desc] of commands) {
    console.log(`  ${cmd.padEnd(30)} — ${desc}`);
}
```

Run it:

```bash
npx ts-node versioning.ts
```

```
MAJOR — breaking changes
MINOR — new features, backward compatible
PATCH — bug fixes, backward compatible
```

| Specifier | Example | Meaning |
|-----------|---------|---------|
| `^1.6.0` | Caret | Compatible with 1.x.x (allows minor and patch) |
| `~1.6.0` | Tilde | Approximately 1.6.x (allows patch only) |
| `1.6.0` | Pinned | Exact version, no updates |

---

## Essential npm Commands

> 🎯 **Teach:** The key npm commands for inspecting and maintaining project health. **See:** `npm list`, `npm outdated`, and `npm audit` output showing dependency status. **Feel:** Prepared to keep any project's dependencies up to date and secure.

### Managing Your Project

> 🎙️ Beyond install, npm gives you several commands for managing your project's dependencies. npm list shows what is installed. npm outdated shows which packages have newer versions available. npm audit checks for known security vulnerabilities. These are commands you should run regularly to keep your project healthy and secure.

Run each of these and observe the output:

```bash
npm list --depth=0
npm outdated
npm audit
```

| Command | Purpose |
|---------|---------|
| `npm install <pkg>` | Install as dependency |
| `npm install -D <pkg>` | Install as devDependency |
| `npm uninstall <pkg>` | Remove a package |
| `npm update` | Update packages within semver range |
| `npm outdated` | Show packages needing updates |
| `npm list --depth=0` | Show top-level installed packages |
| `npm audit` | Check for security vulnerabilities |

---

## Sharpen Your Pencil

> ✏️ Sharpen Your Pencil

1. Create a new project with `npm init` (interactive) and examine the generated `package.json`.
2. Create a second project with `npm init -y` and compare the defaults.
3. Install `lodash` as a dependency and `@types/lodash` as a devDependency. Write `show_packages.ts` using lodash's `chunk`, `shuffle`, and `groupBy` functions.
4. Add `build`, `dev`, and `start` scripts to your `package.json`. Create `src/index.ts` with the task management example and verify all three scripts work.
5. Create `versioning.ts` demonstrating caret, tilde, and pinned version specifiers.
6. Run `npm list --depth=0`, `npm outdated`, and `npm audit`. What did each command show you?
7. Use `npx` to run a package you have not installed globally.

---

> 💡 **Remember this one thing:** npm scripts are your project's command center -- define build, test, and dev commands in package.json so anyone can work with your project immediately.

---

## Up Next

In **Module 16: tsconfig and Build Configuration**, you will learn how `tsconfig.json` controls every aspect of TypeScript compilation -- from which JavaScript version to target, to which type-checking rules to enforce.
