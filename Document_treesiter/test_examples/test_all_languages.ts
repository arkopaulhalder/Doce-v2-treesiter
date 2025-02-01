/**
 * TypeScript example
 */

function simpleFunction(): string {
    return "Hello from TypeScript YaY";
}

class TestClass {
    constructor(private name: string) {}

    greet(): string {
        return `Hello, ${this.name}!`;
    }
}
