# Python for Java Developers - Key Differences & Nuances

This guide highlights important Python language internals and nuances that differ from Java.

---

## 1. Dynamic Typing vs Static Typing

### Java (Static Typing)
```java
String name = "John";  // Type declared explicitly
int age = 30;
List<String> items = new ArrayList<>();
```

### Python (Dynamic Typing)
```python
name = "John"  # Type inferred at runtime
age = 30
items = []  # Can hold any type

# Type hints (optional, for documentation/IDE support)
name: str = "John"
age: int = 30
items: list[str] = []
```

**Python Nuance**: Variables can change type at runtime!
```python
x = 5        # x is int
x = "hello"  # Now x is str - totally valid!
```

---

## 2. Everything is an Object

### Java
Primitives vs Objects: `int` vs `Integer`, `boolean` vs `Boolean`

### Python
Everything is an object - even functions, classes, and modules!

```python
# Functions are objects
def greet():
    return "Hello"

# You can assign functions to variables
my_func = greet
print(my_func())  # Prints: Hello

# Even integers are objects
x = 5
print(x.__class__)  # <class 'int'>
print(dir(x))  # See all methods on integer!
```

**Python Nuance**: This enables powerful metaprogramming and introspection.

---

## 3. No Interfaces or Abstract Classes (Sort of)

### Java
```java
public interface Repository {
    void save(Object obj);
}

public class IngredientRepository implements Repository {
    public void save(Object obj) { ... }
}
```

### Python
Python uses "duck typing" - if it walks like a duck and quacks like a duck, it's a duck!

```python
# No interface needed - just implement the methods
class IngredientRepository:
    def save(self, obj):
        pass

# Python 3+ has ABC (Abstract Base Classes) if you want:
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def save(self, obj):
        pass
```

**Python Philosophy**: "We're all consenting adults here" - trust developers to follow conventions.

---

## 4. No Access Modifiers (public/private/protected)

### Java
```java
private String secretKey;
protected int count;
public String getName() { ... }
```

### Python
```python
# Convention: prefix with _ for "internal" use
_secret_key = "abc123"  # "Please don't use this externally"
__very_private = "xyz"  # Name mangling (see below)

# Everything is accessible!
def get_name(self):
    return self.name
```

**Python Nuance**:
- Single underscore `_var`: Convention for "internal use"
- Double underscore `__var`: Name mangling (becomes `_ClassName__var`)

```python
class MyClass:
    def __init__(self):
        self.__private = "secret"

    def get_private(self):
        return self.__private  # Works inside class

obj = MyClass()
# obj.__private  # AttributeError!
obj._MyClass__private  # Works but VERY discouraged!
```

---

## 5. Memory Management - No Manual Garbage Collection

### Java
```java
// Garbage collection is automatic, but you can suggest
System.gc();  // Suggest GC run
```

### Python
Python uses **reference counting** + garbage collector

```python
import sys

x = [1, 2, 3]
print(sys.getrefcount(x))  # Shows reference count

# When ref count hits 0, memory is freed immediately
# Cyclic references are handled by garbage collector
```

**Python Nuance**: CPython uses reference counting, so objects are freed as soon as there are no references. Circular references are cleaned up by periodic GC.

---

## 6. The Global Interpreter Lock (GIL)

This is a BIG difference from Java!

### Java
True multi-threading - threads run in parallel on multiple CPU cores

### Python (CPython)
The GIL allows only ONE thread to execute Python bytecode at a time!

```python
import threading

# These won't run in parallel (CPU-bound tasks)
def cpu_task():
    sum(range(10000000))

t1 = threading.Thread(target=cpu_task)
t2 = threading.Thread(target=cpu_task)
t1.start()
t2.start()
# Only one thread executes Python at a time!
```

**Solutions**:
1. **multiprocessing**: Use separate processes (no GIL)
2. **async/await**: For I/O-bound tasks
3. **Use C extensions**: NumPy, etc. release the GIL

```python
# For CPU-intensive work, use multiprocessing
from multiprocessing import Process

p1 = Process(target=cpu_task)
p2 = Process(target=cpu_task)
# These run in parallel!
```

---

## 7. List/Dictionary Comprehensions

### Java
```java
List<Integer> squares = new ArrayList<>();
for (int i = 0; i < 10; i++) {
    squares.add(i * i);
}
```

### Python
```python
# List comprehension
squares = [i * i for i in range(10)]

# Dictionary comprehension
squares_dict = {i: i * i for i in range(10)}

# With conditions
even_squares = [i * i for i in range(10) if i % 2 == 0]
```

**Python Nuance**: Comprehensions are faster than loops and more Pythonic!

---

## 8. Multiple Inheritance & Method Resolution Order (MRO)

### Java
Single inheritance + interfaces

### Python
Full multiple inheritance with C3 linearization (MRO)

```python
class A:
    def method(self):
        return "A"

class B(A):
    def method(self):
        return "B"

class C(A):
    def method(self):
        return "C"

class D(B, C):  # Multiple inheritance
    pass

d = D()
print(d.method())  # Which method is called?
print(D.__mro__)  # See method resolution order
# (<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
```

