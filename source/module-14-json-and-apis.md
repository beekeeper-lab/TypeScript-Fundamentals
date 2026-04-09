# Module 14: JSON and APIs

> 🏷️ When You're Ready

> 🎯 **Teach:** How to safely serialize and deserialize JSON in TypeScript, how to build type guard functions that validate external data at runtime, and how to construct a schema validation system for typed API responses. **See:** JSON.stringify with replacers, JSON.parse with revivers, type guard functions for User and Post types, a composable schema validator (string_, number_, object_, array_), and a typed fetch wrapper with safe error handling. **Feel:** A healthy distrust of external data and the discipline to always validate at the boundary.

> 🔄 **Where this fits:** You have learned error handling and the Result type pattern. Now you face the most common source of runtime errors in real applications: data that comes from outside your program — API responses, JSON files, user input. This module teaches you to defend the boundary between your typed code and the untyped outside world.

## JSON Basics

> 🎯 **Teach:** How JSON.stringify serializes typed values (with replacers for filtering and toJSON for custom serialization) and how JSON.parse deserializes them (with revivers for restoring types like Date that JSON cannot represent natively). **See:** Typed stringify with indentation, a replacer that redacts sensitive fields, a class with a custom toJSON method, and a reviver that converts ISO strings back into Date objects. **Feel:** Awareness that serialization is a lossy process — JSON strips types, and it is your job to restore them.

### JSON.stringify with Types

> 🎙️ JSON dot stringify converts a JavaScript value into a JSON string. TypeScript does not change how stringify works at runtime, but it ensures the value you pass in is a valid type. The second argument is a replacer — a function that lets you transform or filter values during serialization. This is useful for redacting sensitive fields like passwords or API keys. The third argument controls formatting — pass a number for indentation or a string for a custom indent character.

```typescript
// JSON.stringify with types
type Config = {
    host: string;
    port: number;
    debug: boolean;
    tags: string[];
    database: {
        name: string;
        pool: number;
    };
};

const config: Config = {
    host: "localhost",
    port: 3000,
    debug: true,
    tags: ["api", "v2"],
    database: { name: "mydb", pool: 5 },
};

// Serialize
const json = JSON.stringify(config, null, 2);
console.log("=== Serialized ===");
console.log(json);

// Deserialize with type assertion
const parsed = JSON.parse(json) as Config;
console.log(`\nHost: ${parsed.host}, Port: ${parsed.port}`);
console.log(`DB: ${parsed.database.name}, Pool: ${parsed.database.pool}`);
```

### Replacer Functions — Filtering Sensitive Fields

```typescript
// JSON.stringify replacer — filter sensitive fields
type UserRecord = {
    id: number;
    name: string;
    email: string;
    password: string;
    apiKey: string;
};

const user: UserRecord = {
    id: 1,
    name: "Alice",
    email: "alice@example.com",
    password: "secret123",
    apiKey: "sk-abc123xyz",
};

const sensitiveFields = new Set(["password", "apiKey"]);
const safeJson = JSON.stringify(user, (key, value) => {
    if (sensitiveFields.has(key)) return "[REDACTED]";
    return value;
}, 2);

console.log("\n=== Redacted Output ===");
console.log(safeJson);
```

### Custom toJSON Methods

```typescript
// JSON.stringify with toJSON method
class DateRange {
    constructor(public start: Date, public end: Date) {}

    toJSON() {
        return {
            start: this.start.toISOString(),
            end: this.end.toISOString(),
            durationMs: this.end.getTime() - this.start.getTime(),
        };
    }
}

const range = new DateRange(new Date("2025-01-01"), new Date("2025-12-31"));
console.log("\n=== Custom toJSON ===");
console.log(JSON.stringify(range, null, 2));
```

### Reviver Functions — Restoring Types from JSON

> 🎙️ JSON dot parse returns any — it has no idea what types the data should be. A type assertion like "as Config" tells TypeScript to trust you, but it performs no runtime check. For simple cases where you control the data source, that is fine. But you can also pass a reviver function as the second argument to JSON.parse. The reviver runs on every key-value pair and lets you transform values — for example, converting date strings back into Date objects. This is how you restore types that JSON cannot represent natively.

