# Module 18: Advanced Patterns

> 🏷️ Advanced

> 🎯 **Teach:** How TypeScript's advanced type features and design patterns solve real architectural problems -- decorators for cross-cutting concerns, builder and singleton patterns for object creation, and mapped/conditional/template literal types for type-level programming. **See:** TC39 decorators logging method calls, a fluent builder API, a singleton database connection, and types that transform other types automatically. **Feel:** Empowered to reach for these tools when simpler approaches are not expressive enough.

> 🔄 **Where this fits:** You have mastered TypeScript's core type system -- generics, utility types, type narrowing. This module goes further, into patterns that let the type system model complex relationships and that let you write code that is both more expressive and more type-safe than what basic annotations can achieve.

## TC39 Stage 3 Decorators

> 🎯 **Teach:** How TC39 Stage 3 decorators add cross-cutting behavior like logging and timing to class methods without modifying the original code. **See:** `@log` and `@timed` decorators wrapping a MathService class, including stacking multiple decorators on one method. **Feel:** Excited that decorators solve real boilerplate problems elegantly.

### Method Decorators

> 🎙️ Decorators are a way to add behavior to classes and their members without modifying the original code. TypeScript 5 supports the TC39 Stage 3 decorator standard, which does not require the experimentalDecorators flag. A method decorator is a function that wraps a class method, adding logic before or after it runs. The two most common uses are logging (recording when methods are called and what they return) and timing (measuring how long methods take). Decorators solve a real problem: cross-cutting concerns that would otherwise require you to copy the same boilerplate into every method.

Set up the project:

```bash
mkdir ~/advanced-ts
cd ~/advanced-ts
npm init -y
npm install --save-dev typescript @types/node
```

Create `tsconfig.json` with decorator support:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "strict": true,
    "outDir": "dist",
    "rootDir": "src",
    "esModuleInterop": true,
    "experimentalDecorators": false
  },
  "include": ["src/**/*"]
}
```

Note: TypeScript 5 decorators use the TC39 Stage 3 standard and do **not** need `experimentalDecorators`.

```bash
mkdir src
```

Create `src/decorators.ts`:

```typescript
// src/decorators.ts

// --- Method decorator: logging ---
function log(
    _target: any,
    context: ClassMethodDecoratorContext
) {
    const methodName = String(context.name);
    return function (this: any, ...args: any[]) {
        console.log(`[LOG] ${methodName}(${args.map(a => JSON.stringify(a)).join(", ")})`);
        const result = (_target as Function).apply(this, args);
        console.log(`[LOG] ${methodName} returned ${JSON.stringify(result)}`);
        return result;
    };
}

// --- Method decorator: timing ---
function timed(
    _target: any,
    context: ClassMethodDecoratorContext
) {
    const methodName = String(context.name);
    return function (this: any, ...args: any[]) {
        const start = performance.now();
        const result = (_target as Function).apply(this, args);
        const elapsed = (performance.now() - start).toFixed(3);
        console.log(`[TIMER] ${methodName} took ${elapsed}ms`);
        return result;
    };
}

class MathService {
    @log
    add(a: number, b: number): number {
        return a + b;
    }

    @timed
    fibonacci(n: number): number {
        if (n <= 1) return n;
        return this.fibonacci(n - 1) + this.fibonacci(n - 2);
    }

    @log
    @timed
    multiply(a: number, b: number): number {
        return a * b;
    }
}

const math = new MathService();
math.add(3, 4);
console.log("---");
math.multiply(5, 6);
```

Compile and run:

```bash
npx tsc
node dist/decorators.js
```

Notice how `multiply` has both `@log` and `@timed` stacked -- decorators compose naturally.

---

## Builder Pattern

> 🎯 **Teach:** How the Builder pattern constructs complex objects step by step with a fluent, chainable API. **See:** A RequestBuilder class with method chaining that builds validated HttpRequest objects, including error handling for missing required fields. **Feel:** Appreciation for how builders make complex construction readable and type-safe.

### Fluent API for Complex Object Construction

> 🎙️ The Builder pattern solves the problem of constructing complex objects step by step. Instead of a constructor with ten parameters, you chain method calls that each configure one aspect of the object. Each setter method returns this, which enables the fluent chaining syntax. The build method at the end validates that all required properties are set and returns the final object. This pattern is especially powerful in TypeScript because the type system can enforce that required properties exist at compile time.

Create `src/builder.ts`:

```typescript
// src/builder.ts

