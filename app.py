from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",  # CHANGE THIS
    database="canteen_db"
)

cursor = db.cursor(dictionary=True)

# HOME PAGE
@app.route('/')
def home():
    return render_template('home.html')

# MENU PAGE
@app.route('/menu')
def menu():
    cursor.execute("SELECT * FROM Menu")
    items = cursor.fetchall()
    return render_template('menu.html', items=items)

# ORDER PAGE
@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        student_id = request.form['student_id']
        item_id = request.form['item_id']
        quantity = request.form['quantity']

        cursor.execute(
            "INSERT INTO Orders (student_id, item_id, quantity) VALUES (%s, %s, %s)",
            (student_id, item_id, quantity)
        )
        db.commit()

        order_id = cursor.lastrowid

        # Generate token number
        cursor.execute("SELECT COUNT(*) as count FROM Tokens")
        token_number = cursor.fetchone()['count'] + 1

        cursor.execute(
            "INSERT INTO Tokens (order_id, token_number, status) VALUES (%s, %s, 'Pending')",
            (order_id, token_number)
        )
        db.commit()

        return redirect('/tokens')

    cursor.execute("SELECT * FROM Menu")
    items = cursor.fetchall()
    return render_template('order.html', items=items)

# TOKENS PAGE
@app.route('/tokens')
def tokens():
    cursor.execute("""
        SELECT t.token_id, t.token_number, t.status, m.item_name, o.quantity
        FROM Tokens t
        JOIN Orders o ON t.order_id = o.order_id
        JOIN Menu m ON o.item_id = m.item_id
        ORDER BY t.token_number DESC
    """)
    tokens = cursor.fetchall()
    return render_template('tokens.html', tokens=tokens)

# UPDATE STATUS
@app.route('/update_status/<int:token_id>')
def update_status(token_id):
    cursor.execute("""
        UPDATE Tokens 
        SET status = CASE 
            WHEN status='Pending' THEN 'Ready'
            WHEN status='Ready' THEN 'Delivered'
            ELSE 'Delivered'
        END
        WHERE token_id=%s
    """, (token_id,))
    db.commit()
    return redirect('/tokens')

if __name__ == '__main__':
    app.run(debug=True)
