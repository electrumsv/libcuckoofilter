"""
maximum entries, added entries, minimum, maximum, average
          16000,          2000,     231,     301,   262.8
          16000,          4000,     470,     601,   535.4
          16000,          8000,    1005,    1161,  1075.9
          16000,         16000,    2021,    2270,  2139.1
          32000,          2000,      53,      88,    67.0
          32000,          4000,     106,     159,   134.7
          32000,          8000,     225,     313,   268.2
          32000,         16000,     503,     602,   542.0
          32000,         32000,     997,    1148,  1069.4
          64000,          2000,       9,      30,    17.0
          64000,          4000,      18,      46,    33.4
          64000,          8000,      46,      83,    65.9
          64000,         16000,     109,     163,   134.2
          64000,         32000,     234,     303,   267.7
          64000,         64000,     478,     598,   533.8
         128000,          2000,       1,      12,     4.6
         128000,          4000,       3,      15,     8.6
         128000,          8000,       9,      26,    17.4
         128000,         16000,      21,      45,    33.4
         128000,         32000,      45,      93,    67.1
         128000,         64000,     103,     166,   135.5
         128000,        128000,     235,     310,   268.9
         256000,          2000,       0,       5,     1.8
         256000,          4000,       1,      11,     4.3
         256000,          8000,       1,      15,     8.5
         256000,         16000,       8,      32,    17.6
         256000,         32000,      21,      48,    33.4
         256000,         64000,      49,      92,    67.3
         256000,        128000,     106,     163,   134.7
         256000,        256000,     229,     316,   266.2
         512000,          2000,       0,       4,     1.1
         512000,          4000,       0,       6,     1.9
         512000,          8000,       0,      11,     4.2
         512000,         16000,       2,      16,     8.4
         512000,         32000,       9,      29,    16.7
         512000,         64000,      22,      51,    33.1
         512000,        128000,      46,      83,    65.7
         512000,        256000,     100,     156,   133.7
         512000,        512000,     240,     303,   268.9
"""

from collections import defaultdict
import os

import bsvcuckoo

LOOKUP_COUNT = 1000000
ITERATIONS = 100
MAX_KICK_COUNT = 1

with open("test.csv", "w") as f:
    print("maximum entries, added entries, minimum, maximum, average", file=f)

    maximum_entries = 16000
    while maximum_entries <= 512000:
        false_positive_map: dict[int, list[int]] = defaultdict(list)
        for i in range(ITERATIONS):
            print(f"{i}, ", end="", flush=True)
            filter = bsvcuckoo.CuckooFilter(maximum_entries, MAX_KICK_COUNT, 1644963952)
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
            print(f"{maximum_entries:15}, {addition_count:13}, {min(false_positive_counts):7}, "
                f"{max(false_positive_counts):7}, {sum(false_positive_counts)/ITERATIONS:7.1f}",
                file=f)
        maximum_entries *= 2