interface HttpRequest {
    method: "GET" | "POST" | "PUT" | "DELETE";
    url: string;
    headers: Record<string, string>;
    body?: string;
    timeout: number;
}

class RequestBuilder {
    private request: Partial<HttpRequest> = {};

    setMethod(method: HttpRequest["method"]): this {
        this.request.method = method;
        return this;
    }

    setUrl(url: string): this {
        this.request.url = url;
        return this;
    }

    addHeader(key: string, value: string): this {
        if (!this.request.headers) {
            this.request.headers = {};
        }
        this.request.headers[key] = value;
        return this;
    }

    setBody(body: object): this {
        this.request.body = JSON.stringify(body);
        this.addHeader("Content-Type", "application/json");
        return this;
    }

    setTimeout(ms: number): this {
        this.request.timeout = ms;
        return this;
    }

    build(): HttpRequest {
        if (!this.request.method) throw new Error("Method is required");
        if (!this.request.url) throw new Error("URL is required");

        return {
            method: this.request.method,
            url: this.request.url,
            headers: this.request.headers ?? {},
            body: this.request.body,
            timeout: this.request.timeout ?? 5000,
        };
    }
}

// Usage — fluent, readable API
const getRequest = new RequestBuilder()
    .setMethod("GET")
    .setUrl("https://api.example.com/users")
    .addHeader("Authorization", "Bearer token123")
    .setTimeout(3000)
    .build();

const postRequest = new RequestBuilder()
    .setMethod("POST")
    .setUrl("https://api.example.com/users")
    .setBody({ name: "Alice", email: "alice@example.com" })
    .addHeader("Authorization", "Bearer token123")
    .build();

console.log("GET Request:", JSON.stringify(getRequest, null, 2));
console.log("\nPOST Request:", JSON.stringify(postRequest, null, 2));

// Builder pattern error handling
try {
    new RequestBuilder().setUrl("/test").build(); // Missing method
} catch (err) {
    console.log(`\nError caught: ${(err as Error).message}`);
}
```

---

## Singleton Pattern

> 🎯 **Teach:** How the Singleton pattern ensures exactly one instance of a class exists, and when this is the right choice. **See:** A Database class with a private constructor and static getInstance, plus a generic Registry for managing named service instances. **Feel:** Clear on when singletons are appropriate and how to implement them safely.

### One Instance, Shared Everywhere

> 🎙️ The Singleton pattern ensures a class has only one instance and provides a global point of access to it. This is the right pattern for resources that should not be duplicated, like database connections, configuration managers, or logging services. The private constructor prevents direct instantiation -- the only way to get an instance is through the static getInstance method, which creates the instance on first call and returns the existing instance on every subsequent call. The generic Registry class shows a related pattern: a single registry that manages named instances of any type.

Create `src/singleton.ts`:

```typescript
// src/singleton.ts

class Database {
    private static instance: Database | null = null;
    private connectionCount = 0;

    private constructor(private host: string, private port: number) {
        console.log(`[DB] Connecting to ${host}:${port}...`);
    }

    static getInstance(host = "localhost", port = 5432): Database {
        if (!Database.instance) {
            Database.instance = new Database(host, port);
        }
        return Database.instance;
    }

    query(sql: string): string {
        this.connectionCount++;
        return `[DB] Query #${this.connectionCount}: ${sql} → (results)`;
    }

    getInfo(): string {
        return `Connected to ${this.host}:${this.port}, queries executed: ${this.connectionCount}`;
    }

    // For testing: reset the singleton
    static resetInstance(): void {
        Database.instance = null;
    }
}

// Both variables point to the SAME instance
const db1 = Database.getInstance("db.example.com", 5432);
const db2 = Database.getInstance(); // Returns existing instance

console.log(db1 === db2); // true — same object

console.log(db1.query("SELECT * FROM users"));
console.log(db2.query("INSERT INTO logs VALUES ('test')"));
console.log(db1.getInfo()); // Shows 2 queries — both used the same instance

// Application-level singleton with generics
class Registry<T> {
    private items = new Map<string, T>();

    register(key: string, item: T): void {
        if (this.items.has(key)) {
            throw new Error(`Key "${key}" already registered`);
        }
        this.items.set(key, item);
    }

