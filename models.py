# models.py - Core classes for Safe Shelter
import sqlite3
from datetime import date

class Resident:
    """Represents a shelter resident"""

    def __init__(self, first_name, last_name, entry_date):        
        self.first_name = first_name
        self.last_name = last_name
        self.entry_date = entry_date

    def save(self):
        """Save resident to database"""
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO residents (first_name, last_name, entry_date) VALUES (?, ?, ?)',
            (self.first_name, self.last_name, self.entry_date)    
        )
        conn.commit()
        conn.close()
        return "Resident saved"

    @staticmethod
    def get_all():
        """Get all residents from database"""
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM residents ORDER BY id')     
        residents = cursor.fetchall()
        conn.close()
        return residents

    @staticmethod
    def check_duplicate(first_name, last_name):
        """Check if resident already exists in database"""
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT id FROM residents WHERE LOWER(first_name) = LOWER(?) AND LOWER(last_name) = LOWER(?)',
            (first_name, last_name)
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None  # Returns True if duplicate exists


class Service:
    """Represents a service provided"""

    @staticmethod
    def add(resident_id, service_type):
        """Add a service record"""
        today = date.today().isoformat()

        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO services (resident_id, service_type, service_date) VALUES (?, ?, ?)',
            (resident_id, service_type, today)
        )
        conn.commit()
        conn.close()
        return "Service logged"