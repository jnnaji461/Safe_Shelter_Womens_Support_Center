# gui.py - Safe Shelter Management System GUI
import tkinter as tk
from tkinter import messagebox
import sqlite3
from models import Resident, Service

class ShelterApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Safe Shelter Management System")
        self.window.geometry("600x600")
        
        self.create_widgets()
        self.refresh_list()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.window, text="Safe Shelter Women's Support Center",
                        font=("Arial", 16, "bold"), fg="darkblue")
        title.pack(pady=15)
        
        # Add Resident Section
        add_frame = tk.LabelFrame(self.window, text="Add New Resident", padx=10, pady=10)
        add_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(add_frame, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.first_entry = tk.Entry(add_frame, width=25)
        self.first_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(add_frame, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.last_entry = tk.Entry(add_frame, width=25)
        self.last_entry.grid(row=1, column=1, padx=5, pady=5)
        
        add_btn = tk.Button(add_frame, text="Add Resident", command=self.add_resident,
                           bg="green", fg="white", width=15)
        add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Search Section
        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=10)
        
        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=25)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        
        search_btn = tk.Button(search_frame, text="Search", command=self.search_residents,
                              bg="orange", fg="white")
        search_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(search_frame, text="Clear Search", command=self.refresh_list)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Log Service Section
        service_frame = tk.LabelFrame(self.window, text="Log Service", padx=10, pady=10)
        service_frame.pack(padx=20, pady=10, fill="x")
        
        tk.Label(service_frame, text="Resident ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.resident_id_entry = tk.Entry(service_frame, width=10)
        self.resident_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(service_frame, text="Service Type:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.service_type_entry = tk.Entry(service_frame, width=20)
        self.service_type_entry.grid(row=0, column=3, padx=5, pady=5)
        
        service_btn = tk.Button(service_frame, text="Log Service", command=self.log_service,
                               bg="blue", fg="white")
        service_btn.grid(row=0, column=4, padx=10, pady=5)
        
        # Residents List Section
        list_frame = tk.LabelFrame(self.window, text="Current Residents", padx=10, pady=10)
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # Create a scrollbar
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.residents_list = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=12)
        self.residents_list.pack(fill="both", expand=True)
        scrollbar.config(command=self.residents_list.yview)
        
        # Button Frame
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)
        
        refresh_btn = tk.Button(btn_frame, text="Refresh List", command=self.refresh_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        report_btn = tk.Button(btn_frame, text="View Services", command=self.view_services)
        report_btn.pack(side=tk.LEFT, padx=5)
        
        exit_btn = tk.Button(btn_frame, text="Exit", command=self.window.quit, bg="red", fg="white")
        exit_btn.pack(side=tk.LEFT, padx=5)
    
    def add_resident(self):
        """Add a new resident to the database with duplicate checking"""
        first = self.first_entry.get().strip()
        last = self.last_entry.get().strip()
        
        if not first or not last:
            messagebox.showerror("Error", "Please enter both first and last name")
            return
        
        # Check for duplicate BEFORE adding
        if Resident.check_duplicate(first, last):
            messagebox.showerror("Error", 
                f"⚠️ DUPLICATE RESIDENT ⚠️\n\n"
                f"Resident '{first} {last}' already exists in the system!\n\n"
                f"Please check the residents list or use a different name.")
            return
        
        # Add the resident (only if not a duplicate)
        from datetime import date
        resident = Resident(first, last, str(date.today()))
        resident.save()
        messagebox.showinfo("Success", 
            f"✅ RESIDENT ADDED\n\n"
            f"Name: {first} {last}\n"
            f"Entry Date: {date.today()}\n\n"
            f"Resident has been added to the database.")
        
        # Clear fields and refresh list
        self.first_entry.delete(0, tk.END)
        self.last_entry.delete(0, tk.END)
        self.refresh_list()
    
    def search_residents(self):
        """Search residents by name"""
        search_term = self.search_entry.get().strip().lower()
        
        if not search_term:
            messagebox.showwarning("Search", "Please enter a name to search for")
            return
        
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM residents 
            WHERE LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ? OR 
                  LOWER(first_name || ' ' || last_name) LIKE ?
            ORDER BY last_name
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
        
        results = cursor.fetchall()
        conn.close()
        
        # Display results
        self.residents_list.delete(0, tk.END)
        
        if results:
            self.residents_list.insert(tk.END, f"=== SEARCH RESULTS ({len(results)} found) ===")
            for resident in results:
                display_text = f"ID {resident[0]}: {resident[1]} {resident[2]} (Entered: {resident[3]})"
                self.residents_list.insert(tk.END, display_text)
        else:
            self.residents_list.insert(tk.END, f"No residents found for '{search_term}'")
    
    def log_service(self):
        """Log a service for a resident"""
        try:
            resident_id = int(self.resident_id_entry.get().strip())
            service_type = self.service_type_entry.get().strip()
            
            if service_type:
                Service.add(resident_id, service_type)
                messagebox.showinfo("Success", 
                                  f"✅ SERVICE LOGGED\n\n"
                                  f"Service: {service_type}\n"
                                  f"For Resident ID: {resident_id}\n"
                                  f"Date: {date.today().isoformat()}")
                self.resident_id_entry.delete(0, tk.END)
                self.service_type_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please enter a service type")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid resident ID number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to log service: {str(e)}")
    
    def refresh_list(self):
        """Refresh the residents list from database"""
        self.residents_list.delete(0, tk.END)
        residents = Resident.get_all()
        
        if not residents:
            self.residents_list.insert(tk.END, "No residents in database")
        else:
            for resident in residents:
                display_text = f"ID {resident[0]}: {resident[1]} {resident[2]} (Entered: {resident[3]})"
                self.residents_list.insert(tk.END, display_text)
    
    def view_services(self):
        """Show all services logged"""
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        
        # Get all services with resident names
        cursor.execute('''
            SELECT services.id, residents.first_name, residents.last_name, 
                   services.service_type, services.service_date
            FROM services
            JOIN residents ON services.resident_id = residents.id
            ORDER BY services.service_date DESC
        ''')
        
        services = cursor.fetchall()
        conn.close()
        
        # Create a new window to display services
        services_window = tk.Toplevel(self.window)
        services_window.title("Logged Services")
        services_window.geometry("500x400")
        
        tk.Label(services_window, text="All Logged Services", 
                font=("Arial", 14, "bold")).pack(pady=10)
        
        # Create text widget to display services
        text_widget = tk.Text(services_window, wrap=tk.WORD, height=15)
        scrollbar = tk.Scrollbar(services_window, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        if services:
            text_widget.insert(tk.END, f"Total Services: {len(services)}\n\n")
            for service in services:
                text = f"• {service[3]} for {service[1]} {service[2]} on {service[4]}\n"
                text_widget.insert(tk.END, text)
        else:
            text_widget.insert(tk.END, "No services have been logged yet.")
        
        text_widget.config(state=tk.DISABLED)  # Make read-only
        
        tk.Button(services_window, text="Close", 
                 command=services_window.destroy).pack(pady=10)
    
    def run(self):
        """Start the application"""
        self.window.mainloop()

# Start the application
if __name__ == "__main__":
    app = ShelterApp()
    app.run()