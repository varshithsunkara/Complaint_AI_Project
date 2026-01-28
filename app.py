from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# ---------- DATABASE SETUP ----------
def init_db():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            complaint TEXT,
            category TEXT,
            solution TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------- AI CATEGORY DETECTION ----------
def classify_complaint(text):
    text = text.lower()

    if "water" in text or "tap" in text or "pipe" in text:
        return "Water Problem 💧"
    elif "electric" in text or "current" in text or "power" in text:
        return "Electricity Problem ⚡"
    elif "road" in text or "pothole" in text:
        return "Road Problem 🚧"
    elif "garbage" in text or "waste" in text:
        return "Garbage Problem 🗑️"
    else:
        return "General Problem ❓"

# ---------- AI SOLUTION GENERATOR ----------
def get_solution(category):
    solutions = {
        "Water Problem 💧": "Check pipelines and contact the water department.",
        "Electricity Problem ⚡": "Report to the electricity board and check power lines.",
        "Road Problem 🚧": "Inform the municipality for road repair.",
        "Garbage Problem 🗑️": "Request garbage collection service.",
        "General Problem ❓": "Forward to concerned department."
    }
    return solutions.get(category, "Forward to concerned department.")

# ---------- HOME PAGE ----------
@app.route('/')
def home():
    return render_template("index.html")

# ---------- SUBMIT COMPLAINT ----------
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    complaint = request.form['complaint']

    category = classify_complaint(complaint)
    solution = get_solution(category)

    # Save to database
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("INSERT INTO complaints (name, complaint, category, solution) VALUES (?, ?, ?, ?)",
              (name, complaint, category, solution))
    conn.commit()
    conn.close()

    return f"""
    <h2>Complaint Received!</h2>
    <p><b>Name:</b> {name}</p>
    <p><b>Complaint:</b> {complaint}</p>
    <p><b>AI Category:</b> {category}</p>
    <p><b>Suggested Solution:</b> {solution}</p>
    <br>
    <a href="/">Go Back</a>
    """

# ---------- ADMIN DASHBOARD ----------
@app.route('/admin')
def admin():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("SELECT * FROM complaints")
    data = c.fetchall()
    conn.close()

    return render_template("admin.html", complaints=data)

# ---------- RUN APP ----------
if __name__ == "__main__":
    app.run()
