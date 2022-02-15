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

Interface
--------
A Cuckoo filter supports following operations:

*  ``cuckoo_filter_new(filter, max_key_count, max_kick_attempts, seed)``: creates a filter
*  ``cuckoo_filter_free(filter)``: destroys a filter
*  ``cuckoo_filter_add(filter, item, item_length_in_bytes)``: add an item to the filter
*  ``cuckoo_filter_remove(filter, item, item_length_in_bytes)``: remove an item from the filter
*  ``cuckoo_filter_contains(filter, item, item_length_in_bytes)``: test for approximate membership of an item in the filter

Repository structure
--------------------

*  ``example/example.c``: an example demonstrating the use of the filter
*  ``include/cuckoo_filter.h``: the public header file
*  ``src/cuckoo_filter.c``: a C-based implementation of a (2, 4)-cuckoo filter
*  ``src/cuckoo_python.c``: a C-based Python extension module wrapping the cuckoo filters
*  ``tests/test.c``: unit tests

Usage
-------

Currently a building script is provided only for Windows, but in due course we will likely support
more platforms through the cross-platform Python package building VMs.

To build the extension module on Windows for now:

    $ make.bat


Original author
---------------
Jonah H. Harris <jonah.harris@gmail.com>

License
-------
The MIT License

References
----------

* "Cuckoo Filter: Better Than Bloom" by Bin Fan, Dave Andersen, and Michael Kaminsky