```typescript
// JSON.parse reviver — restore Date objects
const eventJson = '{"name": "Conference", "date": "2025-06-15T09:00:00.000Z", "attendees": 200}';

const event = JSON.parse(eventJson, (key, value) => {
    if (key === "date" && typeof value === "string") {
        return new Date(value);
    }
    return value;
}) as { name: string; date: Date; attendees: number };

console.log(`\n${event.name} on ${event.date.toLocaleDateString()} (${event.attendees} attendees)`);
console.log(`date is Date instance: ${event.date instanceof Date}`);
```

---

## Type Guards for External Data

> 🎯 **Teach:** Why type assertions (`as User`) are dangerous for external data and how type guard functions validate unknown data at runtime before narrowing it to a specific type. **See:** isObject, isUser, isPost, and isArrayOf type guards, plus a safeParse function that combines JSON.parse with a type guard into a single validated operation. **Feel:** Healthy distrust of any data that comes from outside your program — a type assertion is a lie unless you verify it first.

### The Problem with External Data

> 🎙️ Here is the core problem: when data comes from an API, a file, or any external source, it arrives as an unknown blob. A type assertion like "as User" silences the compiler, but if the data does not actually match the User shape, your code will crash later in a confusing way — accessing a property that does not exist, calling a method on undefined. The solution is type guard functions that check the data at runtime and narrow it to the expected type only if it actually matches. This is the boundary between the untyped outside world and your typed code.

```typescript
// Define API types
type User = {
    id: number;
    name: string;
    email: string;
    role: "admin" | "user" | "guest";
};

type Post = {
    id: number;
    title: string;
    body: string;
    authorId: number;
    tags: string[];
    published: boolean;
};

type ApiError = {
    error: string;
    code: number;
    details?: string;
};

type ApiResponse<T> = { success: true; data: T } | { success: false; error: ApiError };
```

### Writing Type Guard Functions

```typescript
// Type guard functions for external data
function isObject(value: unknown): value is Record<string, unknown> {
    return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isUser(value: unknown): value is User {
    if (!isObject(value)) return false;
    return (
        typeof value.id === "number" &&
        typeof value.name === "string" &&
        typeof value.email === "string" &&
        (value.role === "admin" || value.role === "user" || value.role === "guest")
    );
}

function isPost(value: unknown): value is Post {
    if (!isObject(value)) return false;
    return (
        typeof value.id === "number" &&
        typeof value.title === "string" &&
        typeof value.body === "string" &&
        typeof value.authorId === "number" &&
        Array.isArray(value.tags) && value.tags.every(t => typeof t === "string") &&
        typeof value.published === "boolean"
    );
}

function isArrayOf<T>(value: unknown, guard: (item: unknown) => item is T): value is T[] {
    return Array.isArray(value) && value.every(guard);
}
```

### Safe Parse with Validation

> 🎙️ The safeParse function combines JSON.parse with a type guard into a single operation. It tries to parse the JSON string, then runs the type guard on the result. If both succeed, you get back a success response with typed data. If the JSON is malformed or the data does not match the guard, you get back an error response. This is the pattern you should use for every piece of external data that enters your application.

```typescript
// Simulated API responses (raw JSON strings, as if from a network call)
const rawUserJson = '{"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"}';
const rawPostJson = '{"id": 10, "title": "Hello World", "body": "First post content", "authorId": 1, "tags": ["intro", "hello"], "published": true}';
const rawBadJson = '{"id": "not-a-number", "name": 42}';
const rawUsersJson = '[{"id": 1, "name": "Alice", "email": "a@b.com", "role": "admin"}, {"id": 2, "name": "Bob", "email": "b@c.com", "role": "user"}]';

// Safe parse function
function safeParse<T>(json: string, guard: (value: unknown) => value is T): ApiResponse<T> {
    try {
        const parsed: unknown = JSON.parse(json);
        if (guard(parsed)) {
            return { success: true, data: parsed };
        }
        return { success: false, error: { error: "Validation failed", code: 422, details: "Data does not match expected shape" } };
    } catch {
        return { success: false, error: { error: "Parse error", code: 400, details: "Invalid JSON" } };
    }
}

// Test the type guards
console.log("=== Type Guard Validation ===");

const userResult = safeParse(rawUserJson, isUser);
if (userResult.success) {
    console.log(`Valid user: ${userResult.data.name} (${userResult.data.role})`);
} else {
    console.log(`Invalid: ${userResult.error.details}`);
}

const postResult = safeParse(rawPostJson, isPost);
if (postResult.success) {
    console.log(`Valid post: "${postResult.data.title}" by author #${postResult.data.authorId}`);
}

