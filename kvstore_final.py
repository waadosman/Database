#!/usr/bin/env python3
"""
Simple Key-Value Store with Append-Only Persistence
Author: Waad (EUID: 11660840)
Date: March 2026
"""

import os
import sys

class SimpleIndex:
    """
    Custom index structure - no built-in dictionaries allowed!
    Implements a simple array-based key-value store with linear search.
    """
    def __init__(self):
        self.keys = []
        self.values = []
        self.size = 0
    
    def set(self, key, value):
        """Set key-value pair with last-write-wins semantics"""
        # Check if key exists
        for i in range(self.size):
            if self.keys[i] == key:
                # Update existing key
                self.values[i] = value
                return
        
        # Add new key-value pair
        self.keys.append(key)
        self.values.append(value)
        self.size += 1
    
    def get(self, key):
        """Get value for key, returns None if not found"""
        for i in range(self.size):
            if self.keys[i] == key:
                return self.values[i]
        return None
    
    def get_all_pairs(self):
        """Return all key-value pairs for log replay"""
        pairs = []
        for i in range(self.size):
            pairs.append((self.keys[i], self.values[i]))
        return pairs
    
    def clear(self):
        """Clear the index"""
        self.keys = []
        self.values = []
        self.size = 0


class KVStore:
    """
    Persistent key-value store using append-only log
    """
    def __init__(self, filename="data.db"):
        self.filename = filename
        self.index = SimpleIndex()
        self.replay_log()
    
    def replay_log(self):
        """Replay the append-only log to rebuild the index"""
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse the log line
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        key, value = parts
                        self.index.set(key, value)
        except Exception as e:
            print(f"Error replaying log: {e}", file=sys.stderr)
    
    def set(self, key, value):
        """Set a key-value pair and persist to disk"""
        # Append to log file
        try:
            with open(self.filename, 'a') as f:
                f.write(f"{key} {value}\n")
        except Exception as e:
            print(f"Error writing to log: {e}", file=sys.stderr)
            return
        
        # Update in-memory index
        self.index.set(key, value)
    
    def get(self, key):
        """Get value for key from in-memory index"""
        return self.index.get(key)
    
    def close(self):
        """Clean up resources"""
        pass  # Nothing to clean up


def main():
    """Main CLI loop"""
    store = KVStore("data.db")
    
    while True:
        try:
            # Read command from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line:
                continue
            
            parts = line.split()
            command = parts[0].upper()
            
            if command == "SET" and len(parts) >= 3:
                # Handle SET key value
                key = parts[1]
                # Value might contain spaces, join remaining parts
                value = ' '.join(parts[2:])
                store.set(key, value)
                
            elif command == "GET" and len(parts) == 2:
                # Handle GET key
                key = parts[1]
                value = store.get(key)
                if value is not None:
                    print(value)
                    sys.stdout.flush()
                # Don't print anything for non-existent keys (per spec)
                
            elif command == "EXIT":
                # Exit the program
                store.close()
                break
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
