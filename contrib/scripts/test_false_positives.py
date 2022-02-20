"""
                                .... false positives ....
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
          62914,          2000,      47,     101,    68.8
          62914,          4000,     104,     161,   132.6
          62914,          8000,     233,     315,   270.5
          62914,         16000,     488,     598,   538.3
          62914,         32000,     989,    1141,  1063.8
          62914,         62914,    1869,    2063,  1971.1
          ... 65536 * 0.96
          62915,          2000,      10,      26,    16.8
          62915,          4000,      20,      46,    33.5
          62915,          8000,      47,      92,    67.1
          62915,         16000,     102,     156,   134.8
          62915,         32000,     225,     307,   269.5
          62915,         62915,     463,     584,   530.4
          64000,          2000,       9,      30,    17.0
          64000,          4000,      18,      46,    33.4
          64000,          8000,      46,      83,    65.9
          64000,         16000,     109,     163,   134.2
          64000,         32000,     234,     303,   267.7
          64000,         64000,     478,     598,   533.8
         125829,          2000,       7,      31,    16.6
         125829,          4000,      20,      52,    34.0
         125829,          8000,      47,      83,    67.7
         125829,         16000,     102,     164,   134.4
         125829,         32000,     218,     322,   270.0
         125829,         64000,     478,     597,   535.5
         125829,        125829,     901,    1051,   985.2
         ... (65536 << 1) * 0.96
         125830,          2000,       0,       9,     4.5
         125830,          4000,       2,      15,     8.8
         125830,          8000,       4,      27,    17.1
         125830,         16000,      18,      46,    31.7
         125830,         32000,      44,      86,    66.5
         125830,         64000,     105,     166,   132.8
         125830,        125830,     228,     299,   261.5
         128000,          2000,       1,      12,     4.6
         128000,          4000,       3,      15,     8.6
         128000,          8000,       9,      26,    17.4
         128000,         16000,      21,      45,    33.4
         128000,         32000,      45,      93,    67.1
         128000,         64000,     103,     166,   135.5
         128000,        128000,     235,     310,   268.9
         251658,          2000,       0,       9,     4.2
         251658,          4000,       1,      19,     8.1
         251658,          8000,       9,      34,    17.1
         251658,         16000,      16,      52,    33.0
         251658,         32000,      49,      86,    66.2
         251658,         64000,     104,     174,   135.4
         251658,        128000,     228,     324,   266.8
         251658,        251658,     441,     538,   494.2
         ... (65536 << 2) * 0.96
         251659,          2000,       0,       6,     2.1
         251659,          4000,       1,       9,     4.1
         251659,          8000,       2,      18,     8.4
         251659,         16000,       8,      31,    17.1
         251659,         32000,      19,      47,    33.1
         251659,         64000,      47,      91,    67.6
         251659,        128000,     105,     161,   134.8
         251659,        251659,     224,     306,   263.2
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
MAX_KICK_COUNT = 10

with open("test.csv", "w") as f:
    print("maximum entries, added entries, minimum, maximum, average", file=f)

    maximum_entries = 251658
    while maximum_entries <= 251659:
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
                if last_addition_count < maximum_entries and addition_count > maximum_entries:
                    addition_count = maximum_entries

        print()

        for addition_count, false_positive_counts in false_positive_map.items():
            print(f"{maximum_entries:15}, {addition_count:13}, {min(false_positive_counts):7}, "
                f"{max(false_positive_counts):7}, {sum(false_positive_counts)/ITERATIONS:7.1f}",
                file=f)
        maximum_entries += 1

