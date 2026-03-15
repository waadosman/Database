#!/usr/bin/env python3
"""
Test script for the Key-Value Store
Author: Waad
EUID: 11660840
"""

import subprocess
import os

def test_kvstore():
    """Run tests on the key-value store"""
    
    # Remove existing database if present
    if os.path.exists("data.db"):
        os.remove("data.db")
    
    print("=" * 50)
    print("Testing Key-Value Store")
    print("Author: Waad (EUID: 11660840)")
    print("=" * 50)
    
    # Test 1: Basic SET and GET
    print("\n1. Testing basic SET and GET...")
    commands = "SET name Waad\nGET name\nEXIT\n"
    result = subprocess.run(
        ['python3', 'kvstore.py'],
        input=commands,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if "Waad" in result.stdout:
        print("✓ PASSED")
    else:
        print("✗ FAILED")
    
    # Test 2: Key overwrites
    print("\n2. Testing key overwrites...")
    commands = "SET city Dallas\nGET city\nSET city Austin\nGET city\nEXIT\n"
    result = subprocess.run(
        ['python3', 'kvstore.py'],
        input=commands,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if "Dallas" in result.stdout and "Austin" in result.stdout:
        print("✓ PASSED")
    else:
        print("✗ FAILED")
    
    # Test 3: Non-existent key
    print("\n3. Testing non-existent key...")
    commands = "GET unknown\nEXIT\n"
    result = subprocess.run(
        ['python3', 'kvstore.py'],
        input=commands,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if "(nil)" in result.stdout:
        print("✓ PASSED")
    else:
        print("✗ FAILED")
    
    # Test 4: Persistence after restart
    print("\n4. Testing persistence after restart...")
    
    # First session - set some values
    commands = "SET color blue\nSET size large\nEXIT\n"
    subprocess.run(['python3', 'kvstore.py'], input=commands, capture_output=True, text=True)
    
    # Second session - retrieve values
    commands = "GET color\nGET size\nEXIT\n"
    result = subprocess.run(
        ['python3', 'kvstore.py'],
        input=commands,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if "blue" in result.stdout and "large" in result.stdout:
        print("✓ PASSED")
    else:
        print("✗ FAILED")
    
    # Test 5: Values with spaces
    print("\n5. Testing values with spaces...")
    commands = "SET greeting Hello World\nGET greeting\nEXIT\n"
    result = subprocess.run(
        ['python3', 'kvstore.py'],
        input=commands,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if "Hello World" in result.stdout:
        print("✓ PASSED")
    else:
        print("✗ FAILED")
    
    print("\n" + "=" * 50)
    print("All tests completed - Waad (EUID: 11660840)")

if __name__ == "__main__":
    test_kvstore()
