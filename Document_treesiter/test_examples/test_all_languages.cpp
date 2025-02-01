/**
 * C++ example
 */

#include <string>

void simpleFunction() {
    // Simple function
}

class TestClass {
public:
    /**
     * Constructor
     */
    TestClass(const std::string& name) : name_(name) {}

    /**
     * Return a greeting
     */
    std::string greet() {
        return "Hello, " + name_ + "!";
    }

private:
    std::string name_;
};
