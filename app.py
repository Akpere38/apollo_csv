from flask import Flask, request, send_file, render_template
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Define column mapping
COLUMN_MAPPING = {
    "First Name": "first_name",
    "Last Name": "last_name",
    "Title": "position",
    "Email": "email",
    "Company": "company",
    "Corporate Phone": "phone"
}
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return "No file part", 400
    
    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Process CSV
    df = pd.read_csv(file_path)
    df = df[["First Name", "Last Name", "Title", "Email", "Company", "Corporate Phone"]]  # Filter columns
    df = df.rename(columns=COLUMN_MAPPING)

    # Create processed file name
    processed_filename = f"payload_{file.filename}"
    print(processed_filename)
    processed_file_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    df.to_csv(processed_file_path, index=False)
    
    return send_file(processed_file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
