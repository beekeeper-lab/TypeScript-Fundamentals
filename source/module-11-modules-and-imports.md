# Module 11: Modules and Imports

> 🏷️ When You're Ready

> 🎯 **Teach:** How to organize TypeScript code across multiple files using ES module syntax — named exports, default exports, re-exports, and barrel files. **See:** A complete multi-file project with models, services, and a main entry point that imports cleanly from barrel files. **Feel:** Readiness to structure real projects the way professional codebases are organized.

> 🔄 **Where this fits:** You have learned the type system — primitives, unions, interfaces, classes, generics, and narrowing. Now you need to organize all of that into files that can grow without becoming unmanageable. Modules are how TypeScript (and JavaScript) code scales from a single file to a real application.

## ES Module Syntax

> 🎯 **Teach:** The difference between named exports and default exports, how import syntax mirrors them, and how barrel files (index.ts) create clean public APIs for folders. **See:** Named exports with curly-brace imports, a default class export with bare imports, and a barrel file that re-exports from multiple modules. **Feel:** Clarity about the two export styles and when to use each one.

### Named and Default Exports

> 🎙️ TypeScript uses ES module syntax to organize code across files. Every file is its own module. You choose what to expose by marking things with the export keyword. There are two kinds of exports: named exports, where you export specific items by name, and default exports, where you export one main thing from the file. When importing, named exports use curly braces and default exports do not. This distinction matters because it affects how consumers import your code and how refactoring tools can track references.

```typescript
// math.ts — Named exports
export function add(a: number, b: number): number { return a + b; }
export const PI = 3.14159;

// logger.ts — Default export
export default class Logger {
    log(msg: string) { console.log(msg); }
}

// app.ts — Importing
import { add, PI } from "./math";
import Logger from "./logger";
```

![Module exports and imports — named exports flow through curly braces, default exports flow directly](../images/module-11/exports-imports-flow.png)
*Module exports and imports — named exports flow through curly braces, default exports flow directly*

### Barrel Files

> 🎙️ As your project grows, you end up with many files in a folder. Instead of making every consumer import from individual files deep inside your directory structure, you create a barrel file — an index.ts that re-exports everything from the folder. Consumers import from the folder path, and the barrel file decides what is public. This gives you clean import paths and a single place to control the public API of each folder.

```typescript
// utils/index.ts
export { add, subtract } from "./math";
export { formatDate } from "./dates";
export { Logger } from "./logger";

// app.ts — clean single import
import { add, formatDate, Logger } from "./utils";
```

---

## Building the Models Layer

> 🎯 **Teach:** How to define the data-shape layer of a project using exported types, interfaces, and factory functions in dedicated model files. **See:** A User model with a role type, interface, createUser factory, and formatUser helper, plus a Product model with an enum, factory function, and a default-exported ProductCatalog class. **Feel:** Satisfaction at seeing clean, single-responsibility model files that are easy to import and test.

### User Model

> 🎙️ Let us build a multi-file project step by step. We start with the models layer — the types and factory functions that define the shape of our data. The user model exports a type alias for roles, an interface for the user object, and two functions: one to create users and one to format them for display. Notice that everything is a named export. This makes it easy to import exactly what you need.

```typescript
// models/user.ts

// Named exports for types and a factory function
export type UserRole = "admin" | "editor" | "viewer";

export interface User {
    id: number;
    name: string;
    email: string;
    role: UserRole;
    active: boolean;
}

export function createUser(id: number, name: string, email: string, role: UserRole = "viewer"): User {
    return { id, name, email, role, active: true };
}

export function formatUser(user: User): string {
    return `[${user.role.toUpperCase()}] ${user.name} <${user.email}>`;
}
```

### Product Model

```typescript
// models/product.ts

export interface Product {
    sku: string;
    name: string;
    price: number;
    category: Category;
    inStock: boolean;
}

// Export enum
export enum Category {
    Electronics = "ELECTRONICS",
    Books = "BOOKS",
    Clothing = "CLOTHING",
    Food = "FOOD",
}

export function createProduct(sku: string, name: string, price: number, category: Category): Product {
    return { sku, name, price, category, inStock: true };
}

export function formatPrice(price: number): string {
    return `$${price.toFixed(2)}`;
}

// Default export — a utility class
export default class ProductCatalog {
    private products: Product[] = [];

    add(product: Product): void {
        this.products.push(product);
    }

    findBySku(sku: string): Product | undefined {
        return this.products.find(p => p.sku === sku);
    }

    getByCategory(category: Category): Product[] {
        return this.products.filter(p => p.category === category);
    }

    list(): Product[] {
        return [...this.products];
    }
}
```

