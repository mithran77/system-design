# Database Indexes

## What is the importance of Indexes?
- Purpose
    - Efficiency in Reads: Reduces read complexity from O(n) to O(logn) or O(1).
    - Trade-off with Writes: Writes are slower for tree-based indexes due to the additional O(logn) time needed to update the index.
- Characteristics of Tree-Based Indexes
  - Makes database tables sorted based on the indexed column:
    - O(logn) for reads.
    - O(logn) for range queries.
- Types of Indexes
    - Simple Indexes: Based on a single column/field.
    - Composite Indexes: Span multiple columns/fields.
    - Clustered Indexes: Represent the entire row for efficient access.
- Relevance to Modern Databases
    - Applicable to both SQL and NoSQL databases.
    - In modern applications, read speed is often prioritized over write speed:
      - Slower writes are acceptable to achieve faster read performance.

## What logs does a RDBMS store?
1. **Transaction-Related Logs**
- Write-Ahead Log (WAL): Ensures recoverability by recording changes before applying them.
- REDO Logs: Reapply changes during recovery to maintain consistency.
- UNDO Logs: Rollback transactions for data integrity.

2. **Performance and Query Logs**
- Query Logs: Records all executed queries for analysis.
- Slow Query Logs: Highlights inefficient or time-consuming queries.

3. **System and Maintenance Logs**
- Binary Logs: (e.g., MySQL) Logs changes for replication or recovery.
- Checkpoint Logs: Snapshots the database state to reduce recovery time.

4. **Monitoring and Debugging Logs**
- Error Logs: Records system errors and warnings.
- Debug Logs: Provides detailed technical data for troubleshooting.

5. **Security and Compliance Logs**
- General Activity Logs: Tracks user actions like logins and administrative tasks for security and auditing.
- Audit Logs: Records detailed actions for compliance and security analysis.

6. **Replication Logs**
- Logs changes shared between master and replica databases to ensure data consistency in distributed systems.


## How to Repopulate DB indexes?
- We typically use the WAL,
  - To avoid the overhead of scanning entire databases
  - Scanning is done when building **all** indexes
  - WAL has the most recent DB data
  - Also allows incremental rebuilds from checkpoint or recent changes

## Referenes:
- https://www.youtube.com/@hnasr

