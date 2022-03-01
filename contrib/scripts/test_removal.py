import bsvcuckoo
import os
import sys

f = bsvcuckoo.CuckooFilter(500000, 500, 1646115433)
adds = [ os.urandom(32) for i in range(600000) ]
add_fails = {}
add_full_index = -1
for i, k in enumerate(adds):
    v1 = f.add(k)
    if v1 == 2:
        add_full_index = i
        break
    elif v1 > 0:
        if v1 not in add_fails:
            add_fails[v1] = set()
        add_fails[v1].add(k)

contains_counts = {}
contains_fails = {}
for i, k in enumerate(adds):
    if add_full_index > -1 and i > add_full_index:
        break
    v = f.contains(k)
    if v not in contains_counts:
        contains_counts[v] = 1
    else:
        contains_counts[v] += 1
    if v > 0:
        if v not in contains_fails:
            contains_fails[v] = set()
        contains_fails[v].add(k)

print("adds before filter became full:", add_full_index)
false_negative_count = sum(value for retcode, value in contains_counts.items() if retcode > 0)
print("false negatives               :", false_negative_count)
for retcode, fail_keys in contains_fails.items():
    if retcode > 0:
        for k in fail_keys:
            print(f"  fail: {retcode:2d}, key: {k.hex()}, index: {adds.index(k)}")
            print(f"            hash: {f.hash(k)}")


for i, k in enumerate(adds):
    if add_full_index > -1 and i > add_full_index:
        print("exit removal loop")
        break
    v = f.contains(k)
    if v != 0:
        print(f"failed pre-contains index {i} key {k.hex()} with {v}")
        break
    v = f.remove(k)
    if v > 0:
        print(f"failed removing index {i} key {k.hex()} with {v}")
        break
    v = f.contains(k)
    if v != 1:
        print(f"failed contains index {i} key {k.hex()} with {v}")
        break
