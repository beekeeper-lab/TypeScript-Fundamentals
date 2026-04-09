# Module 4: Control Flow

> 🏷️ Start Here

> 🎯 **Teach:** How conditionals, loops, and iteration methods work in TypeScript — and how control flow enables type narrowing. **See:** TypeScript tracking what type a variable could be at each branch of an if/else or switch. **Feel:** That control flow is not just about logic — it is how TypeScript gets smarter about your types.

> 🔄 **Where this fits:** Modules 0-3 covered data types and functions. Now you learn the structures that make decisions and repeat work. Control flow is where TypeScript's type narrowing truly shines — the compiler uses your if/else checks and switch statements to automatically narrow union types, eliminating the need for manual type assertions.

## Type Narrowing Through Control Flow

> 🎯 **Teach:** How TypeScript uses your if/else and switch logic to automatically narrow union types — no manual casts needed. **See:** A function that accepts `string | number` where TypeScript knows the exact type inside each branch of an if/else. **Feel:** That control flow is not just about logic — it is how TypeScript gets smarter about your types at each point in the code.

> 🎙️ TypeScript control flow is identical to JavaScript in syntax, but TypeScript does something remarkable with it: it uses your control flow to narrow types. When you have a value that could be a string or a number, and you write an if statement checking `typeof value === "string"`, TypeScript knows that inside that if block the value is definitely a string. This is not a cast or an assertion — it is the compiler following your logic and deducing what the type must be. This is one of TypeScript's most powerful features, and it works with if/else, switch, ternary operators, and more.

```typescript
function process(value: string | number) {
    if (typeof value === "string") {
        console.log(value.toUpperCase()); // TS knows it's a string here
    } else {
        console.log(value.toFixed(2));    // TS knows it's a number here
    }
}
```

## Loops Overview

> 🎯 **Teach:** The five loop constructs available in TypeScript — `for...of`, `for...in`, traditional `for`, `while`, and `forEach` — and when to use each. **See:** A quick-reference showing the syntax for each loop type. **Feel:** Clear on which loop to reach for in different situations.

```typescript
// for...of — iterate values (preferred)
for (const item of array) { }

// for...in — iterate keys/indices (use with caution)
for (const key in object) { }

// Traditional for
for (let i = 0; i < 10; i++) { }

// while
while (condition) { }

// forEach (array method)
array.forEach((item, index) => { });
```

---

## Conditionals

> 🎯 **Teach:** How to use if/else, ternary operators, nullish coalescing (`??`), optional chaining (`?.`), and switch statements in TypeScript. **See:** A grade classifier, null-safe value access, and a day-type switch — all fully typed. **Feel:** Comfortable with every conditional pattern and confident handling null/undefined safely.

### Program A: conditionals.ts

```typescript
// if / else if / else
function classifyGrade(score: number): string {
    if (score >= 90) return "A";
    else if (score >= 80) return "B";
    else if (score >= 70) return "C";
    else if (score >= 60) return "D";
    else return "F";
}

const testScores = [95, 82, 74, 61, 55];
for (const score of testScores) {
    console.log(`${score} → ${classifyGrade(score)}`);
}

// Ternary operator
const age = 20;
const status = age >= 18 ? "adult" : "minor";
console.log(`Age ${age}: ${status}`);

// Nullish coalescing (??)
const input: string | null = null;
const value = input ?? "default";
console.log(`Value: ${value}`);

// Optional chaining (?.)
const user: { name: string; address?: { city: string } } = { name: "Campbell" };
console.log(`City: ${user.address?.city ?? "unknown"}`);

// switch statement
function dayType(day: string): string {
    switch (day.toLowerCase()) {
        case "monday":
        case "tuesday":
        case "wednesday":
        case "thursday":
        case "friday":
            return "weekday";
        case "saturday":
        case "sunday":
            return "weekend";
        default:
            return "invalid day";
    }
}

console.log(`Monday: ${dayType("Monday")}`);
console.log(`Saturday: ${dayType("Saturday")}`);
```

---

## Loops

