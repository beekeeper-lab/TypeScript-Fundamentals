# Module 1: Variables and Types

> 🏷️ Start Here

> 🎯 **Teach:** The vocabulary of TypeScript's type system — primitives, special types, and inference. **See:** How TypeScript infers types automatically and how explicit annotations add clarity. **Feel:** Comfortable choosing when to annotate and when to let TypeScript figure it out.

> 🔄 **Where this fits:** Module 0 showed you that TypeScript adds types to JavaScript. Now you learn what those types actually are. This vocabulary is the foundation for every module that follows — you cannot type arrays, functions, or objects without knowing these primitives first.

## Variable Declarations

> 🎯 **Teach:** The difference between `let` and `const`, and the full set of primitive types TypeScript provides. **See:** A reference table of every primitive type with examples and usage notes. **Feel:** Grounded in the basic vocabulary needed to declare and type any variable.

### let vs const

```typescript
let mutable: string = "can change";     // Mutable
const immutable: string = "cannot change"; // Immutable (like Java's final)
// var — avoid! Function-scoped, not block-scoped (legacy)
```

### The Primitive Types

| Type | Example | Notes |
|------|---------|-------|
| `string` | `"hello"` | Text — always lowercase `string`, not `String` |
| `number` | `42`, `3.14` | All numbers (no int/float distinction) |
| `boolean` | `true`, `false` | Lowercase, not `Boolean` |
| `null` | `null` | Intentional absence of value |
| `undefined` | `undefined` | Variable declared but not assigned |
| `any` | anything | Opt out of type checking (avoid!) |
| `unknown` | anything | Safe version of `any` (must check type before use) |
| `void` | — | Function returns nothing |
| `never` | — | Function never returns (throws or infinite loop) |

![TypeScript type hierarchy — primitives at the base, special types branching off](../images/module-01/type-hierarchy.png)
*TypeScript type hierarchy — primitives at the base, special types branching off*

---

## Type Inference

> 🎯 **Teach:** How TypeScript's inference engine automatically determines types from assigned values — and when `const` produces literal types. **See:** Variables declared without annotations where TypeScript correctly infers the type, including the difference between `let` and `const` inference. **Feel:** Relieved that you do not have to annotate everything — TypeScript is smarter than you might expect.

### How TypeScript Reads Your Mind

> 🎙️ One of the most important things to understand about TypeScript is that you do not have to annotate every single variable. TypeScript has a powerful type inference engine that looks at the value you assign and figures out the type automatically. When you write `let age = 20`, TypeScript knows that is a number. When you use `const`, TypeScript goes even further — it infers a literal type, because a const can never change. The rule of thumb is simple: let TypeScript infer when it can, and annotate when it cannot or when you want to be explicit for clarity.

```typescript
let name = "Campbell";    // TypeScript infers: string
let age = 20;             // TypeScript infers: number
let active = true;        // TypeScript infers: boolean

// const gets a more specific type (literal type)
const pi = 3.14159;       // TypeScript infers: 3.14159 (not just number)
const lang = "TypeScript"; // TypeScript infers: "TypeScript" (not just string)
```

Rule of thumb: **Let TypeScript infer when it can. Annotate when it can't or when you want to be explicit.**

---

## Type Annotations in Practice

> 🎯 **Teach:** How to write explicit type annotations and when they add value over inference. **See:** A program declaring variables with annotations for strings, numbers, booleans, and union types — plus what happens when you assign the wrong type. **Feel:** Comfortable writing annotations by hand and understanding the error messages when types conflict.

### Program A: annotations.ts

Write a program that declares variables with explicit type annotations:

```typescript
// Explicit annotations
let firstName: string = "Campbell";
let lastName: string = "Reed";
let age: number = 20;
let gpa: number = 3.8;
let isStudent: boolean = true;
let middleName: string | null = null;  // Can be string or null

console.log(`Name: ${firstName} ${lastName}`);
console.log(`Age: ${age}, GPA: ${gpa}`);
console.log(`Student: ${isStudent}`);
console.log(`Middle name: ${middleName ?? "N/A"}`);

// Type inference — no annotation needed
let city = "Austin";         // inferred as string
let zipCode = 78701;         // inferred as number
let enrolled = true;         // inferred as boolean

console.log(`City: ${city}, ZIP: ${zipCode}, Enrolled: ${enrolled}`);
```

Then demonstrate what happens when you try to reassign a wrong type:

```typescript
// age = "twenty";  // Uncomment to see the error
// isStudent = 1;   // Uncomment — number is not boolean
```

---

## const vs let

> 🎯 **Teach:** The mutability rules for `let` and `const`, including the subtle point that `const` prevents reassignment but not mutation of objects and arrays. **See:** Code that reassigns `let` variables, fails to reassign `const` variables, and successfully mutates `const` objects and arrays. **Feel:** Clear on when to use `const` (the default) versus `let`, and why `const` does not mean "immutable."

### Program B: const_vs_let.ts

```typescript
// let — can be reassigned
let score = 100;
score = 95;
console.log(`Score: ${score}`);

// const — cannot be reassigned
const maxScore = 100;
// maxScore = 200;  // Error: Cannot assign to 'maxScore'

// const with objects — the reference is constant, but properties can change
const person = {
    name: "Campbell",
    age: 20,
};
person.age = 21;         // OK — modifying a property
// person = { ... };     // Error — can't reassign the variable

console.log(`${person.name}, age ${person.age}`);

// const with arrays — same idea
const grades: number[] = [88, 92, 76];
grades.push(95);         // OK — modifying the array
// grades = [];          // Error — can't reassign the variable
console.log(`Grades: ${grades}`);
```

---

## Special Types

