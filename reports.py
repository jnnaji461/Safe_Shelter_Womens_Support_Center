# reports.py - Reporting module for Safe Shelter
import sqlite3
from datetime import datetime, timedelta
import csv

class ShelterReports:
    @staticmethod
    def monthly_report(year_month=None):
        """Generate monthly activity report"""
        if year_month is None:
            year_month = datetime.now().strftime("%Y-%m")
        
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        
        # Get month start and end
        year, month = map(int, year_month.split('-'))
        
        print(f"\n{'='*60}")
        print(f"SAFE SHELTER - MONTHLY REPORT: {year_month}")
        print(f"{'='*60}")
        
        # New residents this month
        cursor.execute('''
            SELECT COUNT(*) FROM residents 
            WHERE strftime('%Y-%m', entry_date) = ?
        ''', (year_month,))
        new_residents = cursor.fetchone()[0]
        
        # Services provided this month
        cursor.execute('''
            SELECT service_type, COUNT(*) as count 
            FROM services 
            WHERE strftime('%Y-%m', service_date) = ?
            GROUP BY service_type
            ORDER BY count DESC
        ''', (year_month,))
        services = cursor.fetchall()
        
        # Total residents
        cursor.execute('SELECT COUNT(*) FROM residents')
        total_residents = cursor.fetchone()[0]
        
        # Print report
        print(f"\n📊 MONTHLY STATISTICS")
        print(f"   New Residents: {new_residents}")
        print(f"   Total Residents: {total_residents}")
        
        if services:
            print(f"\n📋 SERVICES PROVIDED")
            for service_type, count in services:
                print(f"   {service_type}: {count}")
            total_services = sum(count for _, count in services)
            print(f"   Total Services: {total_services}")
        else:
            print(f"\n📋 No services recorded this month")
        
        # Top residents by services
        cursor.execute('''
            SELECT r.first_name, r.last_name, COUNT(s.id) as service_count
            FROM residents r
            LEFT JOIN services s ON r.id = s.resident_id AND strftime('%Y-%m', s.service_date) = ?
            GROUP BY r.id
            ORDER BY service_count DESC
            LIMIT 5
        ''', (year_month,))
        top_residents = cursor.fetchall()
        
        if top_residents:
            print(f"\n👥 TOP RESIDENTS BY SERVICES")
            for first, last, count in top_residents:
                if count > 0:
                    print(f"   {first} {last}: {count} services")
        
        conn.close()
        
        # Save to CSV
        filename = f"shelter_report_{year_month}.csv"
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Safe Shelter Monthly Report', year_month])
            writer.writerow([])
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['New Residents', new_residents])
            writer.writerow(['Total Residents', total_residents])
            writer.writerow([])
            writer.writerow(['Service Type', 'Count'])
            for service_type, count in services:
                writer.writerow([service_type, count])
        
        print(f"\n💾 Report saved to: {filename}")
        print(f"{'='*60}")
        return filename

    @staticmethod
    def generate_system_report():
        """Generate comprehensive system report"""
        conn = sqlite3.connect('shelter.db')
        cursor = conn.cursor()
        
        report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n{'='*70}")
        print(f"SAFE SHELTER - COMPREHENSIVE SYSTEM REPORT")
        print(f"Generated: {report_date}")
        print(f"{'='*70}")
        
        # 1. Basic Statistics
        cursor.execute('SELECT COUNT(*) FROM residents')
        total_residents = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM services')
        total_services = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT service_type) FROM services')
        unique_service_types = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(DISTINCT strftime("%Y-%m", service_date)) FROM services')
        active_months = cursor.fetchone()[0]
        
        print(f"\n📈 SYSTEM OVERVIEW")
        print(f"   Total Residents: {total_residents}")
        print(f"   Total Services Provided: {total_services}")
        print(f"   Unique Service Types: {unique_service_types}")
        print(f"   Active Months (with services): {active_months}")
        
        # 2. Recent Activity (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        cursor.execute('SELECT COUNT(*) FROM residents WHERE entry_date >= ?', (thirty_days_ago,))
        recent_residents = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM services WHERE service_date >= ?', (thirty_days_ago,))
        recent_services = cursor.fetchone()[0]
        
        print(f"\n🔄 RECENT ACTIVITY (Last 30 days)")
        print(f"   New Residents: {recent_residents}")
        print(f"   Services Provided: {recent_services}")
        
        # 3. Service Breakdown
        print(f"\n📊 SERVICE BREAKDOWN")
        cursor.execute('''
            SELECT service_type, COUNT(*) as count, 
                   COUNT(DISTINCT resident_id) as unique_residents
            FROM services 
            GROUP BY service_type 
            ORDER BY count DESC
        ''')
        
        service_stats = cursor.fetchall()
        for service_type, count, unique_res in service_stats:
            print(f"   {service_type}: {count} sessions, {unique_res} residents")
        
        # 4. Current Month Summary
        current_month = datetime.now().strftime("%Y-%m")
        print(f"\n📅 CURRENT MONTH ({current_month})")
        
        cursor.execute('SELECT COUNT(*) FROM residents WHERE strftime("%Y-%m", entry_date) = ?', 
                      (current_month,))
        month_residents = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM services WHERE strftime("%Y-%m", service_date) = ?', 
                      (current_month,))
        month_services = cursor.fetchone()[0]
        
        print(f"   New Residents This Month: {month_residents}")
        print(f"   Services This Month: {month_services}")
        
        conn.close()
        
        # Save to file
        filename = f"system_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(f"Safe Shelter System Report\n")
            f.write(f"Generated: {report_date}\n")
            f.write("="*50 + "\n\n")
            f.write(f"Total Residents: {total_residents}\n")
            f.write(f"Total Services: {total_services}\n")
            f.write(f"Recent Residents (30 days): {recent_residents}\n")
            f.write(f"Recent Services (30 days): {recent_services}\n")
        
        print(f"\n💾 Report saved to: {filename}")
        print(f"{'='*70}")
        return filename

# Test the reports
if __name__ == "__main__":
    print("Testing Shelter Reports...")
    ShelterReports.monthly_report("2025-12")
    ShelterReports.generate_system_report()