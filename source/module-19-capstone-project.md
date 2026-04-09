# Module 19: Capstone Project

> 🏷️ Advanced

> 🎯 **Teach:** How to build a complete, well-structured TypeScript project from scratch -- combining types, modules, testing, configuration, and build scripts into a professional whole. **See:** A fully functional Task Tracker CLI with proper project layout, type definitions, core logic, CLI interface, and comprehensive tests. **Feel:** The satisfaction of seeing everything from this entire course come together in one real project.

> 🔄 **Where this fits:** This is where all 19 modules come together. Every concept you have learned -- type annotations, interfaces, classes, generics, utility types, modules, async patterns, error handling, npm, tsconfig, and testing -- gets applied in a single cohesive project. This is how professional TypeScript projects look.

## The Task Tracker CLI

> 🎯 **Teach:** What you are building -- a complete Task Tracker CLI with proper project structure, types, logic, interface, and tests. **See:** The standard project layout with src/, tests/, package.json, tsconfig.json, and .gitignore. **Feel:** Excited to bring every concept from the entire course together in one real project.

### Project Overview

> 🎙️ In this capstone, you will build a Task Tracker command-line application from scratch. This is not a toy example -- it has the same structure as a real production TypeScript project. There is a types file that defines all the data shapes. There is a store module that handles the core business logic. There is a CLI module that parses commands and formats output. There is an entry point that ties it all together. And there are tests that verify everything works. The project includes proper npm scripts, a tsconfig.json, and a .gitignore. When you finish this module, you will have built something you can point to and say: I know how to structure a TypeScript project.

### Standard Project Layout

```
task-tracker/
  src/
    index.ts          # Entry point
    types.ts          # Type definitions
    task-store.ts     # Core logic
    cli.ts            # CLI interface
  tests/
    task-store.test.ts
  package.json
  tsconfig.json
  .gitignore
```

![A complete project structure with types, logic, CLI, and tests all connected](../images/module-19/project-structure.png)
*A well-structured TypeScript project separates types, logic, interface, and tests*

---

## Project Initialization

> 🎯 **Teach:** How to initialize a professional project with npm, TypeScript, Vitest, and a complete set of npm scripts. **See:** `npm init`, dependency installation, tsconfig.json, .gitignore, and scripts for build, start, dev, test, and clean. **Feel:** Confident that you can set up a production-quality project scaffold from scratch.

### Setting Up package.json and Dependencies

> 🎙️ Every project starts with npm init and installing your dependencies. For this project, you need TypeScript for compilation, Vitest for testing, and the Node.js type definitions. All three are dev dependencies because they are tools you use during development, not code that runs in production. The scripts section defines your entire workflow: build compiles TypeScript, start runs the compiled output, dev runs directly with ts-node, test runs your test suite, and clean removes the build output.

```bash
mkdir ~/task-tracker
cd ~/task-tracker
npm init -y
npm install --save-dev typescript vitest @types/node
```

### Creating tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "declaration": true,
    "sourceMap": true,
    "resolveJsonModule": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "tests"]
}
```

### Creating .gitignore

```
node_modules/
dist/
coverage/
*.js.map
.DS_Store
```

### Configuring npm Scripts

Add these scripts to `package.json`:

```json
{
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "npx ts-node src/index.ts",
    "test": "vitest run",
    "test:watch": "vitest",
    "clean": "rm -rf dist"
  }
}
```

Create the source and test directories:

```bash
mkdir src tests
```

---

## Type Definitions

> 🎯 **Teach:** How to centralize all type definitions in a single file so every module shares a single source of truth. **See:** Task, Priority, Status, TaskFilter, TaskStats, and derived input types using Pick and Partial. **Feel:** Appreciation for how well-designed types make the rest of the codebase safer and more maintainable.

### Defining the Data Shapes

> 🎙️ The types file is where you define every data shape your application uses. This is a practice that pays enormous dividends as your project grows. By centralizing your type definitions, every module in your project imports from a single source of truth. The Task interface defines what a task looks like. TaskFilter defines how to search for tasks. TaskStats defines the shape of aggregate statistics. And the CreateTaskInput and UpdateTaskInput types use Pick and Partial to derive input shapes from the Task interface, so they stay in sync automatically.

Create `src/types.ts`:

```typescript
// src/types.ts

export type Priority = "low" | "medium" | "high";
export type Status = "todo" | "in-progress" | "done";