    get(key: string): T {
        const item = this.items.get(key);
        if (!item) throw new Error(`Key "${key}" not found`);
        return item;
    }

    list(): string[] {
        return [...this.items.keys()];
    }
}

interface Service {
    name: string;
    execute(): string;
}

const registry = new Registry<Service>();
registry.register("logger", {
    name: "LoggerService",
    execute: () => "Logging...",
});
registry.register("auth", {
    name: "AuthService",
    execute: () => "Authenticating...",
});

console.log(`\nRegistered services: ${registry.list().join(", ")}`);
console.log(registry.get("logger").execute());
console.log(registry.get("auth").execute());
```

---

## Mapped Types

> 🎯 **Teach:** How mapped types transform every property of an existing type to create new types automatically. **See:** `Immutable<T>`, `Nullable<T>`, and `StringProps<T>` applied to a User interface, producing readonly, nullable, and filtered variants. **Feel:** A sense of power from writing type-level transformations that keep derived types in sync with the source.

### Transforming Types Automatically

> 🎙️ Mapped types let you create new types by transforming every property of an existing type. Think of them as a for loop over an object's keys, but at the type level. Immutable takes any type and makes all its properties readonly. Nullable takes any type and makes every property accept null. StringProps uses a conditional filter to keep only the properties whose values are strings. These are not utility functions that transform data at runtime -- they are utility types that transform type shapes at compile time. This is type-level programming.

Create `src/advanced_types.ts`:

```typescript
// src/advanced_types.ts

// --- Mapped Types ---
// Create new types by transforming existing ones

interface User {
    id: number;
    name: string;
    email: string;
    isAdmin: boolean;
}

// Make all properties readonly
type Immutable<T> = { readonly [K in keyof T]: T[K] };

// Make all properties nullable
type Nullable<T> = { [K in keyof T]: T[K] | null };

// Pick only string properties
type StringProps<T> = {
    [K in keyof T as T[K] extends string ? K : never]: T[K];
};

type ImmutableUser = Immutable<User>;
type NullableUser = Nullable<User>;
type UserStrings = StringProps<User>; // { name: string; email: string }

const frozenUser: ImmutableUser = { id: 1, name: "Alice", email: "a@b.com", isAdmin: false };
// frozenUser.name = "Bob";  // Error: readonly

const nullableUser: NullableUser = { id: null, name: "Alice", email: null, isAdmin: null };

const userStrings: UserStrings = { name: "Alice", email: "alice@example.com" };

console.log("Immutable:", frozenUser);
console.log("Nullable:", nullableUser);
console.log("String props:", userStrings);
```

---

## Conditional Types

> 🎯 **Teach:** How conditional types use extends and infer to branch and extract types at the type level. **See:** `IsString<T>`, `ElementType<T>` extracting array element types, and `Unwrap<T>` extracting Promise resolved types. **Feel:** Understanding that conditional types are the if/else of the type system and power many built-in utility types.

### Types That Depend on a Condition

> 🎙️ Conditional types use a syntax that looks like the ternary operator, but at the type level. If type T extends some constraint, use one type; otherwise, use another. The infer keyword inside a conditional type lets you extract a type from inside another type. ElementType extracts the element type from an array. Unwrap extracts the resolved type from a Promise. These are the same mechanisms that power built-in utility types like ReturnType and Parameters.

Continuing in `src/advanced_types.ts`:

```typescript
// --- Conditional Types ---
// Types that depend on a condition

type IsString<T> = T extends string ? "yes" : "no";
type A = IsString<string>;    // "yes"
type B = IsString<number>;    // "no"

// Extract array element type
type ElementType<T> = T extends (infer E)[] ? E : never;

type NumElement = ElementType<number[]>;     // number
type StrElement = ElementType<string[]>;     // string

// Extract promise value type
type Unwrap<T> = T extends Promise<infer U> ? U : T;

type P1 = Unwrap<Promise<string>>;  // string
type P2 = Unwrap<number>;           // number