const badResult = safeParse(rawBadJson, isUser);
if (!badResult.success) {
    console.log(`Rejected bad data: ${badResult.error.details}`);
}

const usersResult = safeParse(rawUsersJson, (v): v is User[] => isArrayOf(v, isUser));
if (usersResult.success) {
    console.log(`Valid user array: ${usersResult.data.map(u => u.name).join(", ")}`);
}

// Parse completely invalid JSON
const invalidResult = safeParse("{broken json!!", isUser);
if (!invalidResult.success) {
    console.log(`JSON error: ${invalidResult.error.error}`);
}
```

---

## Schema Validation System

> 🎯 **Teach:** How to build a composable schema validation system with primitive validators (string_, number_, boolean_) and combinators (array_, object_) that infer types automatically from the schema definition. **See:** Validator<T> type with parse and safeParse methods, primitive validators, array_ and object_ combinators, and schema definitions for User and Post whose TypeScript types are inferred via ReturnType. **Feel:** Elegance — instead of writing types and validators separately, the schema is the single source of truth for both.

### Building a Composable Validator

> 🎙️ Writing individual type guard functions for every type gets tedious. A better approach is to build a composable schema validator — a set of small validator functions that you can combine to describe any shape. You create validators for primitives like string and number, then combinators for array and object that accept inner validators. The object combinator takes a shape definition — a record of field names to validators — and returns a validator for the whole object. The resulting type is inferred automatically from the schema, so you never have to write the type and the validator separately.

```typescript
// Schema validator builder (zod-style, simplified)
type Validator<T> = {
    parse: (value: unknown) => T;
    safeParse: (value: unknown) => { success: true; data: T } | { success: false; error: string };
};

function string_(): Validator<string> {
    return {
        parse(value) {
            if (typeof value !== "string") throw new Error(`Expected string, got ${typeof value}`);
            return value;
        },
        safeParse(value) {
            if (typeof value !== "string") return { success: false, error: `Expected string, got ${typeof value}` };
            return { success: true, data: value };
        },
    };
}

function number_(): Validator<number> {
    return {
        parse(value) {
            if (typeof value !== "number") throw new Error(`Expected number, got ${typeof value}`);
            return value;
        },
        safeParse(value) {
            if (typeof value !== "number") return { success: false, error: `Expected number, got ${typeof value}` };
            return { success: true, data: value };
        },
    };
}

function boolean_(): Validator<boolean> {
    return {
        parse(value) {
            if (typeof value !== "boolean") throw new Error(`Expected boolean, got ${typeof value}`);
            return value;
        },
        safeParse(value) {
            if (typeof value !== "boolean") return { success: false, error: `Expected boolean, got ${typeof value}` };
            return { success: true, data: value };
        },
    };
}
```

### Array and Object Combinators

```typescript
function array_<T>(itemValidator: Validator<T>): Validator<T[]> {
    return {
        parse(value) {
            if (!Array.isArray(value)) throw new Error("Expected array");
            return value.map(item => itemValidator.parse(item));
        },
        safeParse(value) {
            if (!Array.isArray(value)) return { success: false, error: "Expected array" };
            const results: T[] = [];
            for (let i = 0; i < value.length; i++) {
                const r = itemValidator.safeParse(value[i]);
                if (!r.success) return { success: false, error: `[${i}]: ${r.error}` };
                results.push(r.data);
            }
            return { success: true, data: results };
        },
    };
}

