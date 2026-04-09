# Module 9: Enums and Utility Types

## Introduction

> 🏷️ Useful Soon

> 🎙️ TypeScript gives you two tools that don't exist in JavaScript at all: enums and utility types. Enums define a fixed set of named constants -- things like log levels, HTTP status codes, or priority levels -- so you never accidentally use an invalid value. Utility types are built-in type transformations that take an existing type and produce a new one. Partial makes all properties optional. Pick selects specific properties. Omit removes them. Record maps keys to values. These are the type-level equivalents of array methods like map and filter, and they're used constantly in real TypeScript codebases.

> 🎯 **Teach:** How to define numeric, string, and const enums, and how to use TypeScript's built-in utility types to transform existing types.
> **See:** Enums used in switch statements and interfaces, utility types creating derived types from a base type, and both combined in a practical employee system.
> **Feel:** That enums make your code self-documenting and utility types eliminate repetition by deriving new types from existing ones.

> 🔄 **Where this fits:** You've built up types with aliases (Module 5), interfaces (Module 6), classes (Module 7), and generics (Module 8). Enums add named constants, and utility types give you tools to reshape the types you've already defined without rewriting them.

## Enums

> 🎯 **Teach:** How to define numeric, string, and const enums, and when to use each kind. **See:** A `Priority` numeric enum with auto-incrementing values, an `HttpStatus` enum with explicit codes, a `LogLevel` string enum for readable output, and a `const enum` that inlines at compile time. **Feel:** That enums make your code self-documenting -- named constants are clearer than magic numbers or raw strings, and TypeScript enforces that you only use valid values.

> 🎙️ An enum defines a set of named constants. Numeric enums auto-increment from zero by default, but you can set explicit values. String enums require each member to be initialized with a string literal. And const enums are inlined at compile time -- they produce no runtime JavaScript object at all, just the raw values substituted wherever you use them. Use numeric enums when the values don't matter, string enums when you need readable values in logs or APIs, and const enums when you want zero runtime overhead.

Enums define a set of named constants:

```typescript
// Numeric enum (values auto-increment from 0)
enum Direction { North, South, East, West }
console.log(Direction.North); // 0

// String enum (each member must be initialized)
enum Color { Red = "RED", Green = "GREEN", Blue = "BLUE" }
console.log(Color.Red); // "RED"

// Const enum (inlined at compile time, no runtime object)
const enum HttpStatus { OK = 200, NotFound = 404, ServerError = 500 }
```

### Program A: enums.ts

```typescript
// Numeric enum
enum Priority {
    Low,      // 0
    Medium,   // 1
    High,     // 2
    Critical, // 3
}

console.log(`High priority value: ${Priority.High}`);
console.log(`Name for value 1: ${Priority[1]}`); // Reverse mapping

// Custom starting value
enum HttpStatus {
    OK = 200,
    Created = 201,
    BadRequest = 400,
    Unauthorized = 401,
    NotFound = 404,
    ServerError = 500,
}

function describeStatus(status: HttpStatus): string {
    switch (status) {
        case HttpStatus.OK: return "Success";
        case HttpStatus.Created: return "Resource created";
        case HttpStatus.BadRequest: return "Bad request";
        case HttpStatus.Unauthorized: return "Unauthorized";
        case HttpStatus.NotFound: return "Not found";
        case HttpStatus.ServerError: return "Internal server error";
    }
}

console.log(`200 = ${describeStatus(HttpStatus.OK)}`);
console.log(`404 = ${describeStatus(HttpStatus.NotFound)}`);

// String enum
enum LogLevel {
    Debug = "DEBUG",
    Info = "INFO",
    Warn = "WARN",
    Error = "ERROR",
}

function log(level: LogLevel, message: string): void {
    console.log(`[${level}] ${message}`);
}

log(LogLevel.Info, "Application started");
log(LogLevel.Error, "Something went wrong");

// Const enum — inlined at compile time
const enum MathConstants {
    Pi = 3.14159,
    E = 2.71828,
    Tau = 6.28318,
}

const circleArea = MathConstants.Pi * 5 ** 2;
console.log(`Area of circle with radius 5: ${circleArea.toFixed(2)}`);

// Enum as a type in an interface
interface Task {
    title: string;
    priority: Priority;
    status: "todo" | "in-progress" | "done";
}

const tasks: Task[] = [
    { title: "Fix bug", priority: Priority.Critical, status: "in-progress" },
    { title: "Write docs", priority: Priority.Low, status: "todo" },
    { title: "Code review", priority: Priority.Medium, status: "done" },
];

for (const task of tasks) {
    console.log(`[${Priority[task.priority]}] ${task.title} — ${task.status}`);
}
```

