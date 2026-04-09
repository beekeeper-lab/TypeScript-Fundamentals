# Module 2: Arrays, Tuples, and Objects

> 🏷️ Start Here

> 🎯 **Teach:** How to structure data using TypeScript's collection and object types. **See:** The difference between arrays (same-type collections), tuples (fixed-length typed positions), and objects (named fields). **Feel:** Confident choosing the right data structure for the job.

> 🔄 **Where this fits:** Module 1 gave you the primitive types. Now you combine them into structures. Arrays, tuples, and objects are how real programs organize data — from API responses to database records to configuration objects. Every module from here forward uses these structures.

## Arrays

> 🎯 **Teach:** How to declare typed arrays that enforce a single element type across the entire collection. **See:** Array declarations using both `type[]` and `Array<type>` syntax, including union type arrays. **Feel:** Clear on how TypeScript prevents you from accidentally mixing incompatible types in an array.

### Typed Arrays

```typescript
let numbers: number[] = [1, 2, 3, 4, 5];
let names: string[] = ["Alice", "Bob"];
let mixed: (string | number)[] = [1, "two", 3]; // Union type array

// Alternative syntax
let scores: Array<number> = [88, 92, 76];
```

## Tuples

> 🎯 **Teach:** How tuples differ from arrays — fixed length, specific type at each position — and when to use them. **See:** Tuple declarations for points, key-value pairs, and RGB colors, with TypeScript enforcing types at each index. **Feel:** Confident distinguishing tuples from arrays and knowing when a tuple is the better choice.

### Fixed-Length Typed Arrays

> 🎙️ Arrays and tuples look similar — they both use square brackets — but they serve different purposes. An array is a collection of values that are all the same type. You do not know how many there will be, and you access them by iterating. A tuple is a fixed-length structure where each position has its own specific type. Think of a tuple as a lightweight object without field names. When a function needs to return two values, a tuple is often the right choice.

```typescript
let point: [number, number] = [3, 4];
let entry: [string, number] = ["Alice", 88];
let rgb: [number, number, number] = [255, 128, 0];
```

## Object Types

> 🎯 **Teach:** How to define inline object types with required, optional, and readonly properties. **See:** Object literals with typed fields, optional properties using `?`, and `readonly` preventing mutation at compile time. **Feel:** Able to model real-world entities as typed objects with precisely the shape you need.

### Inline Object Types

```typescript
let person: { name: string; age: number; active: boolean } = {
    name: "Campbell",
    age: 20,
    active: true,
};

// Optional properties with ?
let config: { host: string; port: number; debug?: boolean } = {
    host: "localhost",
    port: 3000,
    // debug is optional — can be omitted
};
```

### Readonly

> 🎙️ The `readonly` modifier is one of TypeScript's most useful tools for preventing accidental mutation. When you mark a property or array as readonly, TypeScript will stop you at compile time if you try to change it. This is especially valuable for IDs, configuration values, and any data that should be set once and never modified. Note that readonly is a compile-time check only — it does not exist at runtime in JavaScript.

```typescript
const point: readonly number[] = [1, 2, 3];
// point.push(4);  // Error: push does not exist on readonly number[]

let user: { readonly id: number; name: string } = { id: 1, name: "Alice" };
// user.id = 2;    // Error: Cannot assign to 'id'
user.name = "Bob"; // OK — only id is readonly
```

![Data structures in TypeScript — arrays, tuples, and objects compared](../images/module-02/data-structures.png)
*Data structures in TypeScript — arrays, tuples, and objects compared*

---

## Typed Arrays in Depth

> 🎯 **Teach:** How to use typed arrays with full type safety — push, map, filter, reduce, sort, spread, and destructuring. **See:** A complete program that manipulates number arrays while TypeScript guards every operation. **Feel:** Fluent with array operations and confident that TypeScript catches mistakes at each step.

### Program A: arrays.ts

