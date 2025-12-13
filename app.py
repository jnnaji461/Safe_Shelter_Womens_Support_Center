# app.py - Flask web application for Safe Shelter
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)

# Home page - Dashboard
@app.route('/')
def index():
    conn = sqlite3.connect('shelter.db')
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) FROM residents')
    total_residents = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM services')
    total_services = cursor.fetchone()[0]
    
    # Get recent residents
    cursor.execute('SELECT * FROM residents ORDER BY entry_date DESC LIMIT 5')
    recent_residents = cursor.fetchall()
    
    # Get recent services
    cursor.execute('''
        SELECT s.id, r.first_name, r.last_name, s.service_type, s.service_date
        FROM services s
        JOIN residents r ON s.resident_id = r.id
        ORDER BY s.service_date DESC LIMIT 5
    ''')
    recent_services = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         total_residents=total_residents,
                         total_services=total_services,
                         recent_residents=recent_residents,
                         recent_services=recent_services)

# Residents page
@app.route('/residents')
def residents():
    conn = sqlite3.connect('shelter.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM residents ORDER BY entry_date DESC')
    residents = cursor.fetchall()
    conn.close()
    return render_template('residents.html', residents=residents)

# Add resident
@app.route('/add_resident', methods=['POST'])
def add_resident():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    
    if first_name and last_name:
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        
        # Check for duplicate
        cursor.execute(
            'SELECT id FROM residents WHERE LOWER(first_name) = LOWER(?) AND LOWER(last_name) = LOWER(?)',
            (first_name, last_name)
        )
        
        if not cursor.fetchone():  # Only add if not duplicate
            cursor.execute(
                'INSERT INTO residents (first_name, last_name, entry_date) VALUES (?, ?, ?)',
                (first_name, last_name, str(date.today()))
            )
            conn.commit()
        
        conn.close()
    
    return redirect(url_for('residents'))

# Services page
@app.route('/services')
def services():
    conn = sqlite3.connect('shelter.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT s.id, r.first_name, r.last_name, s.service_type, s.service_date
        FROM services s
        JOIN residents r ON s.resident_id = r.id
        ORDER BY s.service_date DESC
    ''')
    services = cursor.fetchall()
    
    cursor.execute('SELECT id, first_name, last_name FROM residents ORDER BY last_name')
    residents = cursor.fetchall()
    
    conn.close()
    return render_template('services.html', services=services, residents=residents)

# Log service
@app.route('/log_service', methods=['POST'])
def log_service():
    resident_id = request.form['resident_id']
    service_type = request.form['service_type']
    
    if resident_id and service_type:
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO services (resident_id, service_type, service_date) VALUES (?, ?, ?)',
            (resident_id, service_type, str(date.today()))
        )
        conn.commit()
        conn.close()
    
    return redirect(url_for('services'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)