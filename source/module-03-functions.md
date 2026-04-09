# Module 3: Functions

> 🏷️ Start Here

> 🎯 **Teach:** How to write fully typed function signatures — parameters, return types, and function types as values. **See:** Functions used as first-class values, passed as arguments, and returned from other functions. **Feel:** That functions in TypeScript are not just procedures — they are typed, composable building blocks.

> 🔄 **Where this fits:** Modules 0-2 covered types for data — variables, arrays, tuples, and objects. Now you learn to type the behavior that operates on that data. Functions are where types and logic meet, and typing them correctly is what makes TypeScript code safe to refactor and extend.

## Function Syntax

> 🎯 **Teach:** The core syntax for typing function parameters, return values, optional/default/rest parameters, and arrow functions. **See:** Named functions, arrow functions, and parameter variations — all with explicit type annotations. **Feel:** Grounded in the basic patterns you will use every time you write a typed function.

### The Basics

```typescript
// Named function with types
function add(a: number, b: number): number {
    return a + b;
}

// Arrow function
const multiply = (a: number, b: number): number => a * b;

// Optional parameter
function greet(name: string, greeting?: string): string {
    return `${greeting ?? "Hello"}, ${name}!`;
}

// Default parameter
function power(base: number, exponent: number = 2): number {
    return base ** exponent;
}

// Rest parameters
function sum(...numbers: number[]): number {
    return numbers.reduce((a, b) => a + b, 0);
}
```

![Anatomy of a TypeScript function — parameter types, return type, optional and default parameters](../images/module-03/function-anatomy.png)
*Anatomy of a TypeScript function — parameter types, return type, optional and default parameters*

## Function Types

> 🎯 **Teach:** How functions are first-class values with their own type signatures, and how to create type aliases for function types. **See:** Function type annotations, type aliases like `MathOp`, and the distinction between `void` and `never` return types. **Feel:** That functions are not just procedures — they are typed values you can assign, pass, and compose.

### Functions as Values

> 🎙️ In TypeScript, functions are first-class values. That means you can assign a function to a variable, pass it as an argument to another function, and return it from a function — just like you would with a number or a string. The key insight is that functions have types, just like data does. A function type describes the shape of the function: what parameters it accepts and what it returns. You can create type aliases for function types, which makes your code cleaner and lets you reuse the same signature in multiple places.

```typescript
// Function type annotation
let operation: (a: number, b: number) => number;
operation = add;
operation = multiply;
// operation = greet;  // Error: signature doesn't match

// Type alias for function types
type MathOp = (a: number, b: number) => number;
const subtract: MathOp = (a, b) => a - b;
```

### Void vs Never

```typescript
function log(msg: string): void { console.log(msg); }  // Returns undefined
function fail(msg: string): never { throw new Error(msg); } // Never returns
```

---

## Basic Functions

> 🎯 **Teach:** How to write and call fully typed functions with different parameter and return types. **See:** Five functions — add, isEven, reverse, maxOfThree, repeat — each with explicit parameter and return type annotations. **Feel:** Comfortable writing typed functions from scratch and testing them with console output.

### Program A: basic_functions.ts

Write typed functions and call each one:

```typescript
function add(a: number, b: number): number {
    return a + b;
}

function isEven(n: number): boolean {
    return n % 2 === 0;
}

function reverse(s: string): string {
    return s.split("").reverse().join("");
}

function maxOfThree(a: number, b: number, c: number): number {
    return Math.max(a, b, c);
}

function repeat(text: string, times: number): string {
    return text.repeat(times);
}

// Test them all
console.log(`add(3, 4) = ${add(3, 4)}`);
console.log(`isEven(7) = ${isEven(7)}`);
console.log(`reverse("TypeScript") = ${reverse("TypeScript")}`);
console.log(`maxOfThree(5, 9, 3) = ${maxOfThree(5, 9, 3)}`);
console.log(`repeat("ha", 3) = ${repeat("ha", 3)}`);
```

---

## Optional, Default, and Rest Parameters

