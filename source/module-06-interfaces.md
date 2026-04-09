# Module 6: Interfaces

## Introduction

> 🏷️ Useful Soon

> 🎙️ In the last module you used type aliases to define object shapes. TypeScript has a second tool for the same job: interfaces. Interfaces are the preferred way to define object shapes in TypeScript. They support extension with the extends keyword, they auto-merge when declared multiple times, and they make your intent clear -- when someone sees interface, they know it describes the shape of an object. Today you'll define interfaces with optional and readonly properties, extend them through single and multiple inheritance, write function and index signatures, and build generic API response interfaces.

> 🎯 **Teach:** How to define, extend, and implement interfaces, and when to choose interface over type.
> **See:** Interfaces composing through extends, function and index signatures, and generic interfaces for API responses.
> **Feel:** That interfaces are the natural choice for describing object shapes, and that the interface-vs-type decision has a simple rule of thumb.

> 🔄 **Where this fits:** You already know type aliases and union types from Module 5. Interfaces give you a second way to define object shapes -- one that's optimized for extension and declaration merging. In Module 7 you'll see classes that implement interfaces.

## Interfaces

> 🎯 **Teach:** The syntax and core features of interfaces -- properties, optional fields, readonly, extension, and the key differences from type aliases. **See:** An interface with optional and readonly properties, single and multiple inheritance with `extends`, and a comparison table of interface vs type. **Feel:** That interfaces are the natural, idiomatic choice for describing object shapes, and that the decision between interface and type has a simple rule of thumb.

> 🎙️ An interface defines the shape of an object -- what properties it must have, their types, and whether they're optional or readonly. It looks similar to a type alias for an object, but uses the interface keyword. The key difference is that interfaces are designed for extension and merging, which makes them the better choice when you're defining object shapes that other code will build on.

```typescript
interface User {
    id: number;
    name: string;
    email: string;
    age?: number;              // Optional
    readonly createdAt: Date;  // Cannot be changed after creation
}
```

### Extending Interfaces

```typescript
interface Animal { name: string; legs: number; }
interface Dog extends Animal { breed: string; }
// Dog has: name, legs, AND breed
```

### Interface vs Type

| Feature | `interface` | `type` |
|---------|------------|--------|
| Extend/inherit | `extends` | `&` (intersection) |
| Merge declarations | Yes (auto-merges) | No |
| Union types | No | Yes |
| Primitives/tuples | No | Yes |
| Use for objects | Preferred | Also works |

Rule of thumb: Use `interface` for object shapes, `type` for everything else.

### Implementing Interfaces

```typescript
interface Printable {
    toString(): string;
}

class Product implements Printable {
    constructor(public name: string, public price: number) {}
    toString(): string { return `${this.name}: $${this.price}`; }
}
```

## Basic Interfaces

> 🎯 **Teach:** How to define a practical interface with readonly IDs, optional properties, and typed arrays. **See:** A `Product` interface with `readonly id`, optional `tags`, and a function that displays products conditionally based on optional fields. **Feel:** That interfaces make your object shapes explicit and self-documenting -- when you read the interface, you know exactly what a Product looks like.

> 🎙️ Let's start with a Product interface that uses the core features: readonly to prevent ID changes after creation, optional properties for tags that might not be present, and a typed array of products. Notice how readonly on id means you can set it when you create the object but can never change it afterward.

### Program A: basic_interfaces.ts

```typescript
interface Product {
    readonly id: number;
    name: string;
    price: number;
    category: string;
    inStock: boolean;
    tags?: string[];
}

function displayProduct(product: Product): void {
    console.log(`[${product.id}] ${product.name} — $${product.price.toFixed(2)}`);
    console.log(`  Category: ${product.category}, In Stock: ${product.inStock}`);
    if (product.tags) {
        console.log(`  Tags: ${product.tags.join(", ")}`);
    }
}

const products: Product[] = [
    { id: 1, name: "Laptop", price: 999.99, category: "Electronics", inStock: true, tags: ["computer", "portable"] },
    { id: 2, name: "Notebook", price: 4.99, category: "Office", inStock: true },
    { id: 3, name: "Headphones", price: 79.99, category: "Electronics", inStock: false, tags: ["audio"] },
];

products.forEach(displayProduct);

// Readonly prevents modification
// products[0].id = 99;  // Error: Cannot assign to 'id'
products[0].price = 899.99;  // OK — price is not readonly
```

## Extending Interfaces

> 🎯 **Teach:** How to build interface hierarchies using `extends`, including single inheritance, multi-level inheritance, and extending multiple interfaces at once. **See:** `BaseEntity` extended by `User`, then `AdminUser` adding permissions, and `AuditedUser` extending both `User` and `Auditable`. **Feel:** That interface extension creates clean, composable hierarchies without repeating properties -- each layer adds only what's new.

> 🎙️ Interface extension is one of the main reasons to choose interface over type. With extends, you build up a hierarchy of shapes. A User extends BaseEntity to get id, createdAt, and updatedAt. An AdminUser extends User to add permissions and department. And you can extend multiple interfaces at once -- AuditedUser extends both User and Auditable. This creates clean, composable hierarchies without repeating properties.

### Program B: extending.ts