---

## Building the Services Layer

> 🎯 **Teach:** How a services layer imports from models and adds business logic, including the use of `import type` for type-only imports and re-exports for consumer convenience. **See:** A UserService that imports types and functions from the models barrel, a ProductService that mixes default and named imports and uses `import type`, and a re-export of Category from the service file. **Feel:** Appreciation for the clean separation between data shapes (models) and behavior (services).

### User Service

> 🎙️ The services layer imports from the models layer and adds business logic. The UserService class manages a collection of users — adding, finding, filtering, and deactivating them. Notice how the import statement pulls in exactly the types and functions it needs from the models layer. This is the pattern: models define data shapes, services operate on that data.

```typescript
// services/user_service.ts

import { User, UserRole, createUser, formatUser } from "../models/user";

export class UserService {
    private users: User[] = [];
    private nextId = 1;

    addUser(name: string, email: string, role: UserRole = "viewer"): User {
        const user = createUser(this.nextId++, name, email, role);
        this.users.push(user);
        return user;
    }

    findByEmail(email: string): User | undefined {
        return this.users.find(u => u.email === email);
    }

    getByRole(role: UserRole): User[] {
        return this.users.filter(u => u.role === role);
    }

    deactivate(id: number): boolean {
        const user = this.users.find(u => u.id === id);
        if (user) {
            user.active = false;
            return true;
        }
        return false;
    }

    listAll(): string[] {
        return this.users.map(formatUser);
    }
}
```

### Product Service

> 🎙️ The ProductService shows two important import patterns. First, it imports the default export ProductCatalog without curly braces, alongside named exports in curly braces — all from the same file. Second, it uses import type for the Product interface, which tells TypeScript this import is only for type checking and should be erased completely from the compiled JavaScript. Finally, notice the re-export at the bottom — the service re-exports Category so that consumers do not need to reach into the models layer directly.

```typescript
// services/product_service.ts

import ProductCatalog, { createProduct, Category, formatPrice } from "../models/product";
import type { Product } from "../models/product";

export class ProductService {
    private catalog = new ProductCatalog();

    addProduct(sku: string, name: string, price: number, category: Category): Product {
        const product = createProduct(sku, name, price, category);
        this.catalog.add(product);
        return product;
    }

    search(sku: string): Product | undefined {
        return this.catalog.findBySku(sku);
    }

    listByCategory(category: Category): string[] {
        return this.catalog.getByCategory(category).map(
            p => `${p.name} — ${formatPrice(p.price)}`
        );
    }

    getInventorySummary(): string {
        const products = this.catalog.list();
        const total = products.reduce((sum, p) => sum + p.price, 0);
        return `${products.length} products, total value: ${formatPrice(total)}`;
    }
}

// Re-export Category for convenience
export { Category } from "../models/product";
```

---

## Barrel Files and the Main Entry Point

> 🎯 **Teach:** How barrel files (index.ts) re-export from individual modules to create a single clean import path per folder, and how a main entry point ties the whole project together. **See:** A models/index.ts and services/index.ts barrel file, plus a main.ts that imports from folder paths instead of individual files. **Feel:** The payoff of good organization — imports are short, the public API of each folder is explicit, and the project reads like a well-structured application.

### Models Barrel File

> 🎙️ Now we create the barrel files — the index.ts in each folder that re-exports everything the folder wants to make public. The models barrel file re-exports all the types, functions, and the default ProductCatalog class from both model files. The services barrel file does the same for the service classes. With these in place, the main entry point can import from just two clean paths instead of reaching into individual files.

```typescript
// models/index.ts

// Barrel file — re-export everything from models
export { User, UserRole, createUser, formatUser } from "./user";
export { Product, Category, createProduct, formatPrice } from "./product";
export { default as ProductCatalog } from "./product";
```

### Services Barrel File

```typescript
// services/index.ts

// Barrel file — re-export services
export { UserService } from "./user_service";
export { ProductService, Category } from "./product_service";
```

