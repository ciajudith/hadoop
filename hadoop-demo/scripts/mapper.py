#!/usr/bin/env python3

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith("Student_ID,"):
        continue
    parts = line.split(",")
    # Make sure we have enough columns
    if len(parts) < 6:
        continue
    country = parts[4]
    try:
        hours = float(parts[5])
        print(f"{country}\t{hours}\t1")
    except ValueError:
        continue