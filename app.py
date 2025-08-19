from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host="mysql",        # service name of MySQL container
        user="flask_user",
        password="flask_pass",
        database="flask_db"
    )
    return conn

# Simple HTML form
HTML = """
<!doctype html>
<title>Employee Form</title>
<h2>Add Employee</h2>
<form method="POST">
  Name: <input type="text" name="name" required>
  <input type="submit" value="Add">
</form>
<h3>Employees:</h3>
<ul>
{% for emp in employees %}
  <li>{{ emp }}</li>
{% endfor %}
</ul>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        name = request.form["name"]
        cur.execute("INSERT INTO employees (name) VALUES (%s)", (name,))
        conn.commit()

    cur.execute("SELECT name FROM employees")
    employees = [row[0] for row in cur.fetchall()]
    conn.close()
    return render_template_string(HTML, employees=employees)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

