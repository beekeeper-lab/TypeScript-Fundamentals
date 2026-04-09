# Module 13: Error Handling

> 🏷️ When You're Ready

> 🎯 **Teach:** How to build a custom error hierarchy with typed error classes, how the Result type pattern makes errors explicit in your type signatures, and how to handle errors gracefully in async code. **See:** Custom error classes with instanceof narrowing, the Result<T,E> discriminated union with Ok/Err helpers, mapResult and flatMapResult for chaining, and async retry with error accumulation. **Feel:** Conviction that errors are data — they deserve the same careful typing as your success paths.

> 🔄 **Where this fits:** You learned async/await in the previous module. Now you need to handle the reality that async operations fail — network errors, timeouts, validation failures. This module gives you two complementary strategies: exception-based error handling with custom classes, and the Result type pattern that makes errors visible in your function signatures.

## Custom Error Classes

> 🎯 **Teach:** How to build a custom error hierarchy with a base AppError class and specific subclasses (ValidationError, NotFoundError, etc.), and how instanceof narrowing lets you handle each error type differently in catch blocks. **See:** An error hierarchy with coded subclasses, a validateUser function that throws typed errors, a handleError function with instanceof narrowing, and try/catch/finally with resource cleanup. **Feel:** Control over your error paths — errors are no longer mystery strings but typed, structured data you can match on.

### Building an Error Hierarchy

> 🎙️ JavaScript's built-in Error class is generic — it just has a message and a stack trace. In a real application, you need to distinguish between different kinds of errors: validation failures, not-found errors, authentication errors, rate limits. The solution is a custom error hierarchy. You create a base AppError class that extends Error and adds a code property, then create specific error subclasses. This lets you use instanceof to narrow errors in your catch blocks, handling each kind differently.

```typescript
// Custom error hierarchy
class AppError extends Error {
    constructor(message: string, public code: string) {
        super(message);
        this.name = "AppError";
    }
}

class ValidationError extends AppError {
    constructor(public field: string, message: string) {
        super(message, "VALIDATION_ERROR");
        this.name = "ValidationError";
    }
}

class NotFoundError extends AppError {
    constructor(public resource: string, public resourceId: string | number) {
        super(`${resource} with id "${resourceId}" not found`, "NOT_FOUND");
        this.name = "NotFoundError";
    }
}

class AuthenticationError extends AppError {
    constructor(message: string = "Authentication required") {
        super(message, "AUTH_ERROR");
        this.name = "AuthenticationError";
    }
}

class RateLimitError extends AppError {
    constructor(public retryAfterMs: number) {
        super(`Rate limited. Retry after ${retryAfterMs}ms`, "RATE_LIMIT");
        this.name = "RateLimitError";
    }
}
```

![Error hierarchy — AppError at the top, with ValidationError, NotFoundError, AuthenticationError, and RateLimitError branching below](../images/module-13/error-hierarchy.png)
*Error hierarchy — AppError at the top, with specialized subclasses for each error category*

### Throwing and Catching Typed Errors

> 🎙️ Once you have your error hierarchy, you throw specific error types from your functions and catch them with instanceof narrowing. The catch block receives an unknown type — TypeScript does not know what was thrown. You narrow it step by step: is it a ValidationError? A NotFoundError? An AuthenticationError? Each instanceof check gives you access to that error's specific properties. The finally block runs regardless of whether an error occurred, making it the right place for cleanup like closing database connections.