export interface Task {
    id: number;
    title: string;
    description: string;
    priority: Priority;
    status: Status;
    createdAt: Date;
    completedAt: Date | null;
}

export interface TaskFilter {
    status?: Status;
    priority?: Priority;
    search?: string;
}

export interface TaskStats {
    total: number;
    todo: number;
    inProgress: number;
    done: number;
    byPriority: Record<Priority, number>;
}

export type CreateTaskInput = Pick<Task, "title" | "description" | "priority">;
export type UpdateTaskInput = Partial<Pick<Task, "title" | "description" | "priority" | "status">>;
```

Notice the patterns at work:
- **Union types** for `Priority` and `Status` -- only valid values are allowed
- **Utility types** `Pick` and `Partial` derive input types from `Task`
- **Record** type for `byPriority` maps each priority to a count
- **Null union** for `completedAt` -- a task is only complete when it has a date

---

## Core Logic

> 🎯 **Teach:** How to build a type-safe business logic layer with precise input/output types for every operation. **See:** The TaskStore class with add, getById, update, delete, list (with filters), getStats, and clear methods. **Feel:** Proud of writing a clean, fully-typed API that handles every operation the application needs.

### The TaskStore Class

> 🎙️ The TaskStore is the core of the application. It manages an array of tasks and provides methods for every operation: add, getById, update, delete, list with filters, get statistics, and clear. Notice how every method has precise input and output types. The add method takes a CreateTaskInput and returns a full Task with auto-generated id, status, and timestamps. The update method takes an UpdateTaskInput where every field is optional -- you update only what you pass. The list method accepts an optional TaskFilter that can filter by status, priority, or search text. This is the kind of clean, type-safe API that TypeScript makes possible.

Create `src/task-store.ts`:

```typescript
// src/task-store.ts
import { Task, CreateTaskInput, UpdateTaskInput, TaskFilter, TaskStats, Status, Priority } from "./types";

export class TaskStore {
    private tasks: Task[] = [];
    private nextId = 1;

    add(input: CreateTaskInput): Task {
        const task: Task = {
            id: this.nextId++,
            title: input.title,
            description: input.description,
            priority: input.priority,
            status: "todo",
            createdAt: new Date(),
            completedAt: null,
        };
        this.tasks.push(task);
        return task;
    }

    getById(id: number): Task | undefined {
        return this.tasks.find(t => t.id === id);
    }

    update(id: number, input: UpdateTaskInput): Task {
        const task = this.getById(id);
        if (!task) throw new Error(`Task ${id} not found`);

        if (input.title !== undefined) task.title = input.title;
        if (input.description !== undefined) task.description = input.description;
        if (input.priority !== undefined) task.priority = input.priority;
        if (input.status !== undefined) {
            task.status = input.status;
            task.completedAt = input.status === "done" ? new Date() : null;
        }

        return task;
    }

    delete(id: number): boolean {
        const index = this.tasks.findIndex(t => t.id === id);
        if (index === -1) return false;
        this.tasks.splice(index, 1);
        return true;
    }

    list(filter?: TaskFilter): Task[] {
        let results = [...this.tasks];

        if (filter?.status) {
            results = results.filter(t => t.status === filter.status);
        }
        if (filter?.priority) {
            results = results.filter(t => t.priority === filter.priority);
        }
        if (filter?.search) {
            const term = filter.search.toLowerCase();
            results = results.filter(
                t => t.title.toLowerCase().includes(term) ||
                     t.description.toLowerCase().includes(term)
            );
        }

        return results;
    }

    getStats(): TaskStats {
        const stats: TaskStats = {
            total: this.tasks.length,
            todo: 0,
            inProgress: 0,
            done: 0,
            byPriority: { low: 0, medium: 0, high: 0 },
        };

        for (const task of this.tasks) {
            if (task.status === "todo") stats.todo++;
            else if (task.status === "in-progress") stats.inProgress++;
            else if (task.status === "done") stats.done++;

            stats.byPriority[task.priority]++;
        }

        return stats;
    }

