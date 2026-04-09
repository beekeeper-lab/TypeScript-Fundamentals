# Module 8: Generics

## Introduction

> 🏷️ Useful Soon

> 🎙️ Generics are the key to writing reusable code in TypeScript without sacrificing type safety. Without generics, you'd have two choices: write a separate function for every type, or use any and lose all type checking. Generics give you a third option -- write the code once with a type parameter, and let TypeScript fill in the concrete type each time you use it. The type parameter is like a variable, but for types instead of values. Today you'll write generic functions, generic interfaces, generic classes, and you'll learn how to constrain generic types so they only accept values with the right shape.

> 🎯 **Teach:** How to write generic functions, interfaces, classes, and constraints in TypeScript.
> **See:** Type parameters preserving type information through function calls, generic classes like Stack and Store that work with any type, and constraints that limit what types are allowed.
> **Feel:** That generics are not complicated -- they're just type-level parameters -- and that they unlock code reuse without losing safety.

> 🔄 **Where this fits:** You've learned types, interfaces, and classes. Generics add a new dimension: parameterizing those constructs over types. The ApiResponse interface from Module 6 already used a generic parameter -- now you'll understand exactly how that works.

## Why Generics Matter

> 🎯 **Teach:** The fundamental problem generics solve -- writing reusable code without losing type information. **See:** A side-by-side comparison of `any`-based functions that lose type info versus generic functions that preserve it, plus a constraint example with `{ length: number }`. **Feel:** That generics are not magic -- they are simply type-level parameters that let TypeScript track types through your code automatically.

> 🎙️ Here's the core problem generics solve. Without generics, a function that returns the first element of an array either has to be written separately for numbers, strings, and every other type -- or it uses any, which means TypeScript forgets the type completely. With a generic type parameter T, you write the function once. When you call it with a number array, TypeScript knows the return type is number. When you call it with a string array, TypeScript knows the return type is string. You get full type safety and full reuse.

```typescript
// Without generics — loses type info
function first(arr: any[]): any { return arr[0]; }

// With generics — preserves type info
function first<T>(arr: T[]): T | undefined { return arr[0]; }

const num = first([1, 2, 3]);      // TypeScript knows: number
const str = first(["a", "b"]);     // TypeScript knows: string
```

### Generic Constraints

```typescript
function getLength<T extends { length: number }>(item: T): number {
    return item.length; // T must have a .length property
}

getLength("hello");     // OK — string has length
getLength([1, 2, 3]);   // OK — array has length
// getLength(42);        // Error — number has no length
```

## Generic Functions

> 🎯 **Teach:** How to declare type parameters on functions using angle brackets, and how TypeScript infers them from arguments. **See:** `identity<T>`, `pair<A, B>`, `swap`, `toArray`, and `findFirst` -- progressively more useful generic functions with single and multiple type parameters. **Feel:** That writing a generic function is as simple as adding `<T>` and using T where you would have used a concrete type -- TypeScript handles the rest through inference.

> 🎙️ The angle brackets after the function name declare a type parameter. You can name it anything, but single uppercase letters are conventional -- T for the primary type, A and B when you have two, K and V for key-value pairs. TypeScript usually infers the type parameter from the arguments you pass, so you rarely need to specify it explicitly. The identity function below is the simplest possible generic -- it just returns what you give it, but with the type preserved.

### Program A: generic_functions.ts

```typescript
// Identity function
function identity<T>(value: T): T {
    return value;
}
console.log(identity<string>("hello"));
console.log(identity(42)); // Type inferred as number

// Pair
function pair<A, B>(first: A, second: B): [A, B] {
    return [first, second];
}
const p = pair("age", 20); // [string, number]
console.log(p);

// Wrap in array
function toArray<T>(value: T): T[] {
    return [value];
}
console.log(toArray("hello")); // string[]
console.log(toArray(42));      // number[]

// Swap tuple
function swap<A, B>(tuple: [A, B]): [B, A] {
    return [tuple[1], tuple[0]];
}
console.log(swap(["hello", 42])); // [42, "hello"]

// Find in array
function findFirst<T>(arr: T[], predicate: (item: T) => boolean): T | undefined {
    for (const item of arr) {
        if (predicate(item)) return item;
    }
    return undefined;
}

const nums = [1, 2, 3, 4, 5];
const firstEven = findFirst(nums, n => n % 2 === 0);
console.log(`First even: ${firstEven}`);

const words = ["apple", "banana", "cherry"];
const longWord = findFirst(words, w => w.length > 5);
console.log(`First long word: ${longWord}`);
```

## Generic Interfaces and Types

> 🎯 **Teach:** How to parameterize interfaces and type aliases with generic type parameters for reusable data structures. **See:** A `Result<T>` interface for success/failure wrapping, `KeyValuePair<K, V>` with two type parameters, and a `MapFn<T, U>` type alias for transformation functions. **Feel:** That generic interfaces are the foundation of typed library design -- you define the shape once and reuse it with any data type.

> 🎙️ Generics aren't limited to functions. You can parameterize interfaces and type aliases too. The Result interface below is a pattern you'll see constantly -- it wraps a success or failure with a typed data field. When you call success with a user object, the return type is Result with the user type filled in. The KeyValuePair and MapFn types show how generic type aliases work the same way.

### Program B: generic_types.ts

