# models.py - Resident, Service, and Room classes

class Resident:
    def __init__(self, first_name, last_name, entry_date):
        self.first_name = first_name
        self.last_name = last_name
        self.entry_date = entry_date
        self.room = None
        self.status = "active"