    clear(): void {
        this.tasks = [];
        this.nextId = 1;
    }
}
```

---

## CLI Interface

> 🎯 **Teach:** How to separate the user-facing layer from business logic, with command parsing and output formatting as distinct responsibilities. **See:** formatTask, formatTaskDetail, and a runCli switch statement that dispatches commands to TaskStore methods. **Feel:** Clear on why separation of concerns makes both the CLI and the store easier to test and maintain.

### Command Parsing and Output Formatting

> 🎙️ The CLI module handles the user-facing layer. It takes raw command arguments, calls the appropriate TaskStore methods, and formats the results for display. The formatTask function produces a compact one-line summary with status icons and priority tags. The formatTaskDetail function produces a full multi-line view. And the runCli function is a switch statement that dispatches commands to store methods. Notice that the CLI module does not manage state -- it receives a TaskStore instance and delegates all logic to it. This separation of concerns makes both modules easier to test and maintain.

Create `src/cli.ts`:

```typescript
// src/cli.ts
import { TaskStore } from "./task-store";
import { Priority, Status, Task } from "./types";

export function formatTask(task: Task): string {
    const statusIcon = task.status === "done" ? "[x]" : task.status === "in-progress" ? "[~]" : "[ ]";
    const priorityTag = `(${task.priority})`;
    return `${statusIcon} #${task.id} ${priorityTag} ${task.title}`;
}

export function formatTaskDetail(task: Task): string {
    const lines = [
        `Task #${task.id}`,
        `  Title:       ${task.title}`,
        `  Description: ${task.description}`,
        `  Priority:    ${task.priority}`,
        `  Status:      ${task.status}`,
        `  Created:     ${task.createdAt.toISOString()}`,
    ];
    if (task.completedAt) {
        lines.push(`  Completed:   ${task.completedAt.toISOString()}`);
    }
    return lines.join("\n");
}

export function runCli(store: TaskStore, args: string[]): string {
    const command = args[0];

    switch (command) {
        case "add": {
            const title = args[1];
            const description = args[2] || "";
            const priority = (args[3] as Priority) || "medium";
            if (!title) return "Usage: add <title> [description] [low|medium|high]";
            const task = store.add({ title, description, priority });
            return `Added: ${formatTask(task)}`;
        }

        case "list": {
            const filter = args[1] as Status | undefined;
            const tasks = store.list(filter ? { status: filter } : undefined);
            if (tasks.length === 0) return "No tasks found.";
            return tasks.map(formatTask).join("\n");
        }

        case "view": {
            const id = parseInt(args[1]);
            if (isNaN(id)) return "Usage: view <id>";
            const task = store.getById(id);
            if (!task) return `Task ${id} not found.`;
            return formatTaskDetail(task);
        }

        case "done": {
            const id = parseInt(args[1]);
            if (isNaN(id)) return "Usage: done <id>";
            try {
                const task = store.update(id, { status: "done" });
                return `Completed: ${formatTask(task)}`;
            } catch (err) {
                return (err as Error).message;
            }
        }

        case "delete": {
            const id = parseInt(args[1]);
            if (isNaN(id)) return "Usage: delete <id>";
            return store.delete(id) ? `Deleted task #${id}.` : `Task ${id} not found.`;
        }

        case "stats": {
            const stats = store.getStats();
            return [
                `Total: ${stats.total}`,
                `  Todo:        ${stats.todo}`,
                `  In Progress: ${stats.inProgress}`,
                `  Done:        ${stats.done}`,
                `  High:        ${stats.byPriority.high}`,
                `  Medium:      ${stats.byPriority.medium}`,
                `  Low:         ${stats.byPriority.low}`,
            ].join("\n");
        }

        default:
            return [
                "Task Tracker Commands:",
                "  add <title> [description] [priority]  — Add a task",
                "  list [status]                         — List tasks",
                "  view <id>                             — View task details",
                "  done <id>                             — Mark task as done",
                "  delete <id>                           — Delete a task",
                "  stats                                 — Show statistics",
            ].join("\n");
    }
}
```

---

## Entry Point

> 🎯 **Teach:** How a minimal entry point wires modules together and demonstrates every feature of the application. **See:** index.ts creating a TaskStore, running a series of demo CLI commands, and printing output. **Feel:** Satisfied that the entry point is simple because the real work is cleanly distributed across modules.

### Tying It All Together

> 🎙️ The entry point is the simplest file in the project. It creates a TaskStore, runs a series of demo commands to show the application working, and prints the output. In a real CLI application, you would read commands from process.argv or an interactive prompt. Here, we simulate a sequence of commands to demonstrate every feature: adding tasks, listing them, marking one as done, viewing statistics, inspecting a single task, filtering by status, deleting a task, and listing again to see the result.

Create `src/index.ts`:

```typescript
// src/index.ts
import { TaskStore } from "./task-store";
import { runCli } from "./cli";