```typescript
// Function that throws typed errors
function validateUser(data: { name?: string; email?: string; age?: number }): void {
    if (!data.name || data.name.trim().length === 0) {
        throw new ValidationError("name", "Name is required");
    }
    if (!data.email || !data.email.includes("@")) {
        throw new ValidationError("email", "Valid email is required");
    }
    if (data.age !== undefined && (data.age < 0 || data.age > 150)) {
        throw new ValidationError("age", "Age must be between 0 and 150");
    }
}

// Catching specific error types
function handleError(err: unknown): void {
    if (err instanceof ValidationError) {
        console.log(`  Validation failed on "${err.field}": ${err.message}`);
    } else if (err instanceof NotFoundError) {
        console.log(`  Not found: ${err.resource} #${err.resourceId}`);
    } else if (err instanceof AuthenticationError) {
        console.log(`  Auth error: ${err.message}`);
    } else if (err instanceof RateLimitError) {
        console.log(`  Rate limited — retry after ${err.retryAfterMs}ms`);
    } else if (err instanceof Error) {
        console.log(`  Unknown error: ${err.message}`);
    } else {
        console.log(`  Non-error thrown: ${err}`);
    }
}

// Test each error type
console.log("=== Validation Errors ===");
const testCases = [
    { name: "", email: "test@test.com" },
    { name: "Alice", email: "invalid" },
    { name: "Bob", email: "bob@test.com", age: -5 },
    { name: "Carol", email: "carol@test.com", age: 25 },
];

for (const data of testCases) {
    try {
        validateUser(data);
        console.log(`  Valid: ${data.name}`);
    } catch (err) {
        handleError(err);
    }
}
```

### try/catch/finally with Resource Cleanup

```typescript
// try/catch/finally with resource cleanup
console.log("\n=== Resource Cleanup ===");
class DatabaseConnection {
    connected = false;

    connect(): void {
        this.connected = true;
        console.log("  DB: Connected");
    }

    query(sql: string): string[] {
        if (!this.connected) throw new Error("Not connected");
        if (sql.includes("DROP")) throw new AppError("Destructive queries not allowed", "FORBIDDEN");
        return ["row1", "row2", "row3"];
    }

    close(): void {
        this.connected = false;
        console.log("  DB: Connection closed");
    }
}

function runQuery(sql: string): void {
    const db = new DatabaseConnection();
    try {
        db.connect();
        const results = db.query(sql);
        console.log(`  Query returned ${results.length} rows`);
    } catch (err) {
        handleError(err);
    } finally {
        db.close(); // Always close the connection
    }
}

runQuery("SELECT * FROM users");
runQuery("DROP TABLE users");
```

---

## The Result Type Pattern

> 🎯 **Teach:** How the Result<T,E> discriminated union makes error paths explicit in function signatures instead of hiding them behind invisible throw statements, and how Ok/Err helpers, mapResult, flatMapResult, and collectResults enable safe chaining. **See:** A generic Result type with Ok and Err constructors, parseInt_ and clamp returning Results, a parseAge pipeline, a createUser chain, and a collectResults utility. **Feel:** Conviction that making errors visible in types is worth the extra verbosity — you will never accidentally ignore an error path again.

### Result<T,E> as a Discriminated Union

> 🎙️ Exceptions have a problem: they are invisible in your type signatures. A function that says it returns a number might actually throw three different kinds of errors, and the caller has no way to know that from the type alone. The Result type pattern solves this. Instead of throwing, your function returns a discriminated union: either an Ok variant with a value, or an Err variant with an error. The caller must check which variant they got before they can access the data. This makes error paths explicit and impossible to ignore.

```typescript
// Generic Result type
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

// Helper functions to create Results
function Ok<T>(value: T): Result<T, never> {
    return { ok: true, value };
}

function Err<E>(error: E): Result<never, E> {
    return { ok: false, error };
}
```

### Typed Error Variants with Result

```typescript
// Typed error variants
type ParseError = { kind: "parse"; message: string; line: number };
type RangeError_ = { kind: "range"; message: string; min: number; max: number; actual: number };
type FormatError = { kind: "format"; message: string; expected: string; got: string };
type AppError = ParseError | RangeError_ | FormatError;