### Main Entry Point

```typescript
// main.ts

// Import from barrel files — clean, single-path imports
import { UserService } from "./services";
import { ProductService, Category } from "./services";
import { formatPrice } from "./models";

// --- Users ---
const userService = new UserService();
userService.addUser("Alice", "alice@example.com", "admin");
userService.addUser("Bob", "bob@example.com", "editor");
userService.addUser("Carol", "carol@example.com");

console.log("=== All Users ===");
for (const line of userService.listAll()) {
    console.log(`  ${line}`);
}

console.log("\n=== Editors ===");
for (const line of userService.getByRole("editor").map(u => u.name)) {
    console.log(`  ${line}`);
}

// --- Products ---
const productService = new ProductService();
productService.addProduct("ELEC-001", "Wireless Mouse", 29.99, Category.Electronics);
productService.addProduct("ELEC-002", "USB-C Hub", 49.99, Category.Electronics);
productService.addProduct("BOOK-001", "TypeScript Handbook", 39.99, Category.Books);
productService.addProduct("CLTH-001", "Dev T-Shirt", 24.99, Category.Clothing);

console.log("\n=== Electronics ===");
for (const line of productService.listByCategory(Category.Electronics)) {
    console.log(`  ${line}`);
}

console.log("\n=== Inventory ===");
console.log(`  ${productService.getInventorySummary()}`);

// Search
const found = productService.search("BOOK-001");
if (found) {
    console.log(`\nFound: ${found.name} — ${formatPrice(found.price)}`);
}
```

---

## Compiling a Multi-File Project

> 🎯 **Teach:** How tsconfig.json configures module resolution, output directory, and file inclusion so a single `tsc` command compiles an entire multi-file project. **See:** A tsconfig.json with NodeNext module settings, include patterns, and the command to compile and run the project. **Feel:** Confidence that you can set up and compile a real multi-file TypeScript project from scratch.

### tsconfig.json for Module Projects

> 🎙️ To compile a multi-file project, you need a tsconfig.json that tells the compiler where to find your source files and how to resolve module imports. The include array lists the file patterns to compile. The module and moduleResolution settings tell TypeScript to use Node's module resolution algorithm. Once this is in place, you can compile the entire project with a single tsc command.

```json
{
    "compilerOptions": {
        "target": "ES2022",
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "outDir": "dist",
        "strict": true
    },
    "include": ["*.ts", "models/*.ts", "services/*.ts"]
}
```

```bash
npx tsc && node dist/main.js
```

Or compile and run directly:

```bash
npx tsc --module nodenext --moduleResolution nodenext --target es2022 --outDir dist main.ts
node dist/main.js
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to build and extend a multi-file module project hands-on, including adding new models, services, barrel exports, and experimenting with import patterns. **See:** Five exercises that walk through creating the full file structure, adding an Order model and service, using `import type`, and renaming exports in barrel files. **Feel:** Ownership — you are not just reading about modules, you are building a real project layout yourself.

> ✏️ Sharpen Your Pencil

1. Create the full file structure (`models/user.ts`, `models/product.ts`, `services/user_service.ts`, `services/product_service.ts`, barrel files, and `main.ts`). Compile and run it.
2. Add a new model file `models/order.ts` that exports an `Order` interface and a `createOrder` function. Update `models/index.ts` to re-export from it.
3. Create `services/order_service.ts` that imports from the models barrel file. Update `services/index.ts` and use the new service in `main.ts`.
4. Try importing with `import type` for an interface and see what happens if you try to use it as a value (e.g., call a constructor). What error do you get?
5. Experiment with renaming an export: `export { UserService as Users }` in the barrel file. How does this affect the import in `main.ts`?

---

> 💡 **Remember this one thing:** Barrel files (index.ts) give clean import paths — import from the folder, not individual files.

---

## Up Next

> 🎯 **Teach:** Where the learning journey goes from here. **See:** A preview of Module 12 covering Promises, async/await, and typed async patterns. **Feel:** Momentum — your code is organized across files, and now you are ready to handle the asynchronous operations that real applications depend on.

In **Module 12: Async/Await and Promises**, you will learn how TypeScript types asynchronous code — from creating and chaining Promises to using async/await, combinators like Promise.all, and typed async patterns like retry and batch processing.
