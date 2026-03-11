from flask import Flask, render_template, request, redirect, session
import sqlite3, os, smtplib

app = Flask(__name__)
app.secret_key = "your_secret_key"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def get_db():
    conn = sqlite3.connect("complaints.db")
    conn.row_factory = sqlite3.Row
    return conn

# ------------------ HOME ------------------
@app.route("/")
def home():
    return render_template("index.html")

# ------------------ SUBMIT COMPLAINT ------------------
@app.route("/submit", methods=["GET","POST"])
def submit():
    if request.method=="POST":
        name = request.form["name"]
        mobile = request.form["mobile"]
        email = request.form["email"]
        category = request.form["category"]
        priority = request.form["priority"]
        location = request.form["location"]

        image = request.files["image"]
        filename = image.filename
        if filename != "":
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO complaints
            (name,mobile,email,category,priority,location,image)
            VALUES (?,?,?,?,?,?,?)""",
            (name,mobile,email,category,priority,location,filename))
        conn.commit()
        conn.close()
        return "Complaint Submitted Successfully"
    return render_template("submit_complaint.html")

# ------------------ TRACK COMPLAINT ------------------
@app.route("/track", methods=["POST"])
def track():

    email = request.form["email"]

    return redirect(f"/user_dashboard/{email}")
# ------------------ USER DASHBOARD ------------------
@app.route("/user_dashboard/<email>", methods=["GET","POST"])
def user_dashboard(email):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM complaints WHERE email=?", (email,))
    data = cursor.fetchall()
    conn.close()
    return render_template("user_dashboard.html", data=data, email=email)

# ------------------ ADMIN DASHBOARD ------------------
@app.route("/admin")
def admin():
    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name,  email, status FROM complaints")
    data = cursor.fetchall()

    conn.close()

    return render_template("admin_dashboard.html", data=data)

# ------------------ UPDATE STATUS ------------------
@app.route("/update_status/<int:complaint_id>", methods=["POST"])
def update_status(complaint_id):
    new_status = request.form['status']

    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET status=? WHERE id=?", (new_status, complaint_id))
    conn.commit()
    conn.close()

    # Redirect back to staff dashboard
    return redirect("/staff")

    # Email notification if resolved
    if status=="Resolved":
        cursor.execute("SELECT email FROM complaints WHERE id=?", (id,))
        email = cursor.fetchone()["email"]
        send_email(email,id)

    conn.close()
    return redirect("/admin")

# ------------------ SEND EMAIL ------------------
def send_email(user_email, complaint_id):
    sender = "autianushka2008@gmail.com"
    password = "hsauiyumskxawptq"
    message = f"""Subject: Complaint Resolved

Your complaint ID {complaint_id} has been resolved.
Municipal Corporation
"""
    server = smtplib.SMTP("smtp.gmail.com",587)
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,user_email,message)
    server.quit()

# ------------------ USER FEEDBACK ------------------
@app.route("/feedback/<id>", methods=["POST"])
def feedback(id):
    user_feedback = request.form["feedback"]
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE complaints SET feedback=? WHERE id=?", (user_feedback,id))
    conn.commit()
    conn.close()
    return redirect(f"/user_dashboard/{request.form['email']}")

# ------------------ STATISTICS ------------------
@app.route("/statistics")
def statistics():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM complaints")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
    resolved = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
    pending = cursor.fetchone()[0]
    conn.close()
    return render_template("statistics.html", total=total, resolved=resolved, pending=pending)

@app.route("/staff")
def staff():
    conn = sqlite3.connect("complaints.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email,mobile,  status, feedback 
        FROM complaints
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template("staff_dashboard.html", data=data)

if __name__=="__main__":
    # Get the PORT from environment variable (provided by host), default to 5000 for local testing
    port = int(os.environ.get("PORT", 5000))
    # host=0.0.0.0 makes the app accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)