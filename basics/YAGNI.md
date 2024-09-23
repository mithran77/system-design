# YAGNI Refresher

> Always implement things when you need them, not when you forsee that you need them

Rationale is that every line of code comes with a cost, It needs to be developed, tested, maintained & understood by other developers.
```
Over Engineered

def process_payment(self, amount, method, ...):
    if method == "credit_card":
        # ... credit card handling
    elif method == "bitcoin":
        # ... bitcoin handling
    elif method == "paypal":
        # ... paypal handling
```
Here we start by adding only the method we need, if future requirements demand bitcoin or paypal, we will add it then
```
YAGNI compliant

def process_payment(self, amount, method, ...):
    if method == "credit_card":
        # ... credit card handling
```
### Benefits
* Avoid wasting time/effort on unecessary code
* Smaller & simple codebase easier to add to, update and maintain
* Focus only on reqs means faster development times

### When NOT to use
* If we know certain features are definitely coming, might be wise to build some basic support in advance for them
* Sometimes where performance/scalibility are important, it might be better to write anticipatory code earlier than later, to avoid risk of introducing bugs.
