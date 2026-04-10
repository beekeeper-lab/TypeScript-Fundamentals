# Module 10: Type Narrowing

> 🏷️ When You're Ready

> 🎯 **Teach:** How TypeScript eliminates impossible types as you add runtime checks, narrowing a broad union into a specific type inside each branch. **See:** typeof guards, instanceof checks, the `in` operator, discriminated unions, custom type guards, exhaustive checks, and assertion functions — all in working code. **Feel:** Confidence that TypeScript is watching your back, turning every `if` and `switch` into a proof that the data is what you think it is.

> 🔄 **Where this fits:** You have learned union types, interfaces, and classes. Type narrowing is the bridge between runtime checks and compile-time safety — it is how TypeScript understands the control flow you already write and rewards you with tighter types inside each branch.

## What Is Type Narrowing?

> 🎯 **Teach:** That TypeScript automatically refines a broad union type into a specific type inside conditional branches based on your runtime checks. **See:** A simple function where typeof narrows `string | number` into each branch, and a diagram of the narrowing funnel. **Feel:** An "aha" moment that your if-statements are doing double duty — runtime logic and compile-time proof.

### TypeScript Eliminates Types As You Check Them

> 🎙️ When you have a variable whose type is a union — say, string or number — TypeScript does not know which one it is. But the moment you write an if-check like typeof value equals string, TypeScript narrows the type inside that block to just string. The broad union gets refined into a specific type. This is called type narrowing, and it happens automatically based on your control flow. Every if, switch, and conditional you write is not just runtime logic — it is also a proof to the compiler about what type the data must be.

```typescript
function process(value: string | number) {
    if (typeof value === "string") {
        console.log(value.toUpperCase()); // TS knows it's string here
    } else {
        console.log(value.toFixed(2));    // TS knows it's number here
    }
}
```


---

## typeof Guards

> 🎯 **Teach:** How typeof checks narrow primitive union types (string, number, boolean, undefined) in each branch of an if/else chain. **See:** Multi-branch formatting functions, null/undefined handling, a safe-stringify utility, and typeof used to route callback parameters. **Feel:** Fluency with the most common narrowing tool — typeof should become second nature.

### Narrowing Primitive Types

> 🎙️ The typeof operator is the simplest narrowing tool. It works for the primitive types that JavaScript knows about: string, number, boolean, undefined, object, and function. When you check typeof inside an if-statement, TypeScript narrows the type in each branch. You can chain else-if blocks to handle every variant of a union, and TypeScript will track the remaining possibilities at each step.

```typescript
// Basic typeof narrowing
function formatValue(value: string | number | boolean): string {
    if (typeof value === "string") {
        return `"${value}" (length: ${value.length})`;
    } else if (typeof value === "number") {
        return value % 1 === 0 ? `${value} (integer)` : `${value.toFixed(2)} (float)`;
    } else {
        return value ? "true" : "false";
    }
}

console.log(formatValue("hello"));
console.log(formatValue(3.14159));
console.log(formatValue(42));
console.log(formatValue(true));
```

### typeof with null and undefined

```typescript
// typeof with null and undefined
function greet(name: string | null | undefined): string {
    if (typeof name === "string") {
        return `Hello, ${name}!`;
    }
    return "Hello, stranger!";
}

console.log(greet("Campbell"));
console.log(greet(null));
console.log(greet(undefined));
```

### A Utility Function Using typeof

```typescript
// typeof in a utility function
function safeStringify(value: string | number | boolean | object | null | undefined): string {
    if (value === null) return "null";
    if (value === undefined) return "undefined";
    if (typeof value === "string") return `"${value}"`;
    if (typeof value === "number") return value.toString();
    if (typeof value === "boolean") return value ? "true" : "false";
    return JSON.stringify(value);
}

console.log(safeStringify("hello"));
console.log(safeStringify(42));
console.log(safeStringify(null));
console.log(safeStringify({ key: "value" }));
```

### typeof to Narrow Callback Parameters

```typescript
// typeof to narrow callback parameters
type StringProcessor = (input: string) => string;
type NumberProcessor = (input: number) => number;

function applyProcessor(value: string | number, strFn: StringProcessor, numFn: NumberProcessor): string | number {
    if (typeof value === "string") {
        return strFn(value);
    }
    return numFn(value);
}

const result = applyProcessor("hello", s => s.toUpperCase(), n => n * 2);
console.log(`Processed: ${result}`);
```

