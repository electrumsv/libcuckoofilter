"""
"""

from collections import defaultdict
import os

import bsvcuckoo

LOOKUP_COUNT = 1000000
ITERATIONS = 100

with open("test_kick.csv", "w") as f:
    print("kick count, added entries, minimum, maximum, average", file=f)

    maximum_entries = 256000
    for kick_count in [0, 1]:
        false_positive_map: dict[int, list[int]] = defaultdict(list)
        for i in range(ITERATIONS):
            print(f"{i}, ", end="", flush=True)
            filter = bsvcuckoo.CuckooFilter(maximum_entries, kick_count, 1644963952)
            addition_count = 2000
            last_addition_count = 0
            while addition_count <= maximum_entries:
                for i in range(last_addition_count, addition_count):
                    k = os.urandom(32)
                    filter.add(k)

                false_positives = 0
                for j in range(LOOKUP_COUNT):
                    k = os.urandom(32)
                    if filter.contains(k) == 0:
                        false_positives += 1
                false_positive_map[addition_count].append(false_positives)
                last_addition_count = addition_count
                addition_count *= 2

        print()

        for addition_count, false_positive_counts in false_positive_map.items():
            print(f"{kick_count:10}, {addition_count:13}, {min(false_positive_counts):7}, "
                f"{max(false_positive_counts):7}, {sum(false_positive_counts)/ITERATIONS:7.1f}",
                file=f)

