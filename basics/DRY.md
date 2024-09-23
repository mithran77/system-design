# DRY Refresher

> Every piece of knowledge must have a single, unambiguous, authoritative representation within a system

DRY encourages writing modular, reusable code primarily avoiding duplicating same functionality in multiple places.

```
def calculate_food_tax(price):
    tax_rate = 0.07
    return price * (1 + tax_rate)

def calculate_clothes_tax(price):
    tax_rate = 0.12
    return price * (1 + tax_rate)

def calculate_electronics_tax(price):
    tax_rate = 0.15
    return price * (1 + tax_rate)
```
the 3 functions can be made one and the taxes defined as constannts to be used elsewhere as well
```
FOOD_TAX = 0.07
CLOTHES_TAX = 0.12
ELECTRONICS_TAX = 0.15

def calculate_tax(price, tax):
    return price * (1 + tax)

food_tax = calculate_tax(100, FOOD_TAX)
clothes_tax = calculate_tax(100, CLOTHES_TAX)
electronics_tax = calculate_tax(100, ELECTRONICS_TAX)
```
Use of decorators also is a good way to DRY. logger decorator is applied to functions that need logging, reducing logging code.
```
def logger(func):
    def wrapper(*args, **kwargs):
        print("Calling " + func.__name__ + " with " + args + " and " + kwargs)
        return func(*args, **kwargs)

    return wrapper

@logger
def multiply(a, b):
    return a * b

@logger
def add(a, b):
    return a + b

multilply(5, 10)
add(2, 3)

```
### PROS:
* Reduce duplicate code
* Improve reusability
* Easier debugging & fixing
* Improved consistency
* Faster development

### How to apply:
* Identify & extract common code into reusable components
* Leverage libraries and frameworks
* Refactor regularly

### When not to apply
* Premature abstraction: Too early in the dev cycle (may lead to overengineering)
* Performance critical code: Some cases duplicating code can run faster
* Sacrificing readibility
* One time use
* Legacy or technical debt: Some cases may be better to duplicate code temporarily, rather than trying to refactor the entire system
* Debugging & Testing: Duplicating code sometimes can make it wasier to debug and test allowing for better isolation & control