> 🎯 **Teach:** The purpose and behavior of `null`, `undefined`, `any`, `unknown`, `void`, and `never` — and why `unknown` is safer than `any`. **See:** Code exercising each special type, including a type guard that narrows `unknown` before use. **Feel:** Confident choosing the right special type for each situation and understanding why `any` should be avoided.

### The any vs unknown Distinction

> 🎙️ TypeScript has two types that accept any value: `any` and `unknown`. They look similar but behave very differently. Using `any` is like turning off the type checker — you can do anything with the value and TypeScript will not complain. Using `unknown` is the safe alternative — TypeScript forces you to check what type the value actually is before you can use it. Prefer `unknown` over `any` whenever you are dealing with values whose type you do not know at compile time. It keeps the safety net intact.

### Program C: special_types.ts

```typescript
// null and undefined
let nothing: null = null;
let notSet: undefined = undefined;
let maybeName: string | undefined = undefined;
maybeName = "Campbell";
console.log(`Maybe: ${maybeName}`);

// any — disables type checking (avoid when possible)
let flexible: any = 42;
flexible = "now a string";
flexible = true;
console.log(`Flexible: ${flexible}`);

// unknown — safe alternative to any
let mystery: unknown = 42;
// let num: number = mystery;  // Error! Must check type first
if (typeof mystery === "number") {
    let num: number = mystery;  // OK after type check
    console.log(`Mystery number: ${num}`);
}

// void — function that returns nothing
function logMessage(msg: string): void {
    console.log(msg);
    // no return statement
}
logMessage("This function returns void");

// never — function that never returns
function throwError(message: string): never {
    throw new Error(message);
}
// throwError("This always throws");  // Uncomment to test
```

---

## Template Literals and String Operations

> 🎯 **Teach:** How to use template literals for string interpolation and the most common string methods available in TypeScript. **See:** Backtick strings with embedded expressions, plus methods like `trim`, `toUpperCase`, `includes`, `split`, and `replace`. **Feel:** Fluent with string manipulation in TypeScript, ready to format output and process text.

### Program D: strings.ts

```typescript
const first = "Campbell";
const last = "Reed";
const age = 20;

// Template literals (backticks)
console.log(`Full name: ${first} ${last}`);
console.log(`In 10 years, ${first} will be ${age + 10}`);

// String methods (same as JavaScript)
const sentence = "  TypeScript is Amazing  ";
console.log(`Trimmed: "${sentence.trim()}"`);
console.log(`Upper: ${sentence.trim().toUpperCase()}`);
console.log(`Lower: ${sentence.trim().toLowerCase()}`);
console.log(`Includes 'Script': ${sentence.includes("Script")}`);
console.log(`Starts with '  Type': ${sentence.startsWith("  Type")}`);
console.log(`Length: ${sentence.trim().length}`);
console.log(`Replace: ${sentence.trim().replace("Amazing", "Awesome")}`);
console.log(`Split: ${sentence.trim().split(" ")}`);

// Multi-line strings
const multiLine = `
    This is a multi-line
    template literal in TypeScript.
    It preserves line breaks.
`;
console.log(multiLine);
```

---

## Type Inference Deep Dive

> 🎯 **Teach:** What TypeScript infers for various expressions — primitives, arrays, objects, literal types, and function return types. **See:** Variables without annotations where hovering in the IDE reveals exactly what TypeScript inferred, including literal types for `const`. **Feel:** Trust in TypeScript's inference so you annotate only when necessary.

### Program E: inference.ts

Demonstrate what TypeScript infers for various expressions:

```typescript
// Hover over each variable in your IDE to see the inferred type

let a = 42;                    // number
let b = "hello";              // string
let c = true;                 // boolean
let d = [1, 2, 3];            // number[]
let e = { x: 10, y: 20 };    // { x: number; y: number }
let f = Math.random() > 0.5;  // boolean

const g = 42;                  // 42 (literal type, not number)
const h = "hello";            // "hello" (literal type, not string)

// TypeScript infers return types too
function double(n: number) {   // Return type inferred as number
    return n * 2;
}

// Array inference
let mixed = [1, "two", true]; // (string | number | boolean)[]
console.log(`mixed types: ${mixed.map(v => typeof v)}`);

// Print the results
console.log(`a: ${a}, b: ${b}, c: ${c}`);
console.log(`d: ${d}, f: ${f}`);
console.log(`g: ${g}, h: ${h}`);
console.log(`double(21): ${double(21)}`);
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to apply the full range of variable and type concepts through hands-on coding. **See:** Five targeted exercises covering annotations, const/let, special types, string operations, and inference. **Feel:** Capable of writing each program independently, reinforcing every concept from this module.

> ✏️ Sharpen Your Pencil

1. Write `annotations.ts` with explicit type annotations for at least 6 variables of different types. Include a union type (`string | null`).
2. Write `const_vs_let.ts` demonstrating mutability rules — show that `const` prevents reassignment but not mutation of objects and arrays.
3. Write `special_types.ts` exercising `null`, `undefined`, `any`, `unknown`, `void`, and `never`. For `unknown`, show why you must check the type before using the value.
4. Write `strings.ts` using template literals and at least 5 different string methods.
5. Write `inference.ts` and hover over each variable in your IDE. For each one, write a comment noting what TypeScript inferred.

---

> 💡 **Remember this one thing:** Let TypeScript infer when it can. Annotate when it can't or when you want to be explicit.

---

## Up Next

> 🎯 **Teach:** What comes next in the learning path and how it builds on primitive types. **See:** A preview of Module 2's focus on arrays, tuples, and objects. **Feel:** Eager to combine primitives into real data structures.

In **Module 2: Arrays, Tuples, and Objects**, you will learn how to structure data with types — typed arrays for collections, tuples for fixed-length sequences, and object types for structured records.
