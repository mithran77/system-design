<b>Read Committed</b> is one of the isolation levels in database systems that determines how transactions interact with each other when accessing the same data. It ensures a moderate level of isolation, providing a balance between consistency and performance.
The same level of consistency can be implmented by using row level write locks. But it is far more performance efficient to store the older comitted value and serve it to reads, while a commit is in progress.

## Key Characteristics of Read Committed:

1. <b>Prevention of Dirty Reads:</b>
   - A transaction will only read data that has been committed by other transactions.
   - It avoids reading data that is uncommitted and may be rolled back, ensuring data consistency for the reading transaction.

2. <b>Non-Repeatable Reads Can Occur</b>:
   - A transaction might read the same data twice and get different values if another transaction modifies and commits that data in between the two reads.
   - This is because Read Committed does not prevent changes to data by other transactions during a transaction's execution.

3. <b>Does Not Prevent Phantom Reads</b>:
   - Read Committed does not address the issue of phantom rows, where a transaction sees a different set of rows when executing the same query multiple times due to inserts or deletes by other transactions.


## Example: Dirty Read Prevention

### Scenario:
   - Transaction A: Updates a row but does not commit the change.
   - Transaction B: Tries to read the same row.
### In Read Committed Isolation:
   - Transaction B will not see the uncommitted changes made by Transaction A.
   - It will either read the row’s original (committed) value or wait until Transaction A commits or rolls back.


## Example: Non-Repeatable Read

### Scenario:
   - Transaction A: Starts and reads a value (e.g., Balance = 100).
  - Transaction B: Updates the value to Balance = 200 and commits.
  - Transaction A: Reads the value again and sees Balance = 200.
### In Read Committed Isolation:
   - Transaction A will observe different values for the same data because it only ensures that data read is committed, not that it remains unchanged during the transaction.


## Advantages of Read Committed:
   - <b>Performance</b>: More efficient than higher isolation levels like Repeatable Read or Serializable because it allows greater concurrency.
   - <b>Consistency</b>: Avoids dirty reads, ensuring that only committed data is accessed.

## Disadvantages of Read Committed:
- <b>Non-Repeatable Reads</b>: A transaction may see inconsistent results when reading the same data multiple times.
- <b>Phantom Reads</b>: New rows added by other transactions may appear in subsequent queries within the same transaction.



## Use Cases:
  - Suitable for applications that can tolerate minor inconsistencies (e.g., reporting, monitoring dashboards).
  - Not ideal for systems requiring strict consistency, such as financial systems or inventory management.


## Implementation:
Most relational databases, such as PostgreSQL, Oracle, and SQL Server, use Read Committed as the default isolation level. However, it can be explicitly set using SQL statements like:

<code>SET TRANSACTION ISOLATION LEVEL READ COMMITTED;</code>

## Addiio