> 🎯 **Teach:** How optional (`?`), default (`= value`), and rest (`...args`) parameters make functions flexible while staying type-safe. **See:** Functions that omit arguments, use defaults, accept variable-length argument lists, and combine all three patterns. **Feel:** Confident designing function signatures that are both flexible and safe.

### Program B: parameters.ts

```typescript
// Optional parameter
function createUser(name: string, email?: string): string {
    if (email) {
        return `${name} <${email}>`;
    }
    return name;
}

console.log(createUser("Campbell"));
console.log(createUser("Campbell", "campbell@example.com"));

// Default parameter
function formatCurrency(amount: number, currency: string = "USD", decimals: number = 2): string {
    return `${amount.toFixed(decimals)} ${currency}`;
}

console.log(formatCurrency(42.5));
console.log(formatCurrency(42.5, "EUR"));
console.log(formatCurrency(42.5, "JPY", 0));

// Rest parameters
function average(...nums: number[]): number {
    return nums.reduce((a, b) => a + b, 0) / nums.length;
}

console.log(`Average: ${average(10, 20, 30, 40, 50)}`);

// Combining all three
function buildUrl(
    base: string,
    path: string = "/",
    ...queryParams: string[]
): string {
    let url = `${base}${path}`;
    if (queryParams.length > 0) {
        url += `?${queryParams.join("&")}`;
    }
    return url;
}

console.log(buildUrl("https://api.example.com"));
console.log(buildUrl("https://api.example.com", "/users"));
console.log(buildUrl("https://api.example.com", "/search", "q=typescript", "page=1"));
```

---

## Arrow Functions and Callbacks

> 🎯 **Teach:** How arrow functions work as callbacks in higher-order functions like map, filter, reduce, and sort — with types flowing automatically. **See:** Arrow functions passed to array methods, typed comparators for sorting, and a custom higher-order function that accepts a callback. **Feel:** Fluent with the functional programming patterns that make TypeScript code concise and expressive.

### Higher-Order Functions

> 🎙️ A higher-order function is a function that takes another function as a parameter or returns a function as its result. This is one of the most powerful patterns in TypeScript. Array methods like map, filter, and reduce are higher-order functions — they take a callback function that you provide. TypeScript types flow through these seamlessly: when you call `numbers.filter(n => n > 5)`, TypeScript knows `n` is a number because `numbers` is a `number[]`. You get full type safety inside your callbacks without writing a single annotation.

### Program C: arrows.ts

```typescript
// Arrow function variations
const double = (n: number): number => n * 2;
const greet = (name: string): string => `Hello, ${name}!`;
const isPositive = (n: number): boolean => n > 0;

// Arrow functions shine as callbacks
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

const evens = numbers.filter(n => n % 2 === 0);
const squared = numbers.map(n => n ** 2);
const sum = numbers.reduce((acc, n) => acc + n, 0);

console.log(`Evens: ${evens}`);
console.log(`Squared: ${squared}`);
console.log(`Sum: ${sum}`);

// Sorting with typed comparators
const words = ["banana", "apple", "cherry", "date"];
const sorted = [...words].sort((a, b) => a.localeCompare(b));
const byLength = [...words].sort((a, b) => a.length - b.length);

console.log(`Alphabetical: ${sorted}`);
console.log(`By length: ${byLength}`);

// Higher-order function
function applyOperation(a: number, b: number, op: (x: number, y: number) => number): number {
    return op(a, b);
}

console.log(`Add: ${applyOperation(10, 5, (a, b) => a + b)}`);
console.log(`Multiply: ${applyOperation(10, 5, (a, b) => a * b)}`);
console.log(`Power: ${applyOperation(2, 10, (a, b) => a ** b)}`);
```

---

## Function Types

> 🎯 **Teach:** How to define reusable function type aliases and use them to type parameters, variables, and return values. **See:** Type aliases like `Predicate`, `Transform`, and `Combiner` used to type filter functions, and a factory function that returns a new function. **Feel:** That function types are a powerful abstraction — you can describe the shape of behavior just like you describe the shape of data.