**Python Nuance**: MRO ensures a consistent order for method lookup using C3 linearization algorithm.

---

## 9. Decorators (Like Annotations, But Different)

### Java
```java
@Override
@Transactional
public void save() { ... }
```

### Python
Decorators are functions that wrap other functions!

```python
def my_decorator(func):
    def wrapper():
        print("Before function")
        result = func()
        print("After function")
        return result
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# Equivalent to: say_hello = my_decorator(say_hello)

say_hello()
# Output:
# Before function
# Hello!
# After function
```

**Common Use Cases**:
```python
@staticmethod  # Like static in Java
@classmethod   # Receives class, not instance
@property      # Getter without parentheses
@abstractmethod
```

---

## 10. Context Managers (`with` statement)

### Java
```java
try (FileReader reader = new FileReader("file.txt")) {
    // Use reader
} // Automatically closed
```

### Python
```python
# with statement ensures cleanup
with open("file.txt") as f:
    content = f.read()
# File automatically closed here

# You can create your own:
class MyResource:
    def __enter__(self):
        print("Acquire resource")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Release resource")

with MyResource() as r:
    print("Using resource")
```

---

## 11. Mutable Default Arguments (GOTCHA!)

### Java
```java
public void add(List<String> items) {
    if (items == null) {
        items = new ArrayList<>();  // New list each time
    }
}
```

### Python
**DANGEROUS GOTCHA**:
```python
def add_item(item, items=[]):  # DEFAULT IS SHARED!
    items.append(item)
    return items

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2] - WHAT?!
print(add_item(3))  # [1, 2, 3] - Same list!
```

**Correct Way**:
```python
def add_item(item, items=None):
    if items is None:
        items = []  # New list each time
    items.append(item)
    return items
```

**Python Nuance**: Default arguments are evaluated ONCE at function definition time, not each call!

---

## 12. `self` is Explicit

### Java
```java
public class Person {
    private String name;

    public void setName(String name) {
        this.name = name;  // 'this' optional if no conflict
    }
}
```

### Python
```python
class Person:
    def __init__(self, name):
        self.name = name  # 'self' is ALWAYS required

    def set_name(self, name):
        self.name = name  # Must use self
```

**Why?** Makes it explicit what's an instance variable vs local variable.

---

## 13. Generators & Lazy Evaluation

### Java
```java
Stream<Integer> numbers = IntStream.range(0, 1000000).boxed();
// Similar to generators
```

### Python
```python
# Generator function (lazy evaluation)
def count_up_to(n):
    i = 0
    while i < n:
        yield i  # Pause here, resume later
        i += 1

# Only generates values as needed!
for num in count_up_to(1000000):
    if num > 10:
        break  # Only generated 11 values, not 1 million!

# Generator expression (like list comprehension)
squares = (i * i for i in range(1000000))  # No memory used yet!
```

**Python Nuance**: Generators are memory-efficient for large datasets.

---

## 14. Unpacking & Multiple Return Values

### Java
```java
// Need to create a class or use array
public int[] divide(int a, int b) {
    return new int[]{a / b, a % b};
}

int[] result = divide(10, 3);
int quotient = result[0];
int remainder = result[1];
```

### Python
```python
# Can return multiple values naturally
def divide(a, b):
    return a // b, a % b  # Returns tuple

# Unpack directly
quotient, remainder = divide(10, 3)

# Works with lists, tuples, etc.
first, *rest, last = [1, 2, 3, 4, 5]
# first = 1, rest = [2, 3, 4], last = 5
```

---

## 15. Monkey Patching (Dynamic Modification)

### Java
Classes are sealed at compile time

### Python
You can modify classes at runtime!

```python
class Dog:
    def speak(self):
        return "Woof!"

# Add a new method at runtime!
def bark_loudly(self):
    return "WOOF WOOF!"

Dog.bark = bark_loudly

dog = Dog()
print(dog.bark())  # WOOF WOOF!
```

**When is this useful?**
- Testing (mock objects)
- Extending third-party libraries
- BUT: Use with caution! Can make code hard to understand.

---

## Key Takeaways for Java Developers

1. **Embrace duck typing** - No need for interfaces everywhere
2. **Trust conventions** - No private/public, use `_` prefix instead
3. **Understand the GIL** - Use multiprocessing for CPU-bound parallelism
4. **Watch for mutable defaults** - Common gotcha!
5. **Everything is an object** - Even functions and classes
6. **Comprehensions are your friend** - More Pythonic than loops
7. **Context managers** - Use `with` for resource management
8. **Generators for large data** - Lazy evaluation saves memory

---

## Recommended Next Steps

1. Read PEP 8 (Python style guide)
2. Learn about `*args` and `**kwargs`
3. Understand list slicing: `list[start:end:step]`
4. Explore Python's rich standard library
5. Learn about `__str__`, `__repr__`, and other magic methods
6. Understand when to use lists vs tuples vs sets vs dicts
