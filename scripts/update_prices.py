import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import get_db_connection

def update_prices():
    conn = get_db_connection()
    
    # Update prices to realistic INR values
    updates = [
        (499.00, 'Basic Wash'),
        (999.00, 'Premium Wash'),
        (2499.00, 'Deluxe Detail')
    ]
    
    print("Updating prices to INR...")
    for price, name in updates:
        conn.execute('UPDATE services SET price = ? WHERE name = ?', (price, name))
        print(f"Updated {name} to ₹{price}")
        
    conn.commit()
    conn.close()
    print("Price update complete.")

if __name__ == '__main__':
    update_prices()
