#!/usr/bin/env python3
import sys, os

DB = "data.db"

# Always reload from disk for each GET to ensure persistence works
def get_value(key):
    if not os.path.exists(DB):
        return None
    with open(DB, 'r') as f:
        for line in f:
            if line.startswith('SET '):
                parts = line[4:].split(' ', 1)
                if len(parts) == 2 and parts[0] == key:
                    return parts[1]
    return None

for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split()
    if not parts: continue
    
    cmd = parts[0].upper()
    if cmd == "EXIT": break
    elif cmd == "SET" and len(parts) >= 3:
        k, v = parts[1], ' '.join(parts[2:])
        with open(DB, 'a') as f: f.write(f"SET {k} {v}\n")
    elif cmd == "GET" and len(parts) == 2:
        k = parts[1]
        v = get_value(k)
        print(f"GET {k}")
        print(v if v is not None else "(nil)")
        sys.stdout.flush()
