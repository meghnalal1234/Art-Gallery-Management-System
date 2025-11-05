from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from database.db_connect import get_db_connection
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# ==================== WEB PAGE ROUTES ====================

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/artists')
def artists_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Artist_art")
    artists = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('artists.html', artists=artists)

@app.route('/artworks')
def artworks_page():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.Artwork_ID, a.Title, a.Year_Created, a.Kind_of_Art, a.Price, 
               ar.Name AS Artist_Name
        FROM Artwork_art a
        LEFT JOIN Artist_art ar ON a.Artist_art_ID = ar.Artist_art_ID
    """)
    artworks = cursor.fetchall()
    
    # Get all artists for the dropdown
    cursor.execute("SELECT Artist_art_ID, Name FROM Artist_art")

    artists = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('artworks.html', artworks=artworks, artists=artists)

@app.route('/reserve')
def reserve_page():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get available artworks
    cursor.execute("""
        SELECT a.Artwork_ID, a.Title, a.Year_Created, a.Kind_of_Art, a.Price, 
               ar.Name AS Artist_Name
        FROM Artwork_art a
        LEFT JOIN Artist_art ar ON a.Artist_art_ID = ar.Artist_art_ID
    """)
    artworks = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('reserve.html', artworks=artworks)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Get user reservations
    cursor.execute("""
        SELECT r.Reservation_ID, a.Title, r.Status, r.Date
        FROM Reservation r
        JOIN Artwork_art a ON r.Artwork_ID = a.Artwork_ID
        WHERE r.Customer_ID = %s
        ORDER BY r.Date DESC
    """, (session['user_id'],))
    reservations = cursor.fetchall()
    
    # Get all artists and artworks for admin
    cursor.execute("SELECT COUNT(*) as count FROM Artist_art")
    artist_count = cursor.fetchone()['count']
    
    cursor.execute("SELECT COUNT(*) as count FROM Artwork_art")
    artwork_count = cursor.fetchone()['count']
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', 
                         user_name=session.get('user_name'),
                         user_role=session.get('user_role'),
                         reservations=reservations,
                         artist_count=artist_count,
                         artwork_count=artwork_count)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# ==================== ARTIST API ROUTES ====================

@app.route('/api/get_artists', methods=['GET'])
def get_artists():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Artist_art")
    artists = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(artists)

@app.route('/api/add_artist', methods=['POST'])
def add_artist():
    data = request.get_json()
    name = data.get('Name')
    birthplace = data.get('Birthplace')
    age = data.get('Age')
    style = data.get('Style')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Artist_art (Name, Birthplace, Age, Style)
        VALUES (%s, %s, %s, %s)
    """, (name, birthplace, age, style))
    conn.commit()
    artist_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Artist added successfully", "Artist_ID": artist_id}), 201

# ==================== ARTWORK API ROUTES ====================

@app.route('/api/get_artworks', methods=['GET'])
def get_artworks():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.*, ar.Name as Artist_Name
        FROM Artwork_art a
        LEFT JOIN Artist_art ar ON a.Artist_art_ID = ar.Artist_ID
    """)
    artworks = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(artworks)

@app.route('/api/add_artwork', methods=['POST'])
def add_artwork():
    data = request.get_json()
    title = data.get('Title')
    year_created = data.get('Year_Created')
    kind_of_art = data.get('Kind_of_Art')
    price = data.get('Price')
    artist_id = data.get('Artist_art_ID')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Artwork_art (Title, Year_Created, Kind_of_Art, Price, Artist_art_ID)
        VALUES (%s, %s, %s, %s, %s)
    """, (title, year_created, kind_of_art, price, artist_id))
    conn.commit()
    artwork_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Artwork added successfully", "Artwork_ID": artwork_id}), 201

# ==================== CUSTOMER API ROUTES ====================

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('Name')
    email = data.get('Email')
    password = data.get('Password')
    role = data.get('Role', 'Visitor')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if email already exists
    cursor.execute("SELECT * FROM Customer WHERE Email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Email already registered"}), 400
    
    cursor.execute("""
        INSERT INTO Customer (Name, Email, Password, Role)
        VALUES (%s, %s, %s, %s)
    """, (name, email, password, role))
    conn.commit()
    customer_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({"message": "Registration successful", "Customer_ID": customer_id}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('Email')
    password = data.get('Password')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Customer WHERE Email = %s AND Password = %s", (email, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user:
        session['user_id'] = user['Customer_ID']
        session['user_name'] = user['Name']
        session['user_role'] = user['Role']
        session.permanent = True  # Make session permanent
        return jsonify({
            "message": "Login successful",
            "Name": user['Name'],
            "Role": user['Role'],
            "Customer_ID": user['Customer_ID']
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# ==================== RESERVATION API ROUTES ====================

@app.route('/api/reserve', methods=['POST'])
def reserve():
    data = request.get_json()
    artwork_id = data.get('Artwork_ID')
    customer_id = data.get('Customer_ID')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Check if artwork is already reserved
    cursor.execute("""
        SELECT * FROM Reservation 
        WHERE Artwork_ID = %s AND Status = 'Reserved'
    """, (artwork_id,))
    existing = cursor.fetchone()
    
    status = 'Waitlisted' if existing else 'Reserved'
    date = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute("""
        INSERT INTO Reservation (Artwork_ID, Customer_ID, Status, Date)
        VALUES (%s, %s, %s, %s)
    """, (artwork_id, customer_id, status, date))
    conn.commit()
    reservation_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({
        "message": f"Reservation {status.lower()} successfully",
        "Reservation_ID": reservation_id,
        "Status": status
    }), 201

@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, a.Title, c.Name as Customer_Name
        FROM Reservation r
        JOIN Artwork_art a ON r.Artwork_ID = a.Artwork_ID
        JOIN Customer c ON r.Customer_ID = c.Customer_ID
        ORDER BY r.Date DESC
    """)
    reservations = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservations)

# Debug route to check session
@app.route('/api/session_info')
def session_info():
    return jsonify({
        'logged_in': 'user_id' in session,
        'user_id': session.get('user_id'),
        'user_name': session.get('user_name'),
        'user_role': session.get('user_role'),
        'session_keys': list(session.keys())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)