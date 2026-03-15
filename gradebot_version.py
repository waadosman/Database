#!/usr/bin/env python3
"""
Simple Key-Value Store - Gradebot Optimized Version
Author: Waad
EUID: 11660840
Date: March 2026
"""

import os
import sys

DB_FILE = "data.db"

# Load existing data
data = []
if os.path.exists(DB_FILE):
    try:
        with open(DB_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('SET '):
                    parts = line[4:].split(' ', 1)
                    if len(parts) == 2:
                        key = parts[0]
                        value = parts[1]
                        # Update or add
                        found = False
                        for i, (k, v) in enumerate(data):
                            if k == key:
                                data[i] = [key, value]
                                found = True
                                break
                        if not found:
                            data.append([key, value])
    except:
        pass

# Process commands - NO WELCOME MESSAGE, just process stdin
for line in sys.stdin:
    line = line.strip()
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
        try:
            with open(DB_FILE, 'a') as f:
                f.write(f"SET {key} {value}\n")
                f.flush()
        except:
            pass
        
        # Update memory
        found = False
        for i, (k, v) in enumerate(data):
            if k == key:
                data[i] = [key, value]
                found = True
                break
        if not found:
            data.append([key, value])
    
    elif cmd == "GET" and len(parts) == 2:
        key = parts[1]
        value = None
        for k, v in data:
            if k == key:
                value = v
                break
        
        # Print EXACT format - NO EXTRA SPACES
        sys.stdout.write(f"GET {key}\n")
        if value is None:
            sys.stdout.write("(nil)\n")
        else:
            sys.stdout.write(f"{value}\n")
        sys.stdout.flush()
    
    # Ignore any other commands
