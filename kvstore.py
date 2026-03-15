#!/usr/bin/env python3
"""
Simple Key-Value Store with Persistent Storage
Author: Waad
EUID: 11660840
Date: March 2026
"""

import os
import sys

class KeyValueStore:
    """A simple persistent key-value store using append-only logging"""
    
    def __init__(self, db_file="data.db"):
        """Initialize the database with the given file"""
        self.db_file = db_file
        self.index = []  # Custom index structure (list of [key, value] pairs)
        self._load_from_disk()
    
    def _load_from_disk(self):
        """Replay the log file to rebuild the in-memory index"""
        self.index = []  # Reset index
        
        if not os.path.exists(self.db_file):
            return  # No existing database file
        
        try:
            with open(self.db_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Parse each line: "SET key value"
                    parts = line.split(' ', 2)
                    if len(parts) == 3 and parts[0] == "SET":
                        key = parts[1]
                        value = parts[2]
                        
                        # Update index with last write wins semantics
                        self._set_in_index(key, value)
        except IOError as e:
            print(f"Error loading database: {e}", file=sys.stderr)
    
    def _set_in_index(self, key, value):
        """
        Custom index manipulation without using dict
        Uses linear search in a list of [key, value] pairs
        """
        # Search for existing key
        for i, (k, v) in enumerate(self.index):
            if k == key:
                # Update existing key
                self.index[i] = [key, value]
                return
        
        # Add new key-value pair
        self.index.append([key, value])
    
    def _get_from_index(self, key):
        """Linear search for a key in the index"""
        for k, v in self.index:
            if k == key:
                return v
        return None
    
    def set(self, key, value):
        """
        Set a key-value pair and persist to disk
        Uses append-only logging
        """
        # Validate input
        if not key or ' ' in key:
            print("Error: Key cannot be empty or contain spaces", file=sys.stderr)
            return False
        
        # Append to log file
        try:
            with open(self.db_file, 'a') as f:
                f.write(f"SET {key} {value}\n")
                f.flush()  # Ensure it's written to disk
                os.fsync(f.fileno())  # Force write to disk
        except IOError as e:
            print(f"Error writing to disk: {e}", file=sys.stderr)
            return False
        
        # Update in-memory index
        self._set_in_index(key, value)
        return True
    
    def get(self, key):
        """Retrieve a value for a given key"""
        value = self._get_from_index(key)
        if value is None:
            print(f"GET {key}")
            print("(nil)")
        else:
            print(f"GET {key}")
            print(value)
        return value
    
    def close(self):
        """Clean up resources"""
        pass

class CommandLineInterface:
    """Handles user interaction through command line"""
    
    def __init__(self):
        self.db = KeyValueStore()
        self.running = True
    
    def process_command(self, command_line):
        """Process a single command"""
        if not command_line:
            return
        
        parts = command_line.strip().split()
        if not parts:
            return
        
        cmd = parts[0].upper()
        
        if cmd == "EXIT":
            self.running = False
            return True
        
        elif cmd == "SET":
            if len(parts) >= 3:
                key = parts[1]
                # Value might contain spaces, join remaining parts
                value = ' '.join(parts[2:])
                self.db.set(key, value)
            else:
                print("Error: SET requires key and value", file=sys.stderr)
        
        elif cmd == "GET":
            if len(parts) == 2:
                self.db.get(parts[1])
            else:
                print("Error: GET requires a key", file=sys.stderr)
        
        else:
            print(f"Error: Unknown command '{cmd}'", file=sys.stderr)
        
        return False
    
    def run(self):
        """Main CLI loop"""
        if sys.stdin.isatty():
            # Interactive mode
            print("Simple Key-Value Store")
            print("Author: Waad (EUID: 11660840)")
            print("Commands: SET key value, GET key, EXIT")
            print("-" * 40)
        
        for line in sys.stdin:
            line = line.strip()
            if self.process_command(line):
                break
        
        self.db.close()

def main():
    """Main entry point"""
    cli = CommandLineInterface()
    cli.run()

if __name__ == "__main__":
    main()
