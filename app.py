from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import mysql.connector

app = Flask(__name__)

# ✅ Connect to MySQL Database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",  # Replace with your MySQL username
        password="mysql",  # Replace with your MySQL password
        database="web_vulnerability_scanner"
    )
    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as err:
    print(f"❌ MySQL Connection Error: {err}")

# ✅ Function to Store Scan Results in MySQL
def store_scan(target_url, vulnerability, payload):
    query = "INSERT INTO scans (target_url, vulnerability_type, payload, detected) VALUES (%s, %s, %s, %s)"
    values = (target_url, vulnerability, payload, True if vulnerability else False)
    cursor.execute(query, values)
    db.commit()

# ✅ Homepage Route
@app.route("/")
def home():
    return "Flask Vulnerability Scanner is Running!"

# ✅ SQL Injection Scanner
sql_payloads = ["' OR '1'='1", "' UNION SELECT NULL, NULL --", "'; DROP TABLE users; --"]
def scan_sql_injection(target_url):
    try:
        for payload in sql_payloads:
            response = requests.get(target_url + "?id=" + payload, timeout=5)
            if "error" in response.text.lower() or "syntax" in response.text.lower():
                store_scan(target_url, "SQL Injection", payload)
                return {"vulnerability": "SQL Injection", "payload": payload}
        return {"vulnerability": None}
    except requests.exceptions.RequestException:
        return {"error": "Could not reach target URL"}

# ✅ XSS Scanner
xss_payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
def scan_xss(target_url):
    try:
        for payload in xss_payloads:
            response = requests.get(target_url + "?search=" + payload, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            if payload in str(soup):
                store_scan(target_url, "XSS", payload)
                return {"vulnerability": "XSS", "payload": payload}
        return {"vulnerability": None}
    except requests.exceptions.RequestException:
        return {"error": "Could not reach target URL"}

# ✅ Directory Traversal Scanner
def scan_directory_traversal(target_url):
    try:
        payloads = ["../../../etc/passwd", "../../admin.php"]
        for payload in payloads:
            response = requests.get(target_url + f"?file={payload}", timeout=5)
            if "root:x:" in response.text or "Admin Panel" in response.text:
                store_scan(target_url, "Directory Traversal", payload)
                return {"vulnerability": "Directory Traversal", "payload": payload}
        return {"vulnerability": None}
    except requests.exceptions.RequestException:
        return {"error": "Could not reach target URL"}

# ✅ Broken Authentication Test
def scan_broken_auth(target_url):
    try:
        test_url = target_url + "/admin"
        response = requests.get(test_url, timeout=5)
        if response.status_code == 200 and "login" not in response.text.lower():
            store_scan(target_url, "Broken Authentication", "/admin")
            return {"vulnerability": "Broken Authentication", "payload": "/admin"}
        return {"vulnerability": None}
    except requests.exceptions.RequestException:
        return {"error": "Could not reach target URL"}

# ✅ Security Headers Test
def scan_security_headers(target_url):
    try:
        response = requests.get(target_url, timeout=5)
        headers = response.headers

        missing_headers = []
        required_headers = ["Content-Security-Policy", "Strict-Transport-Security", "X-Frame-Options"]
        
        for header in required_headers:
            if header not in headers:
                missing_headers.append(header)

        if missing_headers:
            store_scan(target_url, "Missing Security Headers", ", ".join(missing_headers))
            return {"vulnerability": "Missing Security Headers", "payload": missing_headers}
        return {"vulnerability": None}
    except requests.exceptions.RequestException:
        return {"error": "Could not reach target URL"}

# ✅ Flask Route to Perform Scanning on External Sites
@app.route("/scan", methods=["GET"])
def scan():
    target_url = request.args.get("url")
    
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400
    
    if not target_url.startswith("http"):
        return jsonify({"error": "Invalid URL format"}), 400

    try:
        results = {
            "sql_injection": scan_sql_injection(target_url),
            "xss": scan_xss(target_url),
            "directory_traversal": scan_directory_traversal(target_url),
            "broken_auth": scan_broken_auth(target_url),
            "security_headers": scan_security_headers(target_url)
        }

        return jsonify({"target_url": target_url, "scan_results": results})

    except requests.exceptions.RequestException:
        return jsonify({"error": "Could not reach target URL"}), 400

if __name__ == "__main__":
    app.run(debug=True)