// Demonstrate at runtime
function checkTypes(): void {
    const a: A = "yes";
    const b: B = "no";
    console.log(`\nIsString<string> = ${a}`);
    console.log(`IsString<number> = ${b}`);
}
checkTypes();
```

---

## Template Literal Types

> 🎯 **Teach:** How template literal types combine union types to generate every possible string combination at the type level. **See:** `ColorVariant`, `Endpoint`, and `MouseEvent` types generated from unions, plus a `HandlerMap` that auto-generates event handler interfaces. **Feel:** Amazed that TypeScript can generate dozens of precise string types from a few lines of type-level code.

### Building String Types from Combinations

> 🎙️ Template literal types use the same backtick syntax as JavaScript template strings, but they operate at the type level. When you combine two union types inside a template literal type, TypeScript generates every possible combination. A Shade union with two values crossed with a Color union with three values produces six ColorVariant values. Combined with the Capitalize utility type, you can automatically generate event handler names from event names. The EventMap example shows how this works in practice: you define your events and their payload types, and a mapped type with template literals generates the complete handler interface automatically.

Continuing in `src/advanced_types.ts`:

```typescript
// --- Template Literal Types ---
type Color = "red" | "green" | "blue";
type Shade = "light" | "dark";

// Generates: "light-red" | "light-green" | "light-blue" | "dark-red" | ...
type ColorVariant = `${Shade}-${Color}`;

type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type ApiRoute = "/users" | "/posts";

// Generates: "GET /users" | "GET /posts" | "POST /users" | ...
type Endpoint = `${HttpMethod} ${ApiRoute}`;

// Event handler names from properties
type EventFor<T extends string> = `on${Capitalize<T>}`;
type MouseEvent = EventFor<"click" | "move" | "down" | "up">;
// "onClick" | "onMove" | "onDown" | "onUp"

const endpoint: Endpoint = "GET /users";
const color: ColorVariant = "dark-blue";
const event: MouseEvent = "onClick";

console.log(`\nEndpoint: ${endpoint}`);
console.log(`Color: ${color}`);
console.log(`Event: ${event}`);

// Practical: type-safe event emitter shape
type EventMap = {
    click: { x: number; y: number };
    keypress: { key: string };
    resize: { width: number; height: number };
};

type HandlerMap<T extends Record<string, any>> = {
    [K in keyof T as `on${Capitalize<string & K>}`]: (event: T[K]) => void;
};

type Handlers = HandlerMap<EventMap>;
// { onClick: (event: {x, y}) => void; onKeypress: ...; onResize: ... }

const handlers: Handlers = {
    onClick: (e) => console.log(`Clicked at (${e.x}, ${e.y})`),
    onKeypress: (e) => console.log(`Key: ${e.key}`),
    onResize: (e) => console.log(`Resized to ${e.width}x${e.height}`),
};

handlers.onClick({ x: 100, y: 200 });
handlers.onKeypress({ key: "Enter" });
handlers.onResize({ width: 1920, height: 1080 });
```

![Type-level programming: mapped types, conditional types, and template literal types transforming type shapes](../images/module-18/type-level-programming.png)
*Advanced types let TypeScript model complex relationships at the type level*

---

## Sharpen Your Pencil

> ✏️ Sharpen Your Pencil

1. Create `@log` and `@timed` decorators using the TC39 Stage 3 syntax. Apply them to a `MathService` class with `add`, `fibonacci`, and `multiply` methods. Stack both decorators on `multiply`.
2. Build a `RequestBuilder` class with a fluent API. Chain `.setMethod()`, `.setUrl()`, `.addHeader()`, `.setBody()`, and `.setTimeout()` calls. Call `.build()` and verify it throws when required fields are missing.
3. Implement a `Database` singleton with a private constructor and `getInstance()`. Verify that two calls to `getInstance()` return the same object. Build a generic `Registry<T>` that registers and retrieves named items.
4. Create mapped types `Immutable<T>`, `Nullable<T>`, and `StringProps<T>`. Apply them to a `User` interface and verify the transformed types work correctly.
5. Create conditional types `IsString<T>`, `ElementType<T>`, and `Unwrap<T>`. Test them with different type arguments.
6. Create template literal types `ColorVariant`, `Endpoint`, and `MouseEvent`. Build a `HandlerMap` that generates event handler interfaces from an `EventMap` type.

---

> 💡 **Remember this one thing:** Advanced types let TypeScript's type system model complex relationships that simpler types cannot express.

---

## Up Next

In **Module 19: Capstone Project**, you will bring everything together -- types, modules, testing, configuration, and patterns -- into a complete, well-structured TypeScript project built from scratch.
