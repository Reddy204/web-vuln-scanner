Web Vulnerability Scanner
A Flask-based security scanner that detects common vulnerabilities like SQL Injection, XSS, Directory Traversal, Broken Authentication, and Security Header Issues.

🚀 Features
✔ SQL Injection Detection
✔ XSS (Cross-Site Scripting) Scanner
✔ Directory Traversal Checks
✔ Broken Authentication Detection
✔ Security Header Analysis
✔ Stores Results in MySQL
✔ Exports Reports as CSV
✔ Deployable to Heroku

🛠 Installation & Setup
1️⃣ Clone the Repository
Run this command in VS Code Terminal:
git clone https://github.com/Reddy204/web-vuln-scanner.git
cd web-vuln-scanner

2️⃣ Install Dependencies
Install required Python packages:
pip install -r requirements.txt


3️⃣ Configure MySQL Database
Run these SQL commands to set up the database:
CREATE DATABASE web_vulnerability_scanner;
USE web_vulnerability_scanner;

CREATE TABLE scans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    target_url VARCHAR(255),
    vulnerability_type VARCHAR(255),
    payload VARCHAR(255),
    detected BOOLEAN,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



🛠 Running the Scanner
Start your Flask application:
python app.py


✔ Open your browser and test a website for vulnerabilities:
http://127.0.0.1:5000/scan?url=https://demo.owasp-juice.shop


✔ To export results as CSV:
http://127.0.0.1:5000/export_csv


✅ Downloads scan_results.csv with all stored vulnerabilities.

🚀 Deployment to Heroku
1️⃣ Install Heroku CLI
pip install gunicorn


✔ gunicorn allows Flask to run in a production environment.
2️⃣ Create Procfile (Heroku Startup File)
Inside your project folder (web-vuln-scanner), create a new file called:
Procfile


Add this line:
web: gunicorn app:app


✔ This tells Heroku how to run your Flask app.
3️⃣ Deploy to Heroku
heroku login
heroku create web-vuln-scanner
git add .
git commit -m "Deploy to Heroku"
git push heroku main
heroku open


✔ Your Flask vulnerability scanner is now live! 🎉

📌 License & Disclaimer
This project is for educational purposes only. Do not use it to scan unauthorized websites.

🤝 Contributions & Feedback
Pull requests are welcome! If you find issues or want to add new vulnerability checks, feel free to contribute.