function object_<T extends Record<string, Validator<any>>>(
    shape: T
): Validator<{ [K in keyof T]: T[K] extends Validator<infer U> ? U : never }> {
    type Result = { [K in keyof T]: T[K] extends Validator<infer U> ? U : never };
    return {
        parse(value) {
            if (typeof value !== "object" || value === null) throw new Error("Expected object");
            const result: any = {};
            for (const [key, validator] of Object.entries(shape)) {
                result[key] = validator.parse((value as any)[key]);
            }
            return result as Result;
        },
        safeParse(value) {
            if (typeof value !== "object" || value === null) return { success: false, error: "Expected object" };
            const result: any = {};
            for (const [key, validator] of Object.entries(shape)) {
                const r = validator.safeParse((value as any)[key]);
                if (!r.success) return { success: false, error: `${key}: ${r.error}` };
                result[key] = r.data;
            }
            return { success: true, data: result as Result };
        },
    };
}
```

### Defining Schemas and Inferring Types

```typescript
// Define schemas
const UserSchema = object_({
    id: number_(),
    name: string_(),
    email: string_(),
    active: boolean_(),
});

const PostSchema = object_({
    id: number_(),
    title: string_(),
    body: string_(),
    authorId: number_(),
    tags: array_(string_()),
});

// Type is inferred from the schema
type User = ReturnType<typeof UserSchema.parse>;
type Post = ReturnType<typeof PostSchema.parse>;
```

---

## Typed Fetch Wrapper

> 🎯 **Teach:** How to build a typed fetch wrapper that combines HTTP requests with schema validation so external API data enters your application fully validated, and how a safe variant returns a Result instead of throwing. **See:** A mockFetch that simulates network responses, typedFetch that validates with a schema, safeTypedFetch that returns Result<T>, and parallel typed fetching with Promise.all. **Feel:** The full boundary defense pattern in action — untyped data goes in, validated typed data comes out, and every failure is handled gracefully.

### Simulated Fetch with Validation

> 🎙️ In a real application, you call fetch to get data from an API. The response dot json method returns a Promise of any — completely untyped. A typed fetch wrapper combines the HTTP request with schema validation in a single function. You pass the URL and a validator, and it handles the request, checks the HTTP status, parses the JSON, validates the shape, and returns a typed value. If anything goes wrong at any step, you get a clear error. This is the boundary defense pattern in action: external data enters untyped and exits fully validated.

```typescript
// Simulated fetch that returns raw JSON
async function mockFetch(url: string): Promise<{ ok: boolean; status: number; json: () => Promise<unknown> }> {
    const mockData: Record<string, unknown> = {
        "/api/users/1": { id: 1, name: "Alice", email: "alice@example.com", active: true },
        "/api/users/2": { id: 2, name: "Bob", email: "bob@example.com", active: false },
        "/api/posts": [
            { id: 1, title: "Hello TypeScript", body: "TS is great", authorId: 1, tags: ["ts", "intro"] },
            { id: 2, title: "Advanced Types", body: "Generics and more", authorId: 1, tags: ["ts", "advanced"] },
        ],
        "/api/bad": { id: "not-a-number", garbage: true },
    };

    await new Promise(resolve => setTimeout(resolve, 50));
    const data = mockData[url];
    if (data === undefined) {
        return { ok: false, status: 404, json: async () => ({ error: "Not found" }) };
    }
    return { ok: true, status: 200, json: async () => data };
}

// Typed fetch wrapper
async function typedFetch<T>(url: string, validator: Validator<T>): Promise<T> {
    const response = await mockFetch(url);
    if (!response.ok) {
        throw new Error(`HTTP ${response.status} for ${url}`);
    }
    const raw = await response.json();
    return validator.parse(raw); // Throws if validation fails
}
```

### Safe Typed Fetch with Result

```typescript
// Safe typed fetch returning a Result
type Result<T> = { ok: true; value: T } | { ok: false; error: string };