const store = new TaskStore();

// Demo: simulate a series of CLI commands
const commands = [
    ["help"],
    ["add", "Learn TypeScript", "Complete all 20 days", "high"],
    ["add", "Write tests", "Unit test the task tracker", "high"],
    ["add", "Read documentation", "Read the TypeScript handbook", "medium"],
    ["add", "Clean up code", "Refactor old exercises", "low"],
    ["list"],
    ["done", "1"],
    ["stats"],
    ["view", "2"],
    ["list", "todo"],
    ["delete", "4"],
    ["list"],
];

for (const args of commands) {
    console.log(`\n> task ${args.join(" ")}`);
    console.log(runCli(store, args));
}
```

---

## Tests

> 🎯 **Teach:** How to write a professional test suite with beforeEach isolation, grouped describe blocks, and coverage of every method and edge case. **See:** task-store.test.ts testing add, getById, update, delete, list with filters, and getStats with sample data. **Feel:** Confident that a well-tested core means fearless refactoring and reliable deployments.

### Comprehensive Test Suite

> 🎙️ The test suite for TaskStore covers every method with multiple scenarios. The beforeEach hook creates a fresh store for every test, ensuring tests are isolated and do not affect each other. The add tests verify that tasks get correct properties and auto-incrementing IDs. The update tests verify that properties change, that completedAt is set when a task is marked done, and that updating a missing task throws an error. The list tests use a second beforeEach to populate the store with sample data, then test filtering by priority, status, and search term. This is what a professional test suite looks like.

Create `tests/task-store.test.ts`:

```typescript
// tests/task-store.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { TaskStore } from "../src/task-store";

describe("TaskStore", () => {
    let store: TaskStore;

    beforeEach(() => {
        store = new TaskStore();
    });

    describe("add", () => {
        it("creates a task with correct properties", () => {
            const task = store.add({ title: "Test", description: "Desc", priority: "high" });
            expect(task.id).toBe(1);
            expect(task.title).toBe("Test");
            expect(task.status).toBe("todo");
            expect(task.completedAt).toBeNull();
        });

        it("auto-increments ids", () => {
            const t1 = store.add({ title: "A", description: "", priority: "low" });
            const t2 = store.add({ title: "B", description: "", priority: "low" });
            expect(t2.id).toBe(t1.id + 1);
        });
    });

    describe("getById", () => {
        it("finds existing task", () => {
            const task = store.add({ title: "Find me", description: "", priority: "medium" });
            expect(store.getById(task.id)?.title).toBe("Find me");
        });

        it("returns undefined for missing task", () => {
            expect(store.getById(999)).toBeUndefined();
        });
    });

    describe("update", () => {
        it("updates task properties", () => {
            const task = store.add({ title: "Old", description: "", priority: "low" });
            const updated = store.update(task.id, { title: "New", priority: "high" });
            expect(updated.title).toBe("New");
            expect(updated.priority).toBe("high");
        });

        it("sets completedAt when status is done", () => {
            const task = store.add({ title: "Task", description: "", priority: "medium" });
            const done = store.update(task.id, { status: "done" });
            expect(done.completedAt).toBeInstanceOf(Date);
        });

        it("throws for missing task", () => {
            expect(() => store.update(999, { title: "X" })).toThrow("not found");
        });
    });

    describe("delete", () => {
        it("removes existing task", () => {
            const task = store.add({ title: "Delete me", description: "", priority: "low" });
            expect(store.delete(task.id)).toBe(true);
            expect(store.getById(task.id)).toBeUndefined();
        });

        it("returns false for missing task", () => {
            expect(store.delete(999)).toBe(false);
        });
    });

    describe("list", () => {
        beforeEach(() => {
            store.add({ title: "Low task", description: "desc", priority: "low" });
            store.add({ title: "High task", description: "important", priority: "high" });
            store.add({ title: "Medium task", description: "normal", priority: "medium" });
        });

        it("returns all tasks without filter", () => {
            expect(store.list()).toHaveLength(3);
        });

        it("filters by priority", () => {
            const high = store.list({ priority: "high" });
            expect(high).toHaveLength(1);
            expect(high[0].title).toBe("High task");
        });

        it("filters by search term", () => {
            const results = store.list({ search: "important" });
            expect(results).toHaveLength(1);
            expect(results[0].title).toBe("High task");
        });

        it("filters by status", () => {
            store.update(1, { status: "done" });
            const done = store.list({ status: "done" });
            expect(done).toHaveLength(1);
        });
    });

    describe("getStats", () => {
        it("returns correct statistics", () => {
            store.add({ title: "A", description: "", priority: "high" });
            store.add({ title: "B", description: "", priority: "medium" });
            store.add({ title: "C", description: "", priority: "high" });
            store.update(2, { status: "done" });

            const stats = store.getStats();
            expect(stats.total).toBe(3);
            expect(stats.todo).toBe(2);
            expect(stats.done).toBe(1);
            expect(stats.byPriority.high).toBe(2);
            expect(stats.byPriority.medium).toBe(1);
        });
    });
});
```

---

## Build, Test, and Run

> 🎯 **Teach:** How to verify the complete project end to end -- tests pass, build succeeds, and the compiled output runs correctly. **See:** `npm test`, `npm run build`, `npm start`, and the dist/ directory containing .js, .d.ts, and .js.map files. **Feel:** The satisfaction of a fully working pipeline from TypeScript source to tested, compiled, runnable output.

### Verifying the Complete Project

> 🎙️ This is the final step: running the tests, building the project, and running the compiled output. When all tests pass, you know your core logic is correct. When the build succeeds, you know your TypeScript configuration is right. And when npm start produces the expected output, you know your entire pipeline works end to end. Check the dist directory -- you should see compiled JavaScript, declaration files, and source maps for every module. This is what a complete, well-structured TypeScript project looks like.

```bash
# Run the tests
npm test

