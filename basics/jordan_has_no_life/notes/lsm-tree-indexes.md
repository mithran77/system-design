# LSM-Tree (Log structure merge) Indexes

## How do LSM-Tree Indexes work?
- Structure:
  - An in-memory balanced binary search tree (e.g., Red-Black Tree, AVL Tree, or B-Tree).
  - Operations (read/write): O(logn).
- Durability:
  - In-memory LSM-Tree lacks durability.
  - Uses Write-Ahead Logging (WAL) for durability:
    - WAL sequentially writes to disk (faster than random writes but adds overhead).
- SSTables (Sorted String Tables):
  - When the in-memory LSM-Tree exceeds a size threshold, it is written as a sorted SSTable on disk.
  - SSTables allow efficient binary searches due to their sorted nature.
- Search Process:
  - Check the in-memory LSM-Tree first, then the most recent SSTable.
- Deletes with Tombstones:
  - Deletes are marked as "tombstones" in the most recent tree.
  - To confirm presence, the check includes both memory and disk.

## What are the LSM optimizations?
- Sparce indexes:
  - Indexes store only select keys with their disk locations.
  - Used to narrow the range for searches in memory.
- Bloom Filters:
  - Quickly determine if a key is not present in an SSTable.
  - Saves search time when the filter returns "NO."
- Compaction:
  - Combines and sorts SSTables, overwriting older values of duplicate keys
  - Maintains sorted order for efficient access

## PROS:
- Scalability: Number of keys not limited by RAM

## Neutral:
- Write Performance: Faster than B-Trees for in-memory writes but slower than hash-based indexing
- Read Performance:
  - Supports range queries but is slower than B-Trees.
  - Requires checking multiple SSTables for reads

## CONS:
- Extra CPU resources used for moving to SSTables & compaction 