// Functions that return Result instead of throwing
function parseInt_(input: string): Result<number, AppError> {
    const num = Number(input);
    if (isNaN(num)) {
        return Err({ kind: "parse", message: `Cannot parse "${input}" as number`, line: 0 });
    }
    if (!Number.isInteger(num)) {
        return Err({ kind: "format", message: "Expected integer", expected: "integer", got: "float" });
    }
    return Ok(num);
}

function clamp(value: number, min: number, max: number): Result<number, AppError> {
    if (value < min || value > max) {
        return Err({ kind: "range", message: `${value} out of range`, min, max, actual: value });
    }
    return Ok(value);
}
```

### Chaining Results

> 🎙️ When you have multiple Result-returning functions that depend on each other, you chain them manually. Call the first function, check if it is Ok, then pass the value to the next function. If any step fails, you return the error immediately. This is more verbose than exception-based code, but every error path is visible and every success path is type-checked. You can also write mapResult and flatMapResult helper functions to make the chaining more concise.

```typescript
// Chaining Results
function parseAge(input: string): Result<number, AppError> {
    const parsed = parseInt_(input);
    if (!parsed.ok) return parsed;
    return clamp(parsed.value, 0, 150);
}

// Using Result types
console.log("=== Result Type ===");
const ageTests = ["25", "abc", "3.14", "-5", "200", "30"];

for (const input of ageTests) {
    const result = parseAge(input);
    if (result.ok) {
        console.log(`  "${input}" -> age: ${result.value}`);
    } else {
        console.log(`  "${input}" -> error [${result.error.kind}]: ${result.error.message}`);
    }
}
```

### mapResult and flatMapResult

```typescript
// Map and flatMap for Result
function mapResult<T, U, E>(result: Result<T, E>, fn: (value: T) => U): Result<U, E> {
    if (result.ok) return Ok(fn(result.value));
    return result;
}

function flatMapResult<T, U, E>(result: Result<T, E>, fn: (value: T) => Result<U, E>): Result<U, E> {
    if (result.ok) return fn(result.value);
    return result;
}
```

### Building a Pipeline with Result

```typescript
// Pipeline using Result
console.log("\n=== Result Pipeline ===");
type User = { name: string; age: number; category: string };

function categorizeAge(age: number): Result<string, AppError> {
    if (age < 13) return Ok("child");
    if (age < 18) return Ok("teen");
    if (age < 65) return Ok("adult");
    return Ok("senior");
}

function createUser(name: string, ageStr: string): Result<User, AppError> {
    const ageResult = parseAge(ageStr);
    if (!ageResult.ok) return ageResult;

    const categoryResult = categorizeAge(ageResult.value);
    if (!categoryResult.ok) return categoryResult;

    return Ok({ name, age: ageResult.value, category: categoryResult.value });
}

const userTests: [string, string][] = [
    ["Alice", "25"],
    ["Bob", "abc"],
    ["Carol", "8"],
    ["Dave", "70"],
];

for (const [name, age] of userTests) {
    const result = createUser(name, age);
    if (result.ok) {
        const user = result.value;
        console.log(`  ${user.name}: age ${user.age} (${user.category})`);
    } else {
        console.log(`  ${name}: error — ${result.error.message}`);
    }
}
```

### Collecting Results

```typescript
// Collecting Results
function collectResults<T, E>(results: Result<T, E>[]): Result<T[], E> {
    const values: T[] = [];
    for (const r of results) {
        if (!r.ok) return r;
        values.push(r.value);
    }
    return Ok(values);
}

console.log("\n=== Collecting Results ===");
const allParsed = collectResults(["1", "2", "3", "4"].map(parseInt_));
if (allParsed.ok) {
    console.log(`  All parsed: [${allParsed.value.join(", ")}]`);
}