## Utility Types

> 🎯 **Teach:** How to use TypeScript's built-in utility types to derive new types from existing ones without rewriting properties. **See:** `Partial` making all fields optional for update payloads, `Pick` and `Omit` selecting or excluding fields, `Record` mapping keys to values, `Readonly` for immutability, and `ReturnType`/`Parameters` for extracting function signatures. **Feel:** That utility types are the type-level equivalent of array methods -- powerful transformations that eliminate repetition and keep your types in sync with their source.

> 🎙️ Think of utility types as type transformations. You feed in an existing type and get back a modified version. Partial takes a type and makes every property optional -- perfect for update payloads where you only send the fields that changed. Required does the opposite, making every property required. Pick selects specific properties by name. Omit removes specific properties. Record creates a type that maps a set of keys to a value type. Readonly makes everything immutable. And ReturnType and Parameters extract types from function signatures. These are all generic types built into TypeScript -- you don't need to import anything.

### Program B: utility_types.ts

```typescript
// Base type
type User = {
    id: number;
    name: string;
    email: string;
    age: number;
    role: "admin" | "user" | "guest";
};

// Partial — all properties become optional
type UpdateUserPayload = Partial<User>;

function updateUser(id: number, updates: UpdateUserPayload): void {
    console.log(`Updating user ${id} with:`, updates);
}

updateUser(1, { name: "Alice" });         // Only update name
updateUser(2, { age: 31, role: "admin" }); // Update age and role

// Required — all properties become required
type Config = {
    host?: string;
    port?: number;
    debug?: boolean;
};

type FullConfig = Required<Config>;

const config: FullConfig = { host: "localhost", port: 3000, debug: false };
console.log(`Server: ${config.host}:${config.port}`);

// Pick — select specific properties
type UserPreview = Pick<User, "id" | "name">;

const preview: UserPreview = { id: 1, name: "Alice" };
console.log(`Preview: ${preview.name}`);

// Omit — exclude specific properties
type PublicUser = Omit<User, "email" | "age">;

const publicUser: PublicUser = { id: 1, name: "Alice", role: "admin" };
console.log(`Public: ${publicUser.name} (${publicUser.role})`);

// Record — map keys to a value type
type Fruit = "apple" | "banana" | "cherry";
type FruitInventory = Record<Fruit, number>;

const inventory: FruitInventory = { apple: 10, banana: 5, cherry: 20 };
console.log(`Apples in stock: ${inventory.apple}`);

// Record with complex values
type UserRoles = Record<string, { permissions: string[]; level: number }>;

const roles: UserRoles = {
    admin: { permissions: ["read", "write", "delete"], level: 3 },
    editor: { permissions: ["read", "write"], level: 2 },
    viewer: { permissions: ["read"], level: 1 },
};

for (const [role, info] of Object.entries(roles)) {
    console.log(`${role} (level ${info.level}): ${info.permissions.join(", ")}`);
}

// Readonly — all properties become readonly
type ImmutableUser = Readonly<User>;

const frozenUser: ImmutableUser = { id: 1, name: "Alice", email: "a@b.com", age: 25, role: "admin" };
// frozenUser.name = "Bob";  // Error: Cannot assign to 'name' because it is a read-only property

// ReturnType — extract a function's return type
function createUser(name: string, email: string) {
    return { id: Math.random(), name, email, createdAt: new Date() };
}

type CreatedUser = ReturnType<typeof createUser>;
const user: CreatedUser = createUser("Bob", "bob@example.com");
console.log(`Created: ${user.name} at ${user.createdAt.toISOString()}`);

// Parameters — extract a function's parameter types as a tuple
type CreateUserParams = Parameters<typeof createUser>;
const args: CreateUserParams = ["Charlie", "charlie@example.com"];
const user2 = createUser(...args);
console.log(`Created from args: ${user2.name}`);
```

## Practical Exercise: Combining Enums and Utility Types