### Program D: function_types.ts

```typescript
// Function type alias
type Predicate = (value: number) => boolean;
type Transform = (value: string) => string;
type Combiner = (a: number, b: number) => number;

// Use function types
const isEven: Predicate = n => n % 2 === 0;
const isPositive: Predicate = n => n > 0;
const toUpper: Transform = s => s.toUpperCase();
const add: Combiner = (a, b) => a + b;

// Function that accepts function types
function filterNumbers(nums: number[], predicate: Predicate): number[] {
    return nums.filter(predicate);
}

const data = [-3, -1, 0, 2, 4, 7, 8, 11];
console.log(`Evens: ${filterNumbers(data, isEven)}`);
console.log(`Positives: ${filterNumbers(data, isPositive)}`);
console.log(`Even AND positive: ${filterNumbers(data, n => isEven(n) && isPositive(n))}`);

// Returning functions
function createMultiplier(factor: number): (n: number) => number {
    return (n) => n * factor;
}

const triple = createMultiplier(3);
const tenX = createMultiplier(10);
console.log(`Triple 5: ${triple(5)}`);
console.log(`10x 7: ${tenX(7)}`);
```

---

## Practical Application: Calculator

> 🎯 **Teach:** How to combine function types, `Record`, and control flow to build a real calculator with typed operations. **See:** A `Record<string, Operation>` that maps operator strings to typed functions, with a `calculate` function dispatching to the correct operation. **Feel:** That typed functions and data structures work together to create clean, extensible programs.

### Program E: calculator.ts

Build a typed calculator with function types:

```typescript
type Operation = (a: number, b: number) => number;

const operations: Record<string, Operation> = {
    "+": (a, b) => a + b,
    "-": (a, b) => a - b,
    "*": (a, b) => a * b,
    "/": (a, b) => {
        if (b === 0) throw new Error("Division by zero");
        return a / b;
    },
    "**": (a, b) => a ** b,
    "%": (a, b) => a % b,
};

function calculate(a: number, op: string, b: number): number {
    const operation = operations[op];
    if (!operation) {
        throw new Error(`Unknown operator: ${op}`);
    }
    return operation(a, b);
}

// Test all operations
const tests: [number, string, number][] = [
    [10, "+", 5],
    [10, "-", 3],
    [4, "*", 7],
    [20, "/", 4],
    [2, "**", 8],
    [17, "%", 5],
];

for (const [a, op, b] of tests) {
    console.log(`${a} ${op} ${b} = ${calculate(a, op, b)}`);
}
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to apply function syntax, parameter patterns, arrow functions, function types, and real-world composition through hands-on practice. **See:** Five exercises building from basic typed functions to a full calculator application. **Feel:** Capable of writing each program independently, solidifying every function concept from this module.

> ✏️ Sharpen Your Pencil

1. Write `basic_functions.ts` with at least 5 typed functions (different parameter types and return types). Call each one and log the result.
2. Write `parameters.ts` demonstrating optional parameters, default parameters, rest parameters, and a function that combines all three.
3. Write `arrows.ts` using arrow functions as callbacks with `filter`, `map`, `reduce`, and `sort`. Write a higher-order function that accepts a callback.
4. Write `function_types.ts` with type aliases for function types. Write a function that accepts a function parameter and one that returns a function.
5. Write `calculator.ts` using a `Record<string, Operation>` to map operator strings to typed functions. Test all operations.

---

> 💡 **Remember this one thing:** Functions are first-class values in TypeScript — you can type them, pass them, and return them just like data.

---

## Up Next

> 🎯 **Teach:** What comes next in the learning path and how it builds on typed functions. **See:** A preview of Module 4's focus on conditionals, loops, and type narrowing through control flow. **Feel:** Eager to learn how TypeScript uses your logic to get smarter about types.

In **Module 4: Control Flow**, you will learn how TypeScript uses conditionals, loops, and iteration methods — and how control flow enables type narrowing, where TypeScript tracks what type a variable could be at each point in your code.