const someFailed = collectResults(["1", "two", "3"].map(parseInt_));
if (!someFailed.ok) {
    console.log(`  Collection failed: ${someFailed.error.message}`);
}
```

---

## Async Error Handling with Result

> 🎯 **Teach:** How to combine the Result type with async/await so that async functions return Promise<Result<T,E>> instead of throwing, and how tryCatchToResult bridges exception-based libraries into the Result world. **See:** NetworkError and TimeoutError classes, a safeFetch returning Result, a tryCatchToResult wrapper, retry with error accumulation, Promise.allSettled with error categorization, and async cleanup with finally. **Feel:** Mastery of two complementary error strategies — exceptions for boundaries you do not control, Result for code you own.

### Custom Errors for Async Operations

> 🎙️ The Result type pattern works beautifully with async code. Instead of an async function that might throw, you write an async function that returns a Promise of Result. The caller awaits the Promise and then checks the ok field — no try/catch needed. You can also write a tryCatchToResult wrapper that takes any async function and converts its success or thrown error into a Result. This lets you gradually adopt the Result pattern even when you are working with libraries that throw exceptions.

```typescript
// Re-use Result type
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

function Ok<T>(value: T): Result<T, never> { return { ok: true, value }; }
function Err<E>(error: E): Result<never, E> { return { ok: false, error }; }

// Custom errors for async operations
class NetworkError extends Error {
    constructor(public url: string, public statusCode: number) {
        super(`Request to ${url} failed with status ${statusCode}`);
        this.name = "NetworkError";
    }
}

class TimeoutError extends Error {
    constructor(public url: string, public timeoutMs: number) {
        super(`Request to ${url} timed out after ${timeoutMs}ms`);
        this.name = "TimeoutError";
    }
}
```

### Async Functions Returning Result

```typescript
// Async function returning Result
async function safeFetch<T>(url: string, mockData: T, shouldFail = false): Promise<Result<T, NetworkError>> {
    await new Promise(resolve => setTimeout(resolve, 50));
    if (shouldFail) {
        return Err(new NetworkError(url, 500));
    }
    return Ok(mockData);
}

// Wrapping async try/catch into Result
async function tryCatchToResult<T>(fn: () => Promise<T>): Promise<Result<T, Error>> {
    try {
        return Ok(await fn());
    } catch (err) {
        return Err(err instanceof Error ? err : new Error(String(err)));
    }
}
```

### Retry with Error Accumulation

> 🎙️ When retrying async operations, you sometimes want to know about every failure, not just the last one. The fetchWithRetry function accumulates errors from each attempt. If any attempt succeeds, it returns the result. If all attempts fail, it returns an array of all the errors. This gives the caller full visibility into what went wrong across every retry.

```typescript
// Async with retry and error accumulation
async function fetchWithRetry<T>(
    fn: () => Promise<Result<T, Error>>,
    retries: number = 3
): Promise<Result<T, Error[]>> {
    const errors: Error[] = [];
    for (let i = 0; i < retries; i++) {
        const result = await fn();
        if (result.ok) return Ok(result.value);
        errors.push(result.error);
        console.log(`    Retry ${i + 1}: ${result.error.message}`);
    }
    return Err(errors);
}

