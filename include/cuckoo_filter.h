
#ifndef CUCKOO_FILTER_H
#define CUCKOO_FILTER_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

// #include "cuckoofilter_export.h"
#define CUCKOOFILTER_EXPORT

#ifdef __GNUC__
#define PACK( __Declaration__ ) __Declaration__ __attribute__((__packed__))
#endif

#ifdef _MSC_VER
#define PACK( __Declaration__ ) __pragma( pack(push, 1) ) __Declaration__ __pragma( pack(pop))
#endif

typedef enum {
  CUCKOO_FILTER_OK = 0,
  CUCKOO_FILTER_NOT_FOUND,
  CUCKOO_FILTER_FULL,
  CUCKOO_FILTER_ALLOCATION_FAILED,
} CUCKOO_FILTER_RETURN;

typedef PACK(struct {
  uint16_t              fingerprint;
}) cuckoo_nest_t;

typedef PACK(struct {
  uint32_t              fingerprint;
  uint32_t              h1;
  uint32_t              h2;
  uint32_t              padding;
}) cuckoo_item_t;

typedef PACK(struct cuckoo_filter_t {
  uint32_t              bucket_count;
  uint32_t              nests_per_bucket;
  uint32_t              mask;
  uint32_t              max_kick_attempts;
  uint32_t              seed;
  uint32_t              padding;
  /* If `last_victim` is non-NULL, this is the last addition (not in the filter proper). */
  cuckoo_item_t         victim;
  /* Used to indicate if the filter is "full". */
  cuckoo_item_t        *last_victim;
  cuckoo_nest_t         bucket[1];
}) cuckoo_filter_t;

CUCKOOFILTER_EXPORT
CUCKOO_FILTER_RETURN
cuckoo_filter_new (
  cuckoo_filter_t     **filter,
  uint32_t              max_key_count,
  uint32_t              max_kick_attempts,
  uint32_t              seed
);

CUCKOOFILTER_EXPORT
CUCKOO_FILTER_RETURN
cuckoo_filter_free (
  cuckoo_filter_t     **filter
);

CUCKOOFILTER_EXPORT
CUCKOO_FILTER_RETURN
cuckoo_filter_add (
  cuckoo_filter_t      *filter,
  void                 *key,
  uint32_t              key_length_in_bytes
);

CUCKOOFILTER_EXPORT
CUCKOO_FILTER_RETURN
cuckoo_filter_remove (
  cuckoo_filter_t      *filter,
  void                 *key,
  uint32_t              key_length_in_bytes
);

CUCKOOFILTER_EXPORT
CUCKOO_FILTER_RETURN
cuckoo_filter_contains (
  cuckoo_filter_t      *filter,
  void                 *key,
  uint32_t              key_length_in_bytes
);

CUCKOOFILTER_EXPORT
CUCKOO_FILTER_RETURN
cuckoo_filter_contains_hash (
  cuckoo_filter_t      *filter,
  uint32_t             fingerprint,
  uint32_t             h1
);

CUCKOOFILTER_EXPORT
void
cuckoo_filter_hash (
  cuckoo_filter_t      *filter,
  void                 *key,
  uint32_t              key_length_in_bytes,
  uint32_t             *fingerprint,
  uint32_t             *h1,
  uint32_t             *h2
);

#endif /* CUCKOO_FILTER_H */