```typescript
interface BaseEntity {
    id: string;
    createdAt: Date;
    updatedAt: Date;
}

interface User extends BaseEntity {
    name: string;
    email: string;
    role: "admin" | "user" | "guest";
}

interface AdminUser extends User {
    permissions: string[];
    department: string;
}

// Multiple extension
interface Auditable {
    lastModifiedBy: string;
}

interface AuditedUser extends User, Auditable {
    loginCount: number;
}

const admin: AdminUser = {
    id: "admin-001",
    createdAt: new Date(),
    updatedAt: new Date(),
    name: "Alice",
    email: "alice@example.com",
    role: "admin",
    permissions: ["read", "write", "delete"],
    department: "Engineering",
};

const auditedUser: AuditedUser = {
    id: "user-001",
    createdAt: new Date(),
    updatedAt: new Date(),
    name: "Bob",
    email: "bob@example.com",
    role: "user",
    lastModifiedBy: "admin-001",
    loginCount: 42,
};

console.log(`Admin: ${admin.name} (${admin.permissions.join(", ")})`);
console.log(`User: ${auditedUser.name} (logins: ${auditedUser.loginCount})`);
```

## Function and Index Signatures

> 🎯 **Teach:** How interfaces can define method signatures, index signatures for dynamic keys, and callable signatures for function-like objects. **See:** A `Calculator` interface with four methods, a `StringMap` with an index signature, and a `Formatter` that is both callable and has properties. **Feel:** That interfaces go beyond simple data shapes -- they can describe any object contract, including objects that behave like functions or have dynamic keys.

> 🎙️ Interfaces can describe more than just data shapes. They can define method signatures, index signatures for dynamic keys, and even callable signatures for objects that act as functions. The Calculator interface below defines four methods. The StringMap interface says "any string key maps to a string value." And the Formatter interface describes an object that you can call like a function but that also has a prefix property.

### Program C: signatures.ts

```typescript
// Interface with methods
interface Calculator {
    add(a: number, b: number): number;
    subtract(a: number, b: number): number;
    multiply(a: number, b: number): number;
    divide(a: number, b: number): number;
}

const calc: Calculator = {
    add: (a, b) => a + b,
    subtract: (a, b) => a - b,
    multiply: (a, b) => a * b,
    divide: (a, b) => {
        if (b === 0) throw new Error("Division by zero");
        return a / b;
    },
};

console.log(`5 + 3 = ${calc.add(5, 3)}`);
console.log(`10 / 3 = ${calc.divide(10, 3).toFixed(2)}`);

// Index signature — dynamic keys
interface StringMap {
    [key: string]: string;
}

const headers: StringMap = {
    "Content-Type": "application/json",
    "Authorization": "Bearer token123",
};

// Interface for callable objects
interface Formatter {
    (value: number): string;
    prefix: string;
}

const currencyFormatter = ((value: number) => {
    return `${currencyFormatter.prefix}${value.toFixed(2)}`;
}) as Formatter;
currencyFormatter.prefix = "$";

console.log(currencyFormatter(42.5));
```

## Practical Exercise: Generic API Response Interfaces

> 🎯 **Teach:** How to combine interfaces with generics to build reusable API response types that wrap any data shape with metadata and pagination. **See:** A generic `ApiResponse<T>` interface used for both `TodoItem[]` lists and single `TodoItem | null` lookups, with optional pagination. **Feel:** That generic interfaces are the key to building typed APIs -- you define the wrapper once and reuse it for every endpoint.

> ✏️ Sharpen Your Pencil

> 🎙️ This exercise brings interfaces into a realistic scenario: defining the types for a REST API. You'll create a generic ApiResponse interface that wraps any data type with status, message, and optional pagination. The generic parameter T lets you reuse the same response shape for todo lists, single items, or any other data type. This is a pattern you'll use in every project that talks to a backend.

### Program D: api_types.ts

```typescript
interface PaginationParams {
    page: number;
    limit: number;
    sortBy?: string;
    order?: "asc" | "desc";
}

interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
    pagination?: {
        total: number;
        page: number;
        pages: number;
    };
}

interface TodoItem {
    id: number;
    title: string;
    completed: boolean;
    priority: 1 | 2 | 3 | 4 | 5;
    dueDate?: string;
}

// Simulate API functions
function getTodos(params: PaginationParams): ApiResponse<TodoItem[]> {
    const todos: TodoItem[] = [
        { id: 1, title: "Learn TypeScript", completed: false, priority: 1 },
        { id: 2, title: "Build a project", completed: false, priority: 2 },
        { id: 3, title: "Write tests", completed: true, priority: 3 },
    ];
    return {
        data: todos,
        status: 200,
        message: "Success",
        pagination: { total: todos.length, page: params.page, pages: 1 },
    };
}

function getTodoById(id: number): ApiResponse<TodoItem | null> {
    return {
        data: id === 1 ? { id: 1, title: "Learn TypeScript", completed: false, priority: 1 } : null,
        status: id === 1 ? 200 : 404,
        message: id === 1 ? "Found" : "Not found",
    };
}

// Use the API
const response = getTodos({ page: 1, limit: 10, sortBy: "priority", order: "asc" });
console.log(`Status: ${response.status}, Items: ${response.data.length}`);
response.data.forEach(todo => {
    const status = todo.completed ? "✓" : "○";
    console.log(`  [${status}] P${todo.priority}: ${todo.title}`);
});

const single = getTodoById(1);
console.log(`\nSingle: ${single.data?.title ?? "Not found"}`);
```

> 💡 **Remember this one thing:** Use interface for object shapes, type for everything else.

## Up Next

> 🎯 **Teach:** Where you are headed next and how interfaces connect to classes. **See:** A preview of classes implementing interfaces with the `implements` keyword, plus access modifiers and abstract classes. **Feel:** Excited to see how classes bring interfaces to life by bundling data and behavior together.

In **Module 7: Classes**, you'll see how classes implement interfaces using the `implements` keyword, and how TypeScript adds access modifiers, parameter properties, and abstract classes to JavaScript's class syntax.