async function main() {
    // Async error handling with specific error types
    console.log("=== Async Error Types ===");

    const result1 = await safeFetch("/api/users", [{ id: 1, name: "Alice" }]);
    if (result1.ok) console.log(`  Users: ${result1.value.length}`);

    const result2 = await safeFetch("/api/broken", null, true);
    if (!result2.ok) console.log(`  Error: ${result2.error.message} (status: ${result2.error.statusCode})`);

    // Promise.allSettled with error categorization
    console.log("\n=== Categorized Async Errors ===");
    const fetches = await Promise.allSettled([
        safeFetch("/api/a", "data-a"),
        safeFetch("/api/b", "data-b", true),
        safeFetch("/api/c", "data-c"),
        safeFetch("/api/d", "data-d", true),
    ]);

    const successes: string[] = [];
    const failures: string[] = [];

    for (const result of fetches) {
        if (result.status === "fulfilled") {
            if (result.value.ok) successes.push(result.value.value);
            else failures.push(result.value.error.message);
        }
    }

    console.log(`  Successes: ${successes.length} — ${successes.join(", ")}`);
    console.log(`  Failures: ${failures.length}`);

    // Retry pattern with error accumulation
    console.log("\n=== Retry with Error Accumulation ===");
    let attempt = 0;
    const retryResult = await fetchWithRetry(async () => {
        attempt++;
        if (attempt < 3) return Err(new Error(`Attempt ${attempt} failed`));
        return Ok("Finally succeeded!");
    });

    if (retryResult.ok) {
        console.log(`  ${retryResult.value}`);
    } else {
        console.log(`  All retries failed (${retryResult.error.length} errors)`);
    }

    // tryCatchToResult wrapper
    console.log("\n=== tryCatchToResult Wrapper ===");
    const wrapped1 = await tryCatchToResult(async () => {
        return JSON.parse('{"name": "Alice"}');
    });
    if (wrapped1.ok) console.log(`  Parsed: ${wrapped1.value.name}`);

    const wrapped2 = await tryCatchToResult(async () => {
        return JSON.parse("not json{{{");
    });
    if (!wrapped2.ok) console.log(`  Parse error: ${wrapped2.error.message}`);

    // Cleanup with finally in async
    console.log("\n=== Async Cleanup ===");
    class Connection {
        open = false;
        async connect() { this.open = true; console.log("  Connection opened"); }
        async close() { this.open = false; console.log("  Connection closed"); }
        async execute(query: string): Promise<string[]> {
            if (!this.open) throw new Error("Connection closed");
            await new Promise(resolve => setTimeout(resolve, 30));
            return ["result1", "result2"];
        }
    }

    const conn = new Connection();
    try {
        await conn.connect();
        const rows = await conn.execute("SELECT * FROM data");
        console.log(`  Got ${rows.length} rows`);
    } catch (err) {
        console.log(`  Query error: ${(err as Error).message}`);
    } finally {
        await conn.close();
    }
}

main();
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to extend both error handling strategies — adding new error subclasses, writing Result-returning validators, chaining with flatMapResult, wrapping try/catch as Result, and implementing exponential backoff. **See:** Five exercises covering PermissionError, parseEmail with Result, flatMapResult pipelines, tryCatchToResult for JSON.parse, and retry with exponential backoff. **Feel:** Readiness to design error handling for a real application using whichever strategy fits each situation.

> ✏️ Sharpen Your Pencil

1. Add a new error class `PermissionError` to the error hierarchy with a `requiredRole` property. Add a case for it in `handleError`. Throw it from a new function and verify it gets caught correctly.
2. Write a `parseEmail(input: string): Result<string, AppError>` function that validates an email format and returns `Ok` with the email or `Err` with a `FormatError`. Chain it with `parseAge` to create a validated user.
3. Use `flatMapResult` to rewrite the `createUser` pipeline so each step chains without explicit `if (!result.ok)` checks.
4. Write an async function that uses `tryCatchToResult` to wrap `JSON.parse` on three different inputs (valid JSON, invalid JSON, empty string) and log the Result for each.
5. Modify `fetchWithRetry` to accept a `delayBetweenRetries` parameter that increases with each attempt (exponential backoff). Test it with a function that succeeds on the third attempt.

---

> 💡 **Remember this one thing:** The Result type pattern makes errors explicit in your type signatures — no more hidden throw paths.

---

## Up Next

> 🎯 **Teach:** Where the learning journey goes from here. **See:** A preview of Module 14 covering JSON parsing, type guards for external data, and schema validation systems. **Feel:** Momentum — you can handle errors gracefully, and now you will defend the boundary where untyped external data enters your typed code.

In **Module 14: JSON and APIs**, you will learn how to safely parse JSON, validate external data with type guards, and build a schema validation system that catches bad data at the boundary between your typed code and the untyped outside world.
