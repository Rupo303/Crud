from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="crud_db"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("index.html", users=users)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    cursor.execute("INSERT INTO users (name, email, age) VALUES (%s, %s, %s)", (name, email, age))
    db.commit()
    return redirect('/')

@app.route('/edit/<int:id>')
def edit(id):
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    return render_template("edit.html", user=user)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']
    cursor.execute("UPDATE users SET name=%s, email=%s, age=%s WHERE id=%s", (name, email, age, id))
    db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    cursor.execute("DELETE FROM users WHERE id = %s", (id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)