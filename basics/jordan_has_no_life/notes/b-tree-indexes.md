# B Tree Indexes

## What is a B-Tree?
- B-tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, insertions, and deletions in logarithmic time
- The B-tree generalizes the binary search tree, allowing for nodes with more than two children

## How do B-Tree Indexes work?
- Structure:
    - Balanced tree structure, self-balancing to maintain efficiency.
    - Ancestor nodes store key ranges and pointers(l & r) for traversal.
    - Leaf nodes hold references to table rows.
- Storage:
    - Typically stored on disk, providing durability without reliance on RAM.
    - Nodes are ~8 KB (page size), storing multiple references efficiently.
- Operations:
    - Search:O(logn) time for exact matches due to balanced structure.
    - Writes:
      - If a node exceeds its size limit, space is adjusted by splitting nodes, potentially up to the root.
      - Data is logged to a WAL to ensure recovery after crashes.

## PROS:
- Efficient Reads: O(logn) reads with balanced access time across nodes.
- Large Dataset Support: Suitable for large databases due to disk storage.
- Range Queries: Optimized for range lookups, as data is effectively sorted.

## CONS:
- Slower Writes/Deletes:
  - Updates may require node splits and adjustments up to the root.
  - This adds overhead compared to hash indexes.

## SUMMARY:
- B-Tree indexes are versatile, offering efficient reads and range queries, making them suitable for large datasets. However, the trade-off is slower writes due to the balancing required for node splits.

## References:
- https://leetcode.com/problems/validate-binary-search-tree/description/