```typescript
// Typed arrays
const grades: number[] = [88, 92, 76, 95, 83];
const languages: string[] = ["TypeScript", "Python", "Java", "Dart"];
const flags: boolean[] = [true, false, true, true];

// Array methods work with type safety
grades.push(91);
// grades.push("A");  // Error: string not assignable to number

console.log(`Grades: ${grades}`);
console.log(`Average: ${(grades.reduce((a, b) => a + b) / grades.length).toFixed(1)}`);
console.log(`Highest: ${Math.max(...grades)}`);
console.log(`Lowest: ${Math.min(...grades)}`);

// Map, filter, reduce — TypeScript infers return types
const doubled = grades.map(g => g * 2);          // number[]
const passing = grades.filter(g => g >= 80);      // number[]
const total = grades.reduce((sum, g) => sum + g, 0); // number

console.log(`Doubled: ${doubled}`);
console.log(`Passing (>=80): ${passing}`);
console.log(`Total: ${total}`);

// Sorting
const sorted = [...grades].sort((a, b) => a - b);
console.log(`Sorted: ${sorted}`);

// Destructuring
const [first, second, ...rest] = sorted;
console.log(`First: ${first}, Second: ${second}, Rest: ${rest}`);
```

---

## Tuples in Depth

> 🎯 **Teach:** Advanced tuple features — labeled tuples, optional elements, destructuring, and functions that return tuples. **See:** Tuples used for coordinates, key-value pairs, and multi-value returns with full type safety at each position. **Feel:** Ready to use tuples as lightweight, typed alternatives to objects when field names are not needed.

### Program B: tuples.ts

```typescript
// Basic tuples
const point: [number, number] = [10, 20];
const nameAge: [string, number] = ["Campbell", 20];
const rgb: [number, number, number] = [255, 128, 0];

// Destructuring tuples
const [x, y] = point;
const [name, age] = nameAge;
const [r, g, b] = rgb;

console.log(`Point: (${x}, ${y})`);
console.log(`${name} is ${age} years old`);
console.log(`RGB: rgb(${r}, ${g}, ${b})`);

// Labeled tuples (TypeScript 4.0+)
type Coordinate = [x: number, y: number, z: number];
const position: Coordinate = [1, 2, 3];

// Tuples with optional elements
type FlexPoint = [number, number, number?];
const point2D: FlexPoint = [5, 10];
const point3D: FlexPoint = [5, 10, 15];

console.log(`2D: ${point2D}`);
console.log(`3D: ${point3D}`);

// Tuple vs Array — key difference
const tuple: [string, number] = ["Alice", 88];
// tuple[0] = 42;   // Error: number not assignable to string
// Tuples enforce type at each position

// Practical use: function returning multiple values
function getMinMax(nums: number[]): [number, number] {
    return [Math.min(...nums), Math.max(...nums)];
}

const [min, max] = getMinMax([3, 1, 4, 1, 5, 9]);
console.log(`Min: ${min}, Max: ${max}`);
```

---

## Object Types in Depth

> 🎯 **Teach:** How to build complex object types with optional, readonly, and nested properties. **See:** Inline object types for a student, a server config, and a company with a nested address — each demonstrating different property modifiers. **Feel:** Comfortable modeling real-world data structures with precise object types.

### Program C: objects.ts

```typescript
// Inline object type
const student: {
    name: string;
    age: number;
    gpa: number;
    courses: string[];
    graduated: boolean;
} = {
    name: "Campbell",
    age: 20,
    gpa: 3.8,
    courses: ["TypeScript", "Python", "Java"],
    graduated: false,
};

console.log(`Student: ${student.name}`);
console.log(`Courses: ${student.courses.join(", ")}`);

// Optional properties
const config: {
    host: string;
    port: number;
    debug?: boolean;    // Optional
    timeout?: number;   // Optional
} = {
    host: "localhost",
    port: 3000,
};

console.log(`Config: ${config.host}:${config.port}`);
console.log(`Debug: ${config.debug ?? "not set"}`);

// Readonly properties
const server: {
    readonly id: string;
    name: string;
    status: string;
} = {
    id: "srv-001",
    name: "Main Server",
    status: "running",
};

server.status = "stopped";  // OK
// server.id = "srv-002";   // Error: Cannot assign to 'id'

// Nested objects
const company: {
    name: string;
    address: {
        street: string;
        city: string;
        state: string;
    };
    employees: number;
} = {
    name: "Stonewaters Consulting",
    address: {
        street: "123 Main St",
        city: "Austin",
        state: "TX",
    },
    employees: 50,
};

console.log(`${company.name} — ${company.address.city}, ${company.address.state}`);
```

---

## Spread and Destructuring

