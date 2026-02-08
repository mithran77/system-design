# ACID Properties:

## Atomicity

- A transaction is treated as a single, indivisible unit.
- Either all operations within the transaction are completed successfully, or none of them are applied.
- If any part of the transaction fails, the entire transaction is rolled back to its initial state.
- Example: In a bank transfer, if money is debited from one account, it must also be credited to the other. If the credit operation fails, the debit must also be undone.

## Consistency

- A transaction must take the database from one valid state to another valid state, maintaining all defined rules, constraints, and relationships.
- This ensures that the database adheres to its schema, triggers, and referential integrity constraints.
- Example: If a database enforces that the balance in an account cannot be negative, a transaction reducing the balance must respect this rule.

## Isolation

- Transactions executed concurrently should not interfere with each other.
- Each transaction must behave as if it is the only one running, even if multiple transactions are executing at the same time.
- Isolation levels (e.g., Read Committed, Repeatable Read, Serializable) determine how much interaction is allowed between concurrent transactions.
- Example: If two transactions are reading and updating the same data simultaneously, isolation ensures that each transaction operates independently without affecting the outcome of the other.

## Durability

- Once a transaction is committed, its changes are permanent, even in the event of a system crash or power failure.
- Databases achieve durability through mechanisms like write-ahead logging and replication.
- Example: If a payment transaction is marked as complete, its details remain intact and recoverable even if the system crashes immediately afterward.

## Practical Examples:
- Many DB's use WAL to ensure ACID transactions (WAL is replayed to rebuild state)
- MySQL, PostgreSQL, and Oracle, but its principles are also relevant for NoSQL systems that require strong consistency
