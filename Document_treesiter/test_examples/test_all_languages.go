// Go example
package main

import "fmt"

// SimpleFunction returns a greeting
func SimpleFunction() string {
    return "Hello from Go"
}

// User represents a person
type User struct {
    Name string
}

// Greet returns a greeting
func (u *User) Greet() string {
    return fmt.Sprintf("Hello, %s!", u.Name)
}
