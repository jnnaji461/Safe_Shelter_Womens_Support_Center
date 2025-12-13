# main.py - Test the complete system
from database import create_database
from models import Resident, Service

def test_system():
    print("=== Safe Shelter System ===\n")
    
    # 1. Create database tables
    create_database()
    print("✓ Database ready")
    
    # 2. Add a resident
    resident = Resident("Maria", "Garcia", "2024-03-15")
    save_result = resident.save()
    print(f"✓ {save_result}")
    
    # 3. Add a service
    service_result = Service.add(1, "Counseling")
    print(f"✓ {service_result}")
    
    # 4. Show all residents
    print("\nCurrent residents:")
    residents = Resident.get_all()
    for r in residents:
        print(f"  - ID {r[0]}: {r[1]} {r[2]} (Entered: {r[3]})")
    
    print("\n✅ System test complete!")

if __name__ == "__main__":
    test_system()