> 🎯 **Teach:** How to iterate over arrays, object keys, and numeric ranges using TypeScript's loop constructs, including `break` and `continue`. **See:** `for...of` with `entries()`, traditional countdowns, while-based Fibonacci, `for...in` over object keys, and control flow with `break`/`continue`. **Feel:** Fluent with every loop pattern and ready to choose the right one for any iteration task.

### Program B: loops.ts

```typescript
// for...of — iterating values
const languages = ["TypeScript", "Python", "Java", "Dart"];
console.log("Languages:");
for (const lang of languages) {
    console.log(`  - ${lang}`);
}

// for...of with index using entries()
console.log("\nWith index:");
for (const [i, lang] of languages.entries()) {
    console.log(`  ${i + 1}. ${lang}`);
}

// Traditional for loop
console.log("\nCountdown:");
for (let i = 10; i > 0; i--) {
    process.stdout.write(`${i} `);
}
console.log("Go!");

// while loop
let fib1 = 0, fib2 = 1;
console.log("\nFibonacci < 100:");
while (fib1 < 100) {
    process.stdout.write(`${fib1} `);
    [fib1, fib2] = [fib2, fib1 + fib2];
}
console.log();

// for...in — iterate object keys
const scores: Record<string, number> = {
    Alice: 88,
    Bob: 92,
    Charlie: 76,
};
console.log("\nScores:");
for (const name in scores) {
    console.log(`  ${name}: ${scores[name]}`);
}

// break and continue
console.log("\nOdd numbers 1-20 (skip 13):");
for (let i = 1; i <= 20; i++) {
    if (i % 2 === 0) continue;
    if (i === 13) {
        console.log("  (skipping unlucky 13)");
        continue;
    }
    process.stdout.write(`${i} `);
}
console.log();
```

---

## Array Iteration Methods

> 🎯 **Teach:** How to use `map`, `filter`, `reduce`, `find`, `some`, `every`, `includes`, and method chaining as a typed data processing pipeline. **See:** Each array method demonstrated individually, then chained together into a single expression with TypeScript tracking types through every step. **Feel:** That functional array methods are often cleaner and safer than manual loops — and TypeScript makes them even better.

### Method Chaining

> 🎙️ Array iteration methods — map, filter, reduce, find, some, every — are the functional programming toolkit built into JavaScript and fully typed by TypeScript. The real power comes from chaining them together. When you write `numbers.filter(n => n % 2 === 0).map(n => n ** 2).reduce((sum, n) => sum + n, 0)`, you are building a data processing pipeline. Each step transforms the data and TypeScript tracks the types through every link in the chain. This is often cleaner and safer than writing manual loops.

### Program C: iteration.ts

![Array iteration methods — map transforms, filter selects, reduce accumulates](../images/module-04/iteration-methods.png)
*Array iteration methods — map transforms, filter selects, reduce accumulates*

```typescript
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// forEach
console.log("forEach:");
numbers.forEach((n, i) => console.log(`  [${i}] = ${n}`));

// map — transform each element
const squares = numbers.map(n => n ** 2);
console.log(`\nSquares: ${squares}`);

// filter — keep elements matching condition
const evens = numbers.filter(n => n % 2 === 0);
console.log(`Evens: ${evens}`);

// reduce — accumulate to single value
const sum = numbers.reduce((acc, n) => acc + n, 0);
console.log(`Sum: ${sum}`);

// find — first match
const firstOver5 = numbers.find(n => n > 5);
console.log(`First > 5: ${firstOver5}`);

// findIndex — index of first match
const indexOver5 = numbers.findIndex(n => n > 5);
console.log(`Index of first > 5: ${indexOver5}`);

// some / every — boolean checks
const hasNegative = numbers.some(n => n < 0);
const allPositive = numbers.every(n => n > 0);
console.log(`Has negative: ${hasNegative}`);
console.log(`All positive: ${allPositive}`);

// includes
console.log(`Includes 7: ${numbers.includes(7)}`);

// Chaining methods
const result = numbers
    .filter(n => n % 2 === 0)       // Keep evens: [2, 4, 6, 8, 10]
    .map(n => n ** 2)                // Square them: [4, 16, 36, 64, 100]
    .reduce((sum, n) => sum + n, 0); // Sum: 220
console.log(`\nSum of squared evens: ${result}`);
```

