#!/usr/bin/env python3
import sys
import os

DB_FILE = "data.db"

# Load existing data
data = []
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('SET '):
                parts = line[4:].split(' ', 1)
                if len(parts) == 2:
                    key = parts[0]
                    value = parts[1]
                    # Update index
                    found = False
                    for i, (k, v) in enumerate(data):
                        if k == key:
                            data[i] = (key, value)
                            found = True
                            break
                    if not found:
                        data.append((key, value))

# Read all input at once (fixes timeout)
import sys
lines = sys.stdin.read().strip().split('\n')

for line in lines:
    if not line:
        continue
    
    parts = line.split()
    if not parts:
        continue
    
    cmd = parts[0].upper()
    
    if cmd == "EXIT":
        break
    
    elif cmd == "SET" and len(parts) >= 3:
        key = parts[1]
        value = ' '.join(parts[2:])
        
        # Write to file
        with open(DB_FILE, 'a') as f:
            f.write(f"SET {key} {value}\n")
            f.flush()
        
        # Update memory
        found = False
        for i, (k, v) in enumerate(data):
            if k == key:
                data[i] = (key, value)
                found = True
                break
        if not found:
            data.append((key, value))
    
    elif cmd == "GET" and len(parts) == 2:
        key = parts[1]
        value = None
        for k, v in data:
            if k == key:
                value = v
                break
        
        # Print immediately
        print(f"GET {key}")
        if value is None:
            print("(nil)")
        else:
            print(value)
        sys.stdout.flush()
