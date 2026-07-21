# Python OOP Refresher

A ground-up walkthrough: classes → `self` → instance/class variables → encapsulation → inheritance → `super()` → polymorphism → abstraction → dunder methods → multiple inheritance → `*args`/`**kwargs`.

---

## 1. Classes and Objects — The Foundation

A **class** is a blueprint. An **object** (instance) is a concrete thing built from that blueprint.

```python
class Student:
    pass

s1 = Student()
s2 = Student()
print(s1 is s2)  # False — two separate objects, same blueprint
```

---

## 2. `self` — The Instance Talking About Itself

`self` is the first parameter of every instance method. It's how an object refers to *itself* — its own attributes and methods — as opposed to some other instance of the same class.

```python
class Student:
    def __init__(self, name, marks):
        self.name = name      # self.name belongs to THIS object
        self.marks = marks

    def greet(self):
        return f"Hi, I'm {self.name}"

s1 = Student("Benir", 85)
s2 = Student("Amina", 92)

print(s1.greet())  # Hi, I'm Benir
print(s2.greet())  # Hi, I'm Amina
```

**Key point:** `self` is not a keyword — it's just a convention (you could call it anything). Python automatically passes the object as the first argument whenever you call `instance.method()`. So `s1.greet()` is really `Student.greet(s1)` under the hood.

---

## 3. Instance Variables vs Class Variables

- **Instance variables**: unique to each object, usually set in `__init__` via `self.x`.
- **Class variables**: shared across *all* instances, defined directly inside the class body.

```python
class Student:
    school_name = "Strathmore University"   # class variable — shared by everyone
    total_students = 0                       # class variable used as a counter

    def __init__(self, name, marks):
        self.name = name        # instance variable — unique per object
        self.marks = marks      # instance variable
        Student.total_students += 1   # modify via the class, not self

s1 = Student("Benir", 85)
s2 = Student("Amina", 92)

print(s1.school_name)          # Strathmore University
print(s2.school_name)          # Strathmore University (same value, shared)
print(Student.total_students)  # 2

# Changing a class variable through the class affects everyone
Student.school_name = "Strathmore University - Main Campus"
print(s1.school_name)  # updated too, since it's shared

# But assigning via an instance creates a NEW instance variable that shadows the class one
s1.school_name = "Custom Campus"
print(s1.school_name)  # Custom Campus (only s1)
print(s2.school_name)  # Strathmore University - Main Campus (unaffected)
```

**Rule of thumb:** if a value should differ per object → instance variable. If it's shared/constant/global-to-the-class (like a counter or config) → class variable.

---

## 4. Encapsulation — Controlling Access to Data

Encapsulation means bundling data + behavior together, and restricting direct access to internal state. Python doesn't have true "private" like Java, but uses naming conventions:

| Prefix | Convention | Meaning |
|---|---|---|
| `name` | public | free to access |
| `_name` | protected (convention only) | "internal use, but accessible" |
| `__name` | private (name-mangled) | Python renames it to `_ClassName__name` to discourage outside access |

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance   # "private" — name-mangled

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient funds")

    def get_balance(self):
        return self.__balance

acc = BankAccount("Benir", 1000)
acc.deposit(500)
print(acc.get_balance())    # 1500

# print(acc.__balance)      # AttributeError — not directly accessible
print(acc._BankAccount__balance)  # 1500 — name mangling exposes the "real" name (don't do this in practice)
```

The point isn't that `__balance` is unbreakable — it's that direct access is *discouraged*, forcing interaction through controlled methods (`deposit`, `withdraw`, `get_balance`). This is the same principle you saw in Django's `ModelForm` — validated, controlled entry points instead of raw field manipulation.

### `@property` — a cleaner way to encapsulate

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance

    @property
    def balance(self):          # acts like an attribute, but is really a method
        return self.__balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = value

acc = BankAccount("Benir", 1000)
print(acc.balance)   # 1000 — looks like a plain attribute access
acc.balance = 2000    # goes through the setter, validated
```

---

## 5. Inheritance — Reusing and Extending Behavior

Inheritance lets a class (**child/subclass**) acquire attributes and methods from another class (**parent/superclass**).

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"I'm {self.name}, {self.age} years old."

class Student(Person):          # Student inherits from Person
    def __init__(self, name, age, student_id):
        super().__init__(name, age)   # more on super() next
        self.student_id = student_id

    def study(self):
        return f"{self.name} is studying."

s = Student("Benir", 21, "CS-2023-001")
print(s.introduce())  # inherited from Person
print(s.study())      # defined in Student
```

`Student` gets `introduce()` for free — no need to rewrite it.

---

## 6. The `super()` Keyword

`super()` gives you access to the parent class's methods — most commonly used to call the parent's `__init__()` so you don't duplicate its setup logic.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)   # delegates name/age setup to Person
        self.student_id = student_id  # Student adds its own extra attribute
```

