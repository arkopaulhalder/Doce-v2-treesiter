//! Rust example

/// Simple function returns a greeting
pub fn simple_function() -> String {
    "Hello from Rust".to_string()
}

/// User struct
pub struct User {
    name: String,
}

impl User {
    /// Create a new user
    pub fn new(name: String) -> Self {
        User { name }
    }

    /// Return a greeting
    pub fn greet(&self) -> String {
        format!("Hello, {}!", self.name)
    }
}
