# Hash Indexes

## How do Hash Indexes work?
- A hashing function maps unique column values to specific indices in an array.
- The index stores references to table rows as a hashmap.
- Search Efficiency: Exact matches operate in O(1) time.
- Collision Handling:
  - Chaining: Uses a linked list to store values at the same index.
  - Probing: Searches for alternate slots:
    - Linear Probing: Sequentially searches for the next available spot. ((hash(x) + 2) % len(arr))
    - Quadratic Probing: Distributes collisions more evenly using a formula. ((hash(x) + 2*2) % len(arr))
  - REf: https://www.geeksforgeeks.org/open-addressing-collision-handling-technique-in-hashing/

## Disadvantages of Hash Indexes?
- Memory Limitations:
  - Stored in RAM, which is expensive and limited in capacity.
  - Hash index layout isn't contiguous, making disk-based storage inefficient.
- Durability Challenges:
  - RAM is non-persistent; recovery relies on WAL (Write-Ahead Log).
  - Write speeds are compromised due to necessary overheads of disk writes(WAL).
- Ineffectiveness for Ranged Queries:
  - Cannot optimize range-based lookups (e.g., rows starting with "A").
  - Linear scan of all keys in O(n) time is required

## PROS:
- O(1) reads & writes

## CONS:
- Keys must fit memory (works best for smaller number of rows)
- No ranged queries

## SUMMARY:
- Hash indexes are optimal for scenarios requiring rapid, exact-match lookups on manageable datasets but unsuitable for ranged queries or very large datasets