---

## Practical Application: Data Processor

> 🎯 **Teach:** How to combine typed interfaces, filtering, grouping, sorting, and reduce to process a real dataset. **See:** A student dataset filtered by major and GPA, averaged by group, sorted for a Dean's list, and counted by grade level. **Feel:** That control flow and iteration methods together make TypeScript a powerful tool for real data processing.

### Program D: data_processor.ts

Process a dataset using typed control flow and iteration:

```typescript
interface Student {
    name: string;
    grade: number;
    major: string;
    gpa: number;
}

const students: Student[] = [
    { name: "Alice", grade: 12, major: "CS", gpa: 3.9 },
    { name: "Bob", grade: 11, major: "Math", gpa: 3.2 },
    { name: "Charlie", grade: 12, major: "CS", gpa: 3.7 },
    { name: "Diana", grade: 10, major: "English", gpa: 3.5 },
    { name: "Eve", grade: 12, major: "CS", gpa: 3.1 },
    { name: "Frank", grade: 11, major: "Math", gpa: 2.8 },
    { name: "Grace", grade: 10, major: "CS", gpa: 3.6 },
    { name: "Hank", grade: 12, major: "English", gpa: 3.4 },
];

// 1. Filter: CS majors with GPA >= 3.5
const topCS = students.filter(s => s.major === "CS" && s.gpa >= 3.5);
console.log("Top CS students:", topCS.map(s => s.name));

// 2. Average GPA by major
const majors = [...new Set(students.map(s => s.major))];
for (const major of majors) {
    const majorStudents = students.filter(s => s.major === major);
    const avgGpa = majorStudents.reduce((sum, s) => sum + s.gpa, 0) / majorStudents.length;
    console.log(`${major} average GPA: ${avgGpa.toFixed(2)}`);
}

// 3. Dean's list (GPA >= 3.5), sorted by GPA descending
const deansList = students
    .filter(s => s.gpa >= 3.5)
    .sort((a, b) => b.gpa - a.gpa);
console.log("\nDean's List:");
deansList.forEach((s, i) => console.log(`  ${i + 1}. ${s.name} (${s.gpa})`));

// 4. Count by grade level using reduce
const byGrade = students.reduce<Record<number, number>>((counts, s) => {
    counts[s.grade] = (counts[s.grade] || 0) + 1;
    return counts;
}, {});
console.log("\nStudents per grade:", byGrade);
```

---

## Sharpen Your Pencil

> 🎯 **Teach:** How to apply conditionals, loops, iteration methods, and data processing through hands-on coding. **See:** Four exercises building from conditional logic to a full data processor with filtering, grouping, and sorting. **Feel:** Capable of writing each program independently, cementing every control flow concept from this module.

> ✏️ Sharpen Your Pencil

1. Write `conditionals.ts` with if/else chains, ternary expressions, nullish coalescing (`??`), optional chaining (`?.`), and a switch statement.
2. Write `loops.ts` using `for...of`, `for...in`, a traditional for loop, a while loop, and `break`/`continue`.
3. Write `iteration.ts` exercising `forEach`, `map`, `filter`, `reduce`, `find`, `findIndex`, `some`, `every`, `includes`, and method chaining.
4. Write `data_processor.ts` with a typed array of objects. Filter by multiple criteria, compute averages by group, sort, and count by category using reduce.

---

> 💡 **Remember this one thing:** TypeScript uses control flow to narrow types — it tracks what type a variable could be at each point in your code.

---

## Up Next

> 🎯 **Teach:** What comes next in the learning path and how it builds on control flow and type narrowing. **See:** A preview of Module 5's focus on type aliases, union types, and intersection types. **Feel:** Eager to create reusable, flexible type definitions that make your code more expressive.

In **Module 5: Type Aliases and Unions**, you will learn how to create reusable type names with `type` aliases and combine types with union (`|`) and intersection (`&`) operators — the building blocks of flexible, expressive type definitions.
