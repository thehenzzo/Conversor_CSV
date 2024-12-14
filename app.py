from flask import Flask, request, render_template, send_file
import os
import re
import csv
from io import StringIO

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_list(file_content):
    csv_output = StringIO()
    csv_writer = csv.writer(csv_output)

    lines = file_content.strip().split("\n")
    phone_pattern = re.compile(r"^\+?\d{9,15}$")

    for line in lines:
        items = line.split()
        phone = None
        name = []

        for item in items:
            if phone_pattern.match(item) or item.isdigit():
                phone = f"55{item.strip('+')}"
            else:
                name.append(item)

        if phone:
            csv_writer.writerow([phone, " ".join(name)])

    csv_output.seek(0)
    return csv_output

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("file")

        if uploaded_file and uploaded_file.filename:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(file_path)

            with open(file_path, "r", encoding="utf-8") as file:
                processed_content = process_list(file.read())

            processed_path = os.path.join(PROCESSED_FOLDER, "mailing.csv")
            with open(processed_path, "w", newline='') as processed_file:
                processed_file.write(processed_content.getvalue())

            return send_file(
                processed_path,
                as_attachment=True,
                download_name="mailing.csv",
                mimetype="text/csv",
            )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)