```typescript
// Generic interface
interface Result<T> {
    success: boolean;
    data: T | null;
    error?: string;
}

function success<T>(data: T): Result<T> {
    return { success: true, data };
}

function failure<T>(error: string): Result<T> {
    return { success: false, data: null, error };
}

const userResult = success({ name: "Alice", age: 25 });
const errorResult = failure<string>("Not found");

console.log(userResult);
console.log(errorResult);

// Generic with multiple types
interface KeyValuePair<K, V> {
    key: K;
    value: V;
}

const entry1: KeyValuePair<string, number> = { key: "age", value: 25 };
const entry2: KeyValuePair<number, string> = { key: 1, value: "first" };

// Generic type alias for a map function
type MapFn<T, U> = (item: T) => U;

const stringLength: MapFn<string, number> = s => s.length;
const numToString: MapFn<number, string> = n => n.toString();

console.log(stringLength("hello")); // 5
console.log(numToString(42));       // "42"
```

## Generic Classes

> 🎯 **Teach:** How to build reusable, type-safe data structures using generic classes with one or more type parameters. **See:** A `Stack<T>` class with push/pop/peek that works with any type, and a `Store<K, V>` class that wraps a typed `Map`. **Feel:** That generic classes are how real libraries build data structures -- you write the logic once and get full type safety for every concrete type you use it with.

> 🎙️ Generic classes let you build reusable data structures. The Stack class below works with any type -- you create a Stack of numbers, a Stack of strings, or a Stack of anything. The type parameter T flows through every method: push takes a T, pop returns a T or undefined, and toArray returns a T array. The Store class goes further with two type parameters, K and V, creating a typed wrapper around a Map. These patterns show up constantly in libraries and frameworks.

### Program C: generic_classes.ts

```typescript
class Stack<T> {
    private items: T[] = [];

    push(item: T): void {
        this.items.push(item);
    }

    pop(): T | undefined {
        return this.items.pop();
    }

    peek(): T | undefined {
        return this.items[this.items.length - 1];
    }

    get size(): number {
        return this.items.length;
    }

    isEmpty(): boolean {
        return this.items.length === 0;
    }

    toArray(): T[] {
        return [...this.items];
    }
}

// Number stack
const numStack = new Stack<number>();
numStack.push(1);
numStack.push(2);
numStack.push(3);
console.log(`Top: ${numStack.peek()}, Size: ${numStack.size}`);
console.log(`Popped: ${numStack.pop()}`);
console.log(`Stack: ${numStack.toArray()}`);

// String stack
const strStack = new Stack<string>();
strStack.push("hello");
strStack.push("world");
console.log(`String stack: ${strStack.toArray()}`);

// Generic key-value store
class Store<K, V> {
    private data = new Map<K, V>();

    set(key: K, value: V): void { this.data.set(key, value); }
    get(key: K): V | undefined { return this.data.get(key); }
    has(key: K): boolean { return this.data.has(key); }
    delete(key: K): boolean { return this.data.delete(key); }
    get size(): number { return this.data.size; }

    entries(): [K, V][] { return [...this.data.entries()]; }
}

const userStore = new Store<number, { name: string; email: string }>();
userStore.set(1, { name: "Alice", email: "alice@example.com" });
userStore.set(2, { name: "Bob", email: "bob@example.com" });

console.log(`\nUser 1: ${userStore.get(1)?.name}`);
console.log(`Store size: ${userStore.size}`);
```

## Generic Constraints

> 🎯 **Teach:** How to limit generic type parameters using `extends` constraints, `keyof` for property access, and default type parameters. **See:** `T extends HasLength` requiring a `.length` property, `K extends keyof T` ensuring valid property names, and `Container<T = string>` with a default type. **Feel:** That constraints are the guardrails that make generics practical -- they let you require exactly the capabilities you need without over-restricting.

> 🎙️ Sometimes any type is too permissive. Constraints let you say "T can be anything, as long as it has these properties." The extends keyword in a generic parameter adds a constraint. T extends HasLength means T must have a length property. K extends keyof T means K must be one of T's property names. You can also set default types, so callers don't have to specify the type parameter if the default is fine.

> ✏️ Sharpen Your Pencil

### Program D: constraints.ts

```typescript
// Constrain to types with length
interface HasLength {
    length: number;
}

function logWithLength<T extends HasLength>(item: T): T {
    console.log(`Length: ${item.length}, Value: ${item}`);
    return item;
}

logWithLength("hello");
logWithLength([1, 2, 3]);
// logWithLength(42);  // Error: number doesn't have length

// Constrain to object keys
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user = { name: "Alice", age: 25, email: "alice@example.com" };
const name = getProperty(user, "name");   // string
const age = getProperty(user, "age");     // number
// getProperty(user, "phone");             // Error: "phone" is not a key

console.log(`${name}, ${age}`);

// Constrain to comparable
function maxItem<T extends { valueOf(): number }>(items: T[]): T {
    return items.reduce((max, item) => item.valueOf() > max.valueOf() ? item : max);
}

console.log(`Max: ${maxItem([3, 1, 4, 1, 5, 9])}`);

// Default generic type
interface Container<T = string> {
    value: T;
}

const strContainer: Container = { value: "hello" };       // T defaults to string
const numContainer: Container<number> = { value: 42 };
```

> 💡 **Remember this one thing:** Generics let you write code that works with any type while maintaining full type safety.

## Up Next

> 🎯 **Teach:** Where you are headed next and how enums and utility types build on the type system you now understand. **See:** A preview of named constants with enums and type transformations like `Partial`, `Pick`, `Omit`, and `Record`. **Feel:** Ready to learn the final set of type-level tools that will let you reshape existing types without rewriting them.

In **Module 9: Enums and Utility Types**, you'll learn how to define named constants with enums and how to transform existing types using TypeScript's built-in utility types like Partial, Pick, Omit, and Record.
