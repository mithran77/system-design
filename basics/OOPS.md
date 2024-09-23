# OOPS Refresher


## 1. Classes and Objects

A class is a template or blueprint for properties and behaviours of an object.
An object is a single instance of a class

```
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def start(self):
        print(self.make + " " + self.model + " is starting.")

swift = Car("Suzuki", "Swift", 2023)
city = Car("Honda", "City", 2015)

swift.start()
city.start()
```

## 2. Encapsulation

Hiding implementaiton of object behaviour and internal state to protect from incorrect external referencing or misuse.
Only necessary information is exposed through public interfaces **(methods)**

```
class BankAccount:
    def __init__(self, account_number):
        self.__account_number = account_number
        self.__balance = balance
    
    def deposit(self, amount):
        self.__balance += amount
    
    def withdraw(self, amount):
        if self.__balance >= amount:
            self.__balance -= amount
        else:
            print("Insufficient funds.")
    
    def get_balance(self):
        reture self.__balance
```

## 3. Inheritance

A way for a class to inherit properties and methods from another class.
Referred to as **parent** and **child**.
Encourages code reuse and creates a hierarchical structure.

```
class Vehicle:
    def __init__(self, color):
        self.color = color
    
    def honk(self):
        print("Honk honk!")

class Car:
    def __init__(self, color, speed):
        super().__init__(color)
        self.speed = speed
    
    def accelerate(self):
    self.speed += 10

my_car = Car("white", 20)
my_car.honk()
my_car.accelerate()
```

## 4. Polymorphism

Ability to write generic code for objects of different classes that implement the same method (interface).

Method Overriding: Subclass implements a method defined in a parent class.

```
class Document:
    def display(self):
        raise NotImplementedError("Needs to be defined in subclass")

class PDF:
    def display(self):
        print("")

class Doc:
    def display(self):
        print("")

docs = [PDF(), Doc()]

for doc in docs:
    doc.dosplay()
```

## 5. Abstraction

Concept of showing only necessary information outside while maintaining all other details hidden.
Here implementation specifics are hidden and only the interface defined by ABC is exposed.

```
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, height, width):
        self.height = height
        self.width = width
    
    def area(self):
        return self.height * self.width

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius
```
