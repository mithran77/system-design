<b>Snapshot Isolation</b> (SI) is a concurrency control mechanism in databases that provides a consistent view of the database to each transaction, based on the state of the database at the time the transaction begins. It uses multi-version concurrency control (MVCC) to achieve this, meaning each transaction works with a "snapshot" of the database rather than directly interacting with the latest data.

## How Snapshot Isolation Works
1. <b>Snapshot View:</b> When a transaction begins, it gets a snapshot of the database as it existed at that moment. This snapshot is isolated from changes made by other transactions.
2. <b>Reads:</b> Transactions always read data from their own snapshot, ensuring consistency during the transaction's execution.
3. <b>Writes:</b>
    - Transactions can modify data, but the changes are not visible to other transactions until the transaction commits.
    - During the commit, the database checks for write conflicts.

## Write Conflicts
Snapshot Isolation prevents write-write conflicts:

- If two transactions modify the same row:
    - The first transaction to commit succeeds.
    - The second transaction fails and must be retried (or aborted).
This ensures no <b>dirty writes</b> occur.

## Key Features
1. <b>Prevents Dirty Reads:</b> Transactions do not see uncommitted changes from other transactions.
2. <b>Prevents Non-Repeatable Reads:</b> Each transaction sees a consistent snapshot of the database.
3. <b>Phantom Reads: Not prevented.</b> New rows inserted by another transaction may appear if they do not affect the snapshot of the querying transaction.


## Comparison with Other Isolation Levels

| Feature |	Snapshot Isolation | Repeatable Read | Serializable | 
| -------- |	-------- | -------- | -------- | 
| Dirty Reads | Prevented | Prevented | Prevented | 
| Non-Repeatable Reads | Prevented | Prevented | Prevented | 
| Phantom Reads | Allowed | Allowed | Prevented | 
| Concurrency | High (uses MVCC) | Medium | Low (due to strict locking) | 
| Write Conflicts | Detected at commit time | Not explicitly detected | Prevented entirely | 


## Example Scenario
Consider a bank application where two transactions run concurrently:

- Initial Balance:

    - Account A: $100.
    - Account B: $200.
- Transaction 1 (T1): Reads the balance of Account A and transfers $50 from Account A to Account B.

- Transaction 2 (T2): Reads the balance of Account A and transfers $30 from Account A to Account B.

- Under Snapshot Isolation:

    - T1 sees Account A's initial balance as $100 (its snapshot).
    - T2 also sees Account A's initial balance as $100 (its snapshot).
    - Writes are checked for conflicts:
        - If T1 commits first, the new balance of Account A is $50.
        - T2 will fail to commit because it tries to modify a row that T1 already modified.
This ensures consistency and avoids data corruption.

## Advantages
1. <b>High Concurrency:</b> Allows many transactions to proceed without blocking each other.
2. <b>Consistency:</b> Provides a stable view of the database, ensuring repeatable reads.
3. <b>Efficiency:</b> MVCC minimizes locking and contention.


## Disadvantages
1. <b>Write Skew:</b> Can occur when transactions read and write related rows, leading to inconsistency if not properly handled.
2. <b>Phantom Reads:</b> SI does not prevent phantom reads, so it is not fully serializable.


## When to Use Snapshot Isolation
- Applications requiring high concurrency and consistent reads.
- Scenarios where write-write conflicts are rare or acceptable to retry.
- Common in systems using MVCC databases like PostgreSQL, MySQL (InnoDB), or Microsoft SQL Server.

Snapshot Isolation strikes a balance between performance and consistency, making it a popular choice in many modern database systems.




<b>Write Skew</b> is a phenomenon in databases where multiple transactions, under certain isolation levels (such as Snapshot Isolation), independently modify different rows based on overlapping reads, leading to an inconsistent or unintended final state. This issue arises because the transactions operate on a consistent snapshot but do not lock the rows they read.