Without `super()`, you'd have to repeat `self.name = name; self.age = age` manually inside `Student`, duplicating logic and violating DRY. `super()` also matters heavily once you get to **multiple inheritance** (section 9) because it respects Python's Method Resolution Order (MRO) rather than hardcoding a specific parent.

You can also use `super()` to *extend* a method rather than fully replace it:

```python
class Student(Person):
    def introduce(self):
        base = super().introduce()   # get the parent's version
        return base + " I'm a student."

s = Student("Benir", 21)
print(s.introduce())  # "I'm Benir, 21 years old. I'm a student."
```

---

## 7. Polymorphism — Same Interface, Different Behavior

Polymorphism means different classes can be used through the same interface, each responding in its own way to the same method call.

```python
class Animal:
    def speak(self):
        raise NotImplementedError

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())   # each object responds differently to the SAME method call
# Woof!
# Meow!
```

This is why you can loop over a list of different object types and call `.speak()` on each without checking `if isinstance(animal, Dog)` — Python figures out which version to run at call time (this is called **dynamic dispatch**).

Python also supports polymorphism informally via **duck typing**: "if it walks like a duck and quacks like a duck..." — you don't even need a shared parent class, just a shared method name.

```python
class Duck:
    def speak(self):
        return "Quack!"

def make_it_speak(thing):
    print(thing.speak())   # works for ANY object with a .speak() method

make_it_speak(Dog())
make_it_speak(Duck())
```

---

## 8. Abstraction — Hiding Implementation, Exposing Interface

Abstraction means defining *what* a class should do without necessarily specifying *how*, forcing subclasses to fill in the details. Python does this with the `abc` module.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass          # no implementation here — subclasses MUST provide one

    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

# shape = Shape()          # TypeError — can't instantiate an abstract class directly
rect = Rectangle(4, 5)
print(rect.area())         # 20
```

If `Rectangle` forgot to implement `perimeter()`, Python would raise a `TypeError` the moment you tried to instantiate it. This guarantees every subclass honors the "contract" — directly relevant to your ML roadmap: scikit-learn's own estimators follow this pattern (every model must implement `fit()` and `predict()`).

**Abstraction vs Encapsulation — the distinction that trips people up:**
- **Encapsulation** hides *data* (state) — e.g., `__balance`.
- **Abstraction** hides *implementation complexity* — e.g., you call `.area()` without needing to know the formula used internally.

---

## 9. Multiple Inheritance

A Python class can inherit from more than one parent class at once.

```python
class Flyer:
    def move(self):
        return "Flying"

class Swimmer:
    def move(self):
        return "Swimming"

class Duck(Flyer, Swimmer):   # inherits from BOTH
    pass

d = Duck()
print(d.move())   # "Flying" — Flyer comes first, so it wins
```

### Method Resolution Order (MRO)

When two parents define the same method, Python decides which one wins using the **MRO** — left-to-right order of inheritance, computed via the C3 linearization algorithm.

```python
print(Duck.__mro__)
# (<class 'Duck'>, <class 'Flyer'>, <class 'Swimmer'>, <class 'object'>)
```

`super()` in a multiple-inheritance setup walks *this* MRO chain, not just "the direct parent" — which is why `super()` is safer than hardcoding `Flyer.move(self)`.

```python
class Flyer:
    def move(self):
        return "Flying"

class Swimmer:
    def move(self):
        return "Swimming"

class Duck(Flyer, Swimmer):
    def move(self):
        return super().move() + " and also " + Swimmer.move(self)

d = Duck()
print(d.move())  # "Flying and also Swimming"
```

Multiple inheritance is powerful but can get tangled fast (the classic "diamond problem"). In practice, Python code often prefers **mixins** — small, focused parent classes meant to be combined — over deep multiple-inheritance trees. Django's own CBVs (`ListView`, `CreateView`, etc.) are themselves built from mixins layered via multiple inheritance.

---

## 10. Dunder Methods (Magic Methods)

"Dunder" = **d**ouble **under**score, e.g. `__init__`, `__str__`. These let your objects hook into Python's built-in syntax and functions (`print()`, `+`, `len()`, `==`, etc.) instead of needing custom method names.

```python
class Book:
    def __init__(self, title, pages):
        self.title = title
        self.pages = pages

    def __str__(self):
        # controls what print(obj) / str(obj) shows — human-readable
        return f"'{self.title}' ({self.pages} pages)"

    def __repr__(self):
        # controls what you see in the shell/debugger — unambiguous, dev-facing
        return f"Book(title={self.title!r}, pages={self.pages})"

    def __len__(self):
        # lets len(obj) work
        return self.pages

    def __eq__(self, other):
        # lets == work
        return self.title == other.title and self.pages == other.pages

    def __add__(self, other):
        # lets + work — combine two books into a "collection" page count
        return self.pages + other.pages

b1 = Book("Automata Theory", 320)
b2 = Book("Automata Theory", 320)

