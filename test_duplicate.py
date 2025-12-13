# Test duplicate checking feature
from models import Resident
from database import create_database

# Setup
create_database()

print("Testing duplicate checking...")
print("=" * 40)

# Test 1: Check for Maria Garcia (should be True - she exists)
print("Test 1: Checking for 'Maria Garcia'...")
result1 = Resident.check_duplicate("Maria", "Garcia")
print(f"   Result: {result1}")
print(f"   Expected: True")
print(f"   ✓ PASS" if result1 == True else "   ✗ FAIL")

print()

# Test 2: Check for non-existent resident (should be False)
print("Test 2: Checking for 'John Doe'...")
result2 = Resident.check_duplicate("John", "Doe")
print(f"   Result: {result2}")
print(f"   Expected: False")
print(f"   ✓ PASS" if result2 == False else "   ✗ FAIL")

print()

# Test 3: Check case sensitivity (should still find Maria)
print("Test 3: Checking for 'maria garcia' (lowercase)...")
result3 = Resident.check_duplicate("maria", "garcia")
print(f"   Result: {result3}")
print(f"   Expected: True")
print(f"   ✓ PASS" if result3 == True else "   ✗ FAIL")

print("=" * 40)
print("Duplicate checking test complete!")