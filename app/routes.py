from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, abort
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import sqlite3
from .database import get_db_connection
from .models import User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    conn.close()
    return render_template('index.html', services=services)

@main.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        vehicle_no = request.form['vehicle_no']
        vehicle_type = request.form['vehicle_type']
        
        hashed_pw = generate_password_hash(password)
        
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (name, email, password_hash, phone, vehicle_no, vehicle_type) VALUES (?, ?, ?, ?, ?, ?)',
                         (name, email, hashed_pw, phone, vehicle_no, vehicle_type))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('main.login'))
        except sqlite3.IntegrityError:
            flash('Email already registered.', 'error')
        finally:
            conn.close()
            
    return render_template('register.html')

@main.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data['id'], user_data['name'], user_data['email'], user_data['role'], 
                       user_data['phone'], user_data['vehicle_no'], user_data['vehicle_type'])
            login_user(user)
            flash('Logged in successfully.', 'success')
            if user.role == 'admin':
                return redirect(url_for('main.admin_dashboard'))
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            
    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('main.index'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('main.admin_dashboard'))
        
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, s.name as service_name 
        FROM bookings b
        JOIN services s ON b.service_id = s.id
        WHERE b.user_id = ?
        ORDER BY b.booking_date DESC, b.start_time DESC
    ''', (current_user.id,)).fetchall()
    conn.close()
    return render_template('dashboard.html', bookings=bookings)

@main.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
        
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT b.*, s.name as service_name, u.name as customer_name, u.phone, u.vehicle_no 
        FROM bookings b
        JOIN services s ON b.service_id = s.id
        JOIN users u ON b.user_id = u.id
        ORDER BY b.booking_date DESC, b.start_time DESC
    ''').fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

@main.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        abort(403)
        
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM users ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('admin_users.html', users=users)

@main.route('/admin/update_status/<int:booking_id>', methods=['POST'])
@login_required
def update_status(booking_id):
    if current_user.role != 'admin':
        abort(403)
    
    new_status = request.form['status']
    conn = get_db_connection()
    conn.execute('UPDATE bookings SET status = ? WHERE id = ?', (new_status, booking_id))
    conn.commit()
    conn.close()
    flash('Booking status updated.', 'success')
    return redirect(url_for('main.admin_dashboard'))

@main.route('/book', methods=('GET', 'POST'))
@login_required
def book():
    conn = get_db_connection()
    services = conn.execute('SELECT * FROM services').fetchall()
    
    if request.method == 'POST':
        service_id = request.form['service_id']
        booking_date = request.form['booking_date']
        start_time = request.form['start_time']
        
        service = conn.execute('SELECT * FROM services WHERE id = ?', (service_id,)).fetchone()
        duration = service['duration_minutes']
        
        start_dt = datetime.strptime(start_time, '%H:%M')
        end_dt = start_dt + timedelta(minutes=duration)
        end_time = end_dt.strftime('%H:%M')
        
        try:
            cur = conn.execute('INSERT INTO bookings (user_id, service_id, booking_date, start_time, end_time) VALUES (?, ?, ?, ?, ?)',
                               (current_user.id, service_id, booking_date, start_time, end_time))
            booking_id = cur.lastrowid
            
            conn.commit()
            return redirect(url_for('main.booking_confirmed', booking_id=booking_id))
            
        except sqlite3.Error as e:
            flash(f"An error occurred: {e}", 'error')
        finally:
            conn.close()
            
    conn.close()
    return render_template('booking.html', services=services)

@main.route('/api/slots')
def get_slots():
    date_str = request.args.get('date')
    if not date_str:
        return jsonify([])
    
    conn = get_db_connection()
    bookings = conn.execute('SELECT start_time, end_time FROM bookings WHERE booking_date = ?', (date_str,)).fetchall()
    conn.close()
    
    slots = []
    start_hour = 9
    end_hour = 17
    
    for h in range(start_hour, end_hour):
        time_str = f"{h:02d}:00"
        is_taken = False
        for b in bookings:
            if b['start_time'] == time_str:
                is_taken = True
                break
        
        if not is_taken:
            slots.append(time_str)
            
    return jsonify(slots)

@main.route('/booking-confirmed/<int:booking_id>')
@login_required
def booking_confirmed(booking_id):
    conn = get_db_connection()
    booking = conn.execute('''
        SELECT b.*, s.name as service_name, u.name as customer_name 
        FROM bookings b
        JOIN services s ON b.service_id = s.id
        JOIN users u ON b.user_id = u.id
        WHERE b.id = ?
    ''', (booking_id,)).fetchone()
    conn.close()
    
    # Security check
    if booking['user_id'] != current_user.id and current_user.role != 'admin':
        abort(403)
        
    return render_template('success.html', booking=booking)