---

## instanceof and the `in` Operator

> 🎯 **Teach:** How instanceof narrows class-based unions by checking the prototype chain, and how the `in` operator narrows object unions by checking whether a property exists. **See:** A Pet union (Dog | Cat | Bird) narrowed with instanceof, and a Fish | Flyer union narrowed with the `in` operator. **Feel:** Confidence choosing the right narrowing tool — typeof for primitives, instanceof for classes, `in` for plain objects.

### instanceof Narrowing with Classes

> 🎙️ When your union is made of class instances rather than primitives, typeof will not help — it just says object for all of them. Instead, use instanceof. It checks the prototype chain and tells TypeScript exactly which class the value belongs to. Inside each instanceof branch, you get full access to that class's properties and methods.

```typescript
// instanceof narrowing
class Dog {
    constructor(public name: string, public breed: string) {}
    bark(): string { return `${this.name} says Woof!`; }
}

class Cat {
    constructor(public name: string, public indoor: boolean) {}
    meow(): string { return `${this.name} says Meow!`; }
}

class Bird {
    constructor(public name: string, public canFly: boolean) {}
    chirp(): string { return `${this.name} says Tweet!`; }
}

type Pet = Dog | Cat | Bird;

function describePet(pet: Pet): string {
    if (pet instanceof Dog) {
        return `${pet.bark()} (${pet.breed})`;
    } else if (pet instanceof Cat) {
        return `${pet.meow()} (${pet.indoor ? "indoor" : "outdoor"})`;
    } else {
        return `${pet.chirp()} (${pet.canFly ? "can fly" : "flightless"})`;
    }
}

const pets: Pet[] = [
    new Dog("Rex", "German Shepherd"),
    new Cat("Whiskers", true),
    new Bird("Tweety", true),
];

for (const pet of pets) {
    console.log(describePet(pet));
}
```

### The `in` Operator

> 🎙️ The in operator checks whether a property exists on an object. TypeScript uses this to narrow unions of object types. If you check whether swim is in creature, TypeScript knows it must be the type that has a swim property. This is especially useful when you are working with plain objects rather than class instances.

```typescript
// "in" operator narrowing
type Fish = { swim: () => void; name: string };
type Flyer = { fly: () => void; name: string };
type Swimmer = Fish | Flyer;

function move(creature: Swimmer): void {
    if ("swim" in creature) {
        console.log(`${creature.name} is swimming`);
        creature.swim();
    } else {
        console.log(`${creature.name} is flying`);
        creature.fly();
    }
}

const fish: Fish = { name: "Nemo", swim: () => console.log("  splash splash") };
const eagle: Flyer = { name: "Eagle", fly: () => console.log("  soaring high") };

move(fish);
move(eagle);
```

---

## Discriminated Unions

> 🎯 **Teach:** How a shared literal-typed tag property (discriminant) lets TypeScript narrow each case in a switch statement to a specific variant, and how custom type guard functions encapsulate complex validation behind a `value is T` predicate. **See:** An AppUser union discriminated by `role`, and custom type guards like `isString` and `isNonEmptyArray` that enable safe filtering. **Feel:** Appreciation that discriminated unions are one of TypeScript's most powerful patterns for modeling real-world data.

### Narrowing with a Shared Tag Property

> 🎙️ A discriminated union is a pattern where every variant in the union has a common property — a tag or discriminant — whose literal type is different for each variant. When you switch on that tag, TypeScript narrows each case to the exact variant. This is one of the most powerful patterns in TypeScript because it gives you exhaustive, type-safe branching over complex data shapes.

```typescript
// Discriminated union narrowing
type AdminUser = { role: "admin"; name: string; superAdmin: boolean };
type RegularUser = { role: "user"; name: string; subscription: "free" | "pro" };
type GuestUser = { role: "guest"; sessionId: string };
type AppUser = AdminUser | RegularUser | GuestUser;

function getGreeting(user: AppUser): string {
    switch (user.role) {
        case "admin":
            return `Welcome back, Admin ${user.name}${user.superAdmin ? " (Super)" : ""}`;
        case "user":
            return `Hello, ${user.name} [${user.subscription}]`;
        case "guest":
            return `Welcome, Guest (session: ${user.sessionId})`;
    }
}

const users: AppUser[] = [
    { role: "admin", name: "Alice", superAdmin: true },
    { role: "user", name: "Bob", subscription: "pro" },
    { role: "guest", sessionId: "abc-123" },
];

for (const user of users) {
    console.log(getGreeting(user));
}
```