> 🎯 **Teach:** How enums and utility types work together in a realistic employee management system with permissions, departments, and derived type variants. **See:** `Permission` and `Department` enums used inside an `Employee` type, then `Pick`, `Omit`, `Partial`, and `Record` creating `DirectoryEntry`, `PublicProfile`, `EmployeeUpdate`, and `DepartmentRoster` from the same base type. **Feel:** Confident that you can model a real application's data layer by combining enums for named constants with utility types for derived views of the same data.

> ✏️ Sharpen Your Pencil

> 🎙️ This exercise ties everything together. You'll define Permission and Department enums, build an Employee type that uses them, and then derive specialized types using utility types. DirectoryEntry uses Pick to select just the fields needed for a listing. PublicProfile uses Omit to hide salary. EmployeeUpdate combines Partial and Omit to create an update payload that can change any field except the ID. And DepartmentRoster uses Record to map each department to its list of employees. This is how real TypeScript applications compose enums and utility types.

### Program C: combined.ts

```typescript
enum Permission {
    Read = "READ",
    Write = "WRITE",
    Delete = "DELETE",
    Admin = "ADMIN",
}

enum Department {
    Engineering = "ENGINEERING",
    Marketing = "MARKETING",
    Sales = "SALES",
    HR = "HR",
}

type Employee = {
    id: number;
    name: string;
    email: string;
    department: Department;
    permissions: Permission[];
    salary: number;
};

// Use Pick to create a directory listing
type DirectoryEntry = Pick<Employee, "id" | "name" | "department">;

// Use Omit to create a public profile (no salary)
type PublicProfile = Omit<Employee, "salary">;

// Use Partial for updates
type EmployeeUpdate = Partial<Omit<Employee, "id">>;

// Use Record to build a department roster
type DepartmentRoster = Record<Department, DirectoryEntry[]>;

// Build employee data
const employees: Employee[] = [
    { id: 1, name: "Alice", email: "alice@co.com", department: Department.Engineering, permissions: [Permission.Read, Permission.Write, Permission.Admin], salary: 120000 },
    { id: 2, name: "Bob", email: "bob@co.com", department: Department.Engineering, permissions: [Permission.Read, Permission.Write], salary: 100000 },
    { id: 3, name: "Carol", email: "carol@co.com", department: Department.Marketing, permissions: [Permission.Read], salary: 90000 },
    { id: 4, name: "Dave", email: "dave@co.com", department: Department.Sales, permissions: [Permission.Read, Permission.Write], salary: 85000 },
];

// Build roster using Record
const roster: DepartmentRoster = {
    [Department.Engineering]: [],
    [Department.Marketing]: [],
    [Department.Sales]: [],
    [Department.HR]: [],
};

for (const emp of employees) {
    const entry: DirectoryEntry = { id: emp.id, name: emp.name, department: emp.department };
    roster[emp.department].push(entry);
}

for (const [dept, members] of Object.entries(roster)) {
    if (members.length > 0) {
        console.log(`\n${dept}:`);
        for (const m of members) {
            console.log(`  ${m.id}. ${m.name}`);
        }
    }
}

// Check permissions
function hasPermission(employee: Employee, required: Permission): boolean {
    return employee.permissions.includes(required);
}

for (const emp of employees) {
    const isAdmin = hasPermission(emp, Permission.Admin);
    console.log(`${emp.name}: Admin = ${isAdmin}`);
}

// Apply an update
function applyUpdate(employee: Employee, update: EmployeeUpdate): Employee {
    return { ...employee, ...update };
}

const updatedAlice = applyUpdate(employees[0], { department: Department.HR, permissions: [Permission.Read, Permission.Write, Permission.Delete, Permission.Admin] });
console.log(`\n${updatedAlice.name} moved to ${updatedAlice.department}`);
```

> 💡 **Remember this one thing:** Utility types transform existing types -- Partial makes everything optional, Pick selects fields, Omit removes them.

## Up Next

> 🎯 **Teach:** Where you are headed next and how type narrowing completes the union types story from Module 5. **See:** A preview of `typeof`, `instanceof`, `in`, truthiness checks, and user-defined type guards for narrowing unions at runtime. **Feel:** Eager to master the full toolkit for working with union types safely and confidently.

In **Module 10: Type Narrowing**, you'll learn the full set of techniques TypeScript provides for narrowing union types at runtime -- typeof, instanceof, in, truthiness checks, and user-defined type guards.