> 🎯 **Teach:** How spread and destructuring work with TypeScript's type system for copying, merging, and extracting values from objects and arrays. **See:** Object destructuring with rename, spread for merging objects, array spread for concatenation, and rest syntax. **Feel:** Empowered to write concise, readable code for common data manipulation patterns.

### Program D: spread_destructure.ts

```typescript
// Object destructuring
const person = { name: "Campbell", age: 20, city: "Austin" };
const { name, age, city } = person;
console.log(`${name}, ${age}, ${city}`);

// Destructuring with rename
const { name: fullName, age: currentAge } = person;
console.log(`${fullName} is ${currentAge}`);

// Spread operator — copy objects
const defaults = { theme: "dark", fontSize: 14, lang: "en" };
const userPrefs = { fontSize: 18, lang: "es" };
const merged = { ...defaults, ...userPrefs }; // userPrefs overrides
console.log(merged); // { theme: "dark", fontSize: 18, lang: "es" }

// Spread with arrays
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];
console.log(`Combined: ${combined}`);

// Rest parameters in destructuring
const { theme, ...otherPrefs } = merged;
console.log(`Theme: ${theme}`);
console.log(`Other:`, otherPrefs);
```

---

## Practical Application: Inventory Tracker

> 🎯 **Teach:** How to combine typed arrays and objects to build a realistic data processing program. **See:** An inventory tracker that calculates total value, finds the most expensive item, and groups items by category using reduce. **Feel:** That arrays, tuples, and objects are not just theory — they power real applications.

### Program E: inventory.ts

Build a typed inventory tracker:

```typescript
const inventory: {
    name: string;
    price: number;
    stock: number;
    category: string;
}[] = [
    { name: "Laptop", price: 999.99, stock: 25, category: "electronics" },
    { name: "Headphones", price: 79.99, stock: 100, category: "electronics" },
    { name: "Notebook", price: 4.99, stock: 500, category: "office" },
    { name: "Pen", price: 1.99, stock: 1000, category: "office" },
    { name: "Backpack", price: 49.99, stock: 75, category: "accessories" },
];

// Total inventory value
const totalValue = inventory.reduce((sum, item) => sum + item.price * item.stock, 0);
console.log(`Total inventory value: $${totalValue.toFixed(2)}`);

// Most expensive item
const mostExpensive = inventory.reduce((max, item) => item.price > max.price ? item : max);
console.log(`Most expensive: ${mostExpensive.name} ($${mostExpensive.price})`);

// Group by category
const byCategory = inventory.reduce<Record<string, typeof inventory>>((groups, item) => {
    const key = item.category;
    groups[key] = groups[key] || [];
    groups[key].push(item);
    return groups;
}, {});

for (const [category, items] of Object.entries(byCategory)) {
    console.log(`\n${category.toUpperCase()}:`);
    items.forEach(item => console.log(`  ${item.name}: $${item.price} (${item.stock} in stock)`));
}
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to apply arrays, tuples, objects, spread, and destructuring through hands-on coding. **See:** Five exercises that build progressively from basic typed arrays to a full inventory tracker. **Feel:** Capable of writing each program independently, cementing every concept from this module.

> ✏️ Sharpen Your Pencil

1. Write `arrays.ts` with typed arrays of numbers, strings, and booleans. Use `map`, `filter`, `reduce`, spread, and destructuring.
2. Write `tuples.ts` with basic tuples, labeled tuples, optional tuple elements, and a function that returns a tuple.
3. Write `objects.ts` with inline object types demonstrating optional properties, readonly properties, and nested objects.
4. Write `spread_destructure.ts` showing object destructuring (with rename), spread for copying/merging, and rest syntax.
5. Write `inventory.ts` — a typed array of product objects. Calculate total value, find the most expensive item, and group items by category.

---

> 💡 **Remember this one thing:** Arrays hold collections of the same type; tuples are fixed-length with specific types at each position.

---

## Up Next

> 🎯 **Teach:** What comes next in the learning path and how it builds on data structures. **See:** A preview of Module 3's focus on typed function signatures, parameters, and function types. **Feel:** Eager to learn how to type the behavior that operates on your data.

In **Module 3: Functions**, you will learn how to type function parameters, return values, optional and default parameters, arrow functions, and function type aliases — making your functions as safe as your data.
