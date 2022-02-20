Cuckoo Filter Python Extension
==============================

This project is a fork of the Cuckoo Filter Library by Jonah H. Harris, and modifies the
original project in two different ways.

The first modification is that it wraps the library in a Python extension module, providing a
`CuckooFilter` object that represents the lifetime of a given cuckoo filter, and exposes methods
allowing the addition, removal and lookup operations.

The second modification is that we extend the API allowing generation of hashes and looking up of
those hashes directly. This is intended to aid in server lookups of the same item data in a
multiple cuckoo filters without requiring that it be hashed as part of each lookup.

Usage notes
-----------

The `max_key_count` is a hint to the bucket allocator. All buckets are sized to the next power of
two above the count. Additionally if the `max_key_count` value is greater than 96% of the bucket
size, the bucket size is bumped up next power of two again.

The memory used for buckets given the `max_key_count` hint is as shown below:

| Hint        | First size  | Actual size |
| ----------- | ----------- | ----------- |
| 1900        |    4096     |     4906    |
| 2000        |    4096     |     8192    |
| 60000       |  131072     |   131072    |
| 65000       |  131072     |   262144    |
| 120000      |  262144     |   262144    |
| 128000      |  262144     |   524288    |
| 250000      |  524288     |   524288    |
| 256000      |  524288     |  1048576    |
| 500000      | 1048576     |  1048576    |
| 512000      | 1048576     |  2097152    |

It is likely that it is not worth allocating space that will be filled above 95% as the filter
will be highly occupied and attempting to fit in extra items will fail. Every time the bucket
space doubles the expected number of false positives encountered decreases in that filter,
although the more occupied a filter becomes the rate of false positives increases. A filter
double the size of another will have half the rate of false positives when it approaches half
occupancy and above. At a quarter occupancy, the larger filter will have quarter the rate of
false positives.

Cuckoo Filter Library
=====================

Similar to a Bloom filter, a Cuckoo filter provides a space-efficient data structure designed to
answer approximate set-membership queries (e.g. "is item x contained in this set?") Unlike
standard Bloom filters, however, Cuckoo filters support deletion. Likewise, Cuckoo filters are
more optimal than Bloom variants which support deletion, such as counting Bloom filters, in both
space and time.

Cuckoo filters are based on cuckoo hashing. A Cuckoo filter is essentially a cuckoo hash table
which stores each key's fingerprint. As Cuckoo hash tables are highly compact, a cuckoo filter
often requires less space than conventional Bloom filters for applications that require low
false positive rates (< 3%).

Implementation Details
----------------------

This library was designed to provide a target false positive probability of ~P(0.001) and was
hard-coded to use sixteen bits per item and four nests per bucket. As it uses two hashes, it's
a (2, 4)-cuckoo filter.

C interface
-----------

A Cuckoo filter supports following operations:

*  ``cuckoo_filter_new(filter, max_key_count, max_kick_attempts, seed)``: creates a filter
*  ``cuckoo_filter_free(filter)``: destroys a filter
*  ``cuckoo_filter_add(filter, item, item_length_in_bytes)``: add an item to the filter
*  ``cuckoo_filter_remove(filter, item, item_length_in_bytes)``: remove an item from the filter
*  ``cuckoo_filter_contains(filter, item, item_length_in_bytes)``: test for approximate membership of an item in the filter
*  ``cuckoo_filter_contains_hash(filter, fingerprint, h1)``: test for approximate membership of a hash in the filter
*  ``cuckoo_filter_hash(filter, item, item_length_in_bytes, *fingerprint, *h1)``: hash the item for contains hash checks

Repository structure
--------------------*

*  ``example/example.c``: an example demonstrating the use of the filter
*  ``include/cuckoo_filter.h``: the public header file
*  ``src/cuckoo_filter.c``: a C-based implementation of a (2, 4)-cuckoo filter
*  ``src/cuckoo_python.c``: a C-based Python extension module wrapping the cuckoo filters
*  ``tests/test.c``: unit tests

Usage
-------

To build and install the extension module for development:

    > pip install -e .


Original author
---------------
Jonah H. Harris <jonah.harris@gmail.com>

License
-------
The MIT License

References
----------

* "Cuckoo Filter: Better Than Bloom" by Bin Fan, Dave Andersen, and Michael Kaminsky

