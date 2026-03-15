#!/usr/bin/env python3
import sys, os

DB = "data.db"
data = {}

if os.path.exists(DB):
    with open(DB) as f:
        for line in f:
            if line.startswith('SET '):
                p = line[4:].split(' ', 1)
                if len(p) == 2:
                    data[p[0]] = p[1]

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
        data[k] = v
    elif cmd == "GET" and len(parts) == 2:
        k = parts[1]
        print(f"GET {k}")
        print(data.get(k, "(nil)"))
        sys.stdout.flush()
