from flask import Flask, render_template, request, send_file
import mysql.connector
import pandas as pd
import os

app = Flask(__name__, template_folder="templates")

# ✅ Connect to MySQL
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="mysql",
        database="web_vulnerability_scanner"
    )
    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as err:
    print(f"❌ MySQL Connection Error: {err}")

# ✅ Route to Export Scan Results as CSV
@app.route("/export_csv")
def export_csv():
    cursor.execute("SELECT * FROM scans ORDER BY scan_date DESC")
    scans = cursor.fetchall()
    
    df = pd.DataFrame(scans)
    csv_file = "scan_results.csv"
    df.to_csv(csv_file, index=False)

    return send_file(csv_file, as_attachment=True)

# ✅ Dashboard Route (Existing Functionality)
@app.route("/", methods=["GET", "POST"])
def dashboard():
    search_query = request.form.get("search", "")
    filter_detected = request.form.get("filter_detected", "")

    page = request.args.get("page", 1, type=int)
    limit = 10
    offset = (page - 1) * limit

    query = "SELECT * FROM scans WHERE 1=1"
    params = []

    if search_query:
        query += " AND (target_url LIKE %s OR vulnerability_type LIKE %s)"
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if filter_detected:
        query += " AND detected = %s"
        params.append(filter_detected)

    query += " ORDER BY scan_date DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(query, params)
    scans = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM scans WHERE 1=1")
    total_scans = cursor.fetchone()["COUNT(*)"]
    total_pages = (total_scans // limit) + (1 if total_scans % limit > 0 else 0)

    return render_template("results.html", scans=scans, search_query=search_query, filter_detected=filter_detected, page=page, total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)