print(b1)          # 'Automata Theory' (320 pages)   <- __str__
print(len(b1))      # 320                              <- __len__
print(b1 == b2)     # True                              <- __eq__
print(b1 + b2)       # 640                              <- __add__
```

Some other common dunders worth knowing:

| Dunder | Triggered by |
|---|---|
| `__init__` | object creation (`Book(...)`) |
| `__str__` / `__repr__` | `print()`, `str()`, shell display |
| `__len__` | `len(obj)` |
| `__eq__`, `__lt__`, `__gt__` | `==`, `<`, `>` |
| `__getitem__` | `obj[key]` (indexing) |
| `__iter__` / `__next__` | `for x in obj:` |
| `__call__` | `obj()` — makes an instance callable like a function |

---

## 11. `*args` and `**kwargs`

Both let a function/method accept a **variable number of arguments** — the difference is positional vs keyword.

### `*args` — variable positional arguments (packed into a tuple)

```python
def add_all(*args):
    print(args)          # tuple, e.g. (1, 2, 3)
    return sum(args)

print(add_all(1, 2, 3))       # 6
print(add_all(5, 10, 15, 20)) # 50 — works with ANY number of arguments
```

### `**kwargs` — variable keyword arguments (packed into a dict)

```python
def build_profile(**kwargs):
    print(kwargs)   # dict, e.g. {'name': 'Benir', 'age': 21}
    return kwargs

build_profile(name="Benir", age=21, course="CS")
# {'name': 'Benir', 'age': 21, 'course': 'CS'}
```

### Combined, in the standard order: `positional, *args, **kwargs`

```python
def create_student(name, *args, **kwargs):
    print("Name:", name)
    print("Extra positional:", args)
    print("Extra keyword:", kwargs)

create_student("Benir", "CS-2023-001", 21, gpa=3.8, campus="Nairobi")
# Name: Benir
# Extra positional: ('CS-2023-001', 21)
# Extra keyword: {'gpa': 3.8, 'campus': 'Nairobi'}
```

### Where this matters most in OOP: flexible `super().__init__()` calls

```python
class Person:
    def __init__(self, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)   # pass along whatever's left to the next class in MRO

class Employee:
    def __init__(self, salary, **kwargs):
        self.salary = salary
        super().__init__(**kwargs)

class Manager(Person, Employee):
    def __init__(self, name, salary, team_size, **kwargs):
        self.team_size = team_size
        super().__init__(name=name, salary=salary, **kwargs)

m = Manager(name="Benir", salary=90000, team_size=5)
print(m.name, m.salary, m.team_size)  # Benir 90000 5
```

This pattern — each class only handling its own kwargs and forwarding the rest — is exactly how cooperative multiple inheritance is meant to work, and it's also why Django's own class-based views accept `**kwargs` so liberally in `as_view()` and `get_context_data()`.

**Quick distinction table:**

| | `*args` | `**kwargs` |
|---|---|---|
| Collects | positional arguments | keyword arguments |
| Stored as | tuple | dict |
| Called like | `func(1, 2, 3)` | `func(a=1, b=2)` |
| Access | `args[0]`, `args[1]`... | `kwargs['a']`, `kwargs['b']`... |

*(Note: `args` and `kwargs` are just conventional names — the `*` and `**` are what actually matter syntactically. You could write `*vals, **opts` and it would work identically.)*

---

## Putting It All Together

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    company_name = "EduPredict Ltd"   # class variable, shared
    total_employees = 0

    def __init__(self, name, salary):
        self.name = name              # instance variable
        self.__salary = salary        # encapsulated (private via name-mangling)
        Employee.total_employees += 1

    @property
    def salary(self):
        return self.__salary

    @abstractmethod
    def role_description(self):       # abstraction — subclasses MUST implement
        pass

    def __str__(self):                # dunder method
        return f"{self.name} ({self.role_description()})"

class Developer(Employee):
    def __init__(self, name, salary, language, *skills, **extra_info):
        super().__init__(name, salary)   # super() — reuse parent init
        self.language = language
        self.skills = skills             # *args packed into tuple
        self.extra_info = extra_info     # **kwargs packed into dict

    def role_description(self):          # polymorphism — overrides parent's abstract method
        return f"Developer working in {self.language}"

dev = Developer("Benir", 80000, "Python", "Django", "ML", level="Junior", remote=True)
print(dev)                     # uses __str__ + role_description (polymorphism)
print(dev.salary)              # via @property, not direct __salary access
print(dev.skills)              # ('Django', 'ML')
print(dev.extra_info)          # {'level': 'Junior', 'remote': True}
print(Employee.total_employees)  # 1
```

This single example threads together every concept above: class vs instance variables, `self`, encapsulation via `@property`, abstraction via `ABC`, inheritance + `super()`, polymorphism via the overridden `role_description()`, a dunder method (`__str__`), and both `*args`/`**kwargs`.
