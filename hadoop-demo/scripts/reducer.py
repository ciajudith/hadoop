#!/usr/bin/env python3
import sys
from collections import defaultdict

sums, counts = defaultdict(float), defaultdict(int)
for line in sys.stdin:
    country, hours, cnt = line.strip().split('\t')
    sums[country] += float(hours)
    counts[country] += int(cnt)
for country in sums:
    avg = sums[country] / counts[country]
    print(f"{country}\t{avg:.2f}")