async function safeTypedFetch<T>(url: string, validator: Validator<T>): Promise<Result<T>> {
    try {
        const response = await mockFetch(url);
        if (!response.ok) return { ok: false, error: `HTTP ${response.status}` };
        const raw = await response.json();
        const result = validator.safeParse(raw);
        if (!result.success) return { ok: false, error: result.error };
        return { ok: true, value: result.data };
    } catch (err) {
        return { ok: false, error: (err as Error).message };
    }
}
```

### Using the Typed Fetch Wrapper

```typescript
async function main() {
    // Schema validation
    console.log("=== Schema Validation ===");
    const goodUser = UserSchema.safeParse({ id: 1, name: "Alice", email: "a@b.com", active: true });
    if (goodUser.success) console.log(`Valid: ${goodUser.data.name}`);

    const badUser = UserSchema.safeParse({ id: "string-id", name: 42 });
    if (!badUser.success) console.log(`Invalid: ${badUser.error}`);

    // Typed fetch
    console.log("\n=== Typed Fetch ===");
    const user = await typedFetch("/api/users/1", UserSchema);
    console.log(`Fetched user: ${user.name} (active: ${user.active})`);

    const posts = await typedFetch("/api/posts", array_(PostSchema));
    console.log(`Fetched ${posts.length} posts:`);
    for (const post of posts) {
        console.log(`  "${post.title}" [${post.tags.join(", ")}]`);
    }

    // Safe fetch — handles errors gracefully
    console.log("\n=== Safe Typed Fetch ===");
    const result1 = await safeTypedFetch("/api/users/2", UserSchema);
    if (result1.ok) console.log(`User: ${result1.value.name}`);

    const result2 = await safeTypedFetch("/api/not-found", UserSchema);
    if (!result2.ok) console.log(`Error: ${result2.error}`);

    const result3 = await safeTypedFetch("/api/bad", UserSchema);
    if (!result3.ok) console.log(`Validation error: ${result3.error}`);

    // Parallel typed fetch
    console.log("\n=== Parallel Typed Fetch ===");
    const [u1, u2] = await Promise.all([
        safeTypedFetch("/api/users/1", UserSchema),
        safeTypedFetch("/api/users/2", UserSchema),
    ]);

    if (u1.ok && u2.ok) {
        console.log(`Users: ${u1.value.name}, ${u2.value.name}`);
    }
}

main();
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to apply JSON serialization, type guards, and schema validation in your own code through focused practice. **See:** Five exercises covering custom replacer/reviver functions, a Product type guard, an optional_ schema combinator, and a parallel fetchAll utility returning Results. **Feel:** Confidence that you can defend the boundary between your typed code and any external data source.

> ✏️ Sharpen Your Pencil

1. Write a replacer function for `JSON.stringify` that converts all Date values to ISO strings and all `undefined` values to `null`. Test it with an object containing nested Dates.
2. Write a reviver function for `JSON.parse` that detects ISO date strings (matching `/^\d{4}-\d{2}-\d{2}T/`) and converts them back to Date objects automatically.
3. Write a type guard `isProduct(value: unknown): value is Product` for a Product type with fields `sku: string`, `name: string`, `price: number`, `inStock: boolean`. Test it with both valid and invalid JSON.
4. Add an `optional_<T>(validator: Validator<T>): Validator<T | undefined>` combinator to the schema system that passes if the value is undefined or if it passes the inner validator. Use it to define a schema with optional fields.
5. Write a `fetchAll<T>(urls: string[], validator: Validator<T>): Promise<Result<T>[]>` function that fetches multiple URLs in parallel using `safeTypedFetch` and returns an array of Results.

---

> 💡 **Remember this one thing:** Never trust external data — always validate JSON from APIs with type guards before using it as a typed value.

---

## Up Next

> 🎯 **Teach:** Where the learning journey goes from here. **See:** A preview of Module 15 covering npm, package.json, and type declarations for third-party libraries. **Feel:** Momentum — you can validate external data, and now you will learn to manage the ecosystem of packages that real projects depend on.

In **Module 15: npm and Package Management**, you will learn how to use npm to manage dependencies, understand package.json and lock files, and work with type declarations for third-party libraries.