# Build the project
npm run build

# Run the compiled output
npm start

# Verify the dist/ directory structure
ls dist/
```

Confirm:
- All tests pass
- `dist/` contains compiled `.js`, `.d.ts`, and `.js.map` files
- `npm start` produces correct CLI demo output

---

## Sharpen Your Pencil

> ✏️ Sharpen Your Pencil

1. Set up the complete project from scratch: `npm init`, install dependencies, create `tsconfig.json`, `.gitignore`, and npm scripts.
2. Create `src/types.ts` with `Task`, `Priority`, `Status`, `TaskFilter`, `TaskStats`, `CreateTaskInput`, and `UpdateTaskInput`.
3. Create `src/task-store.ts` with `add`, `getById`, `update`, `delete`, `list`, `getStats`, and `clear` methods.
4. Create `src/cli.ts` with `formatTask`, `formatTaskDetail`, and `runCli` functions.
5. Create `src/index.ts` that demos every CLI command.
6. Create `tests/task-store.test.ts` with comprehensive tests for every TaskStore method, using `beforeEach` for test isolation.
7. Run `npm test` -- all tests should pass. Run `npm run build` and `npm start` -- the demo should produce correct output.
8. Examine `dist/` and verify it contains `.js`, `.d.ts`, and `.js.map` files.

---

> 💡 **Remember this one thing:** A well-structured TypeScript project combines types, modules, testing, and build config into a maintainable whole.

---

## Congratulations

> 🎙️ You have completed all 20 modules of TypeScript Fundamentals. You started with a single hello.ts file and built your way up to a complete, tested, well-structured CLI application. Along the way, you learned type annotations, interfaces, classes, generics, utility types, type narrowing, modules, async/await, error handling, JSON and APIs, npm, tsconfig, testing with Vitest, and advanced patterns including decorators, mapped types, and template literal types. These are not just academic concepts -- they are the tools that professional TypeScript developers use every day. The next step is to build something of your own. Pick a project, set up the structure you learned here, and start writing TypeScript with confidence.

You have covered:

| Module | Topic |
|--------|-------|
| 0 | What Is TypeScript |
| 1 | Variables and Types |
| 2 | Arrays, Tuples, and Objects |
| 3 | Functions and Type Signatures |
| 4 | Control Flow |
| 5 | Type Aliases and Unions |
| 6 | Interfaces |
| 7 | Classes |
| 8 | Generics |
| 9 | Enums and Utility Types |
| 10 | Type Narrowing |
| 11 | Modules and Imports |
| 12 | Async/Await and Promises |
| 13 | Error Handling |
| 14 | JSON and APIs |
| 15 | npm and Package Management |
| 16 | tsconfig and Build Configuration |
| 17 | Testing with Vitest |
| 18 | Advanced Patterns |
| 19 | Capstone Project |

The foundation is set. Now go build something.
