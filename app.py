from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_user",       # replace with your MySQL username
        password="your_mysql_password", # replace with your MySQL password
        database="student_db"
    )

@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['studentName']
    phone = request.form['phoneNo']
    email = request.form['studentEmail']

    if name and phone and email:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
        conn.commit()
        conn.close()
    
    return index()  # Show updated data on reload

if __name__ == '__main__':
    app.run(debug=True)