### Custom Type Guard Functions

> 🎙️ Sometimes you need narrowing logic that is more complex than a single typeof or instanceof check. You can write a function that returns a type predicate — a special return type that says "if this function returns true, the argument is this specific type." This is called a custom type guard. It lets you encapsulate complex validation logic in a reusable function while still getting full type narrowing at the call site.

```typescript
// Custom type guard function
function isString(value: unknown): value is string {
    return typeof value === "string";
}

function isNonEmptyArray<T>(arr: T[] | null | undefined): arr is [T, ...T[]] {
    return Array.isArray(arr) && arr.length > 0;
}

const maybeNames: (string | number)[] = ["Alice", 42, "Bob", 7, "Carol"];
const names = maybeNames.filter(isString);
console.log(`\nFiltered names: ${names.join(", ")}`);

const emptyArr: string[] = [];
const fullArr: string[] = ["hello"];
console.log(`Empty check: ${isNonEmptyArray(emptyArr)}`);
console.log(`Full check: ${isNonEmptyArray(fullArr)}`);
```

---

## Exhaustive Checks and Assertion Functions

> 🎯 **Teach:** How the `never` type catches unhandled union variants at compile time via assertNever, and how assertion functions (`asserts value is T`) narrow types for the rest of a function body after a single check. **See:** A TrafficLight exhaustive switch, a PaymentMethod discriminated union with assertNever, assertion functions like `assertDefined` and `assertIsString`, and a combined narrowing example with DataSource. **Feel:** Safety and completeness — knowing the compiler will catch you if you forget a case or skip a validation.

### The assertNever Pattern

> 🎙️ When you handle every case in a union with a switch or if-else chain, the remaining type becomes never — a type that represents something that should be impossible. You can assign the value to a variable of type never in the default branch. If you ever add a new variant to the union and forget to handle it, the compiler will refuse to assign it to never and give you a compile error. This is called an exhaustive check, and it is your guarantee that you have covered every case.

```typescript
// Exhaustive check helper
function assertNever(value: never, message?: string): never {
    throw new Error(message ?? `Unexpected value: ${value}`);
}

// Traffic light with exhaustive check
type TrafficLight = "red" | "yellow" | "green";

function getAction(light: TrafficLight): string {
    switch (light) {
        case "red": return "Stop";
        case "yellow": return "Caution";
        case "green": return "Go";
        default: return assertNever(light);
    }
}

console.log(`Red: ${getAction("red")}`);
console.log(`Yellow: ${getAction("yellow")}`);
console.log(`Green: ${getAction("green")}`);
```

### Complex Exhaustive Check — Payment Methods

```typescript
// Complex exhaustive check — payment method
type CreditCard = { method: "credit_card"; cardNumber: string; expiry: string };
type BankTransfer = { method: "bank_transfer"; accountNumber: string; routingNumber: string };
type PayPal = { method: "paypal"; email: string };
type Crypto = { method: "crypto"; walletAddress: string; coin: string };
type PaymentMethod = CreditCard | BankTransfer | PayPal | Crypto;

function processPayment(payment: PaymentMethod): string {
    switch (payment.method) {
        case "credit_card":
            return `Charging card ending in ${payment.cardNumber.slice(-4)}, exp ${payment.expiry}`;
        case "bank_transfer":
            return `Transfer from account ${payment.accountNumber}, routing ${payment.routingNumber}`;
        case "paypal":
            return `PayPal payment to ${payment.email}`;
        case "crypto":
            return `Sending ${payment.coin} to wallet ${payment.walletAddress.slice(0, 8)}...`;
        default:
            return assertNever(payment);
    }
}

const payments: PaymentMethod[] = [
    { method: "credit_card", cardNumber: "4111111111111234", expiry: "12/27" },
    { method: "bank_transfer", accountNumber: "12345678", routingNumber: "021000021" },
    { method: "paypal", email: "user@example.com" },
    { method: "crypto", walletAddress: "0xAbCdEf1234567890", coin: "ETH" },
];

for (const p of payments) {
    console.log(processPayment(p));
}
```

### Assertion Functions

> 🎙️ An assertion function is a function whose return type says "asserts value is T." If the function returns normally, TypeScript treats the assertion as proven — the variable is narrowed from that point forward. If the assertion fails, the function throws. This is useful when you want to validate something once at the top of a function and then use the narrowed type for the rest of the function body, without wrapping everything in an if-block.

```typescript
// Assertion functions
function assertDefined<T>(value: T | null | undefined, name: string): asserts value is T {
    if (value === null || value === undefined) {
        throw new Error(`Expected ${name} to be defined, but got ${value}`);
    }
}

function assertIsString(value: unknown): asserts value is string {
    if (typeof value !== "string") {
        throw new Error(`Expected string, got ${typeof value}`);
    }
}

// Using assertion functions
function processConfig(config: { host?: string; port?: number }) {
    assertDefined(config.host, "host");
    assertDefined(config.port, "port");

    // After assertions, TypeScript knows both are defined
    console.log(`Connecting to ${config.host}:${config.port}`);
}

processConfig({ host: "localhost", port: 8080 });
```

### Assertions in a Lookup

```typescript
// Assertion in a lookup
const registry: Record<string, { name: string; version: string } | undefined> = {
    react: { name: "React", version: "18.2.0" },
    vue: { name: "Vue", version: "3.3.4" },
};

function getPackage(id: string) {
    const pkg = registry[id];
    assertDefined(pkg, `package "${id}"`);
    console.log(`${pkg.name} v${pkg.version}`); // TS knows pkg is defined
}

getPackage("react");
getPackage("vue");
```

### Combining Narrowing Techniques

```typescript
// Combining narrowing techniques
type DataSource =
    | { type: "file"; path: string }
    | { type: "url"; url: string }
    | { type: "inline"; content: string };

function readData(source: DataSource): string {
    switch (source.type) {
        case "file":
            return `Reading file: ${source.path}`;
        case "url":
            return `Fetching URL: ${source.url}`;
        case "inline":
            return `Inline data: ${source.content.slice(0, 50)}`;
        default:
            return assertNever(source);
    }
}

const sources: DataSource[] = [
    { type: "file", path: "/data/input.csv" },
    { type: "url", url: "https://api.example.com/data" },
    { type: "inline", content: "name,age\nAlice,25\nBob,30" },
];

for (const src of sources) {
    console.log(readData(src));
}
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to apply every narrowing technique from this module — typeof, instanceof, discriminated unions, custom guards, and assertNever — in your own code. **See:** Five hands-on exercises that build narrowing functions, shape classes, custom type guards, exhaustive checks, and assertion functions. **Feel:** Readiness to reach for the right narrowing tool in any situation.

> ✏️ Sharpen Your Pencil

1. Write a function `describeValue(value: string | number | boolean | null)` that uses typeof guards to return a different description for each type, including a specific check for null.
2. Create three classes (`Circle`, `Square`, `Triangle`) with a `kind` property and an `area()` method. Write a function using instanceof to describe each shape, and a second version using a discriminated union with a `kind` tag instead.
3. Write a custom type guard `isNonNull<T>(value: T | null | undefined): value is T` and use it with `.filter()` to remove nulls from an array.
4. Add a new variant to the `PaymentMethod` union (e.g., `{ method: "apple_pay"; deviceId: string }`) but do NOT add a case for it in `processPayment`. Observe the compile error from `assertNever`. Then fix it.
5. Write an assertion function `assertPositive(n: number): asserts n is number` that throws if the number is not positive. Use it to guard a function that calculates a square root.

---

> 💡 **Remember this one thing:** Type narrowing is how TypeScript uses your runtime checks to refine types at compile time.

---

## Up Next

> 🎯 **Teach:** Where the learning journey goes from here. **See:** A preview of Module 11 on ES module syntax, barrel files, and multi-file project organization. **Feel:** Momentum — narrowing mastered, now it is time to organize code at scale.

In **Module 11: Modules and Imports**, you will learn how to organize TypeScript code across multiple files using ES module syntax, barrel files, and clean import paths